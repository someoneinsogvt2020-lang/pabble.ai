import re

from .base import Tool
from .router import router


class ChartGeneratorTool(Tool):
    """
    Detects chart/visualization requests and instructs the LLM to emit a
    structured [GENERATE_CHART: type] block that the frontend (index.html /
    renderChartClientSide) parses and renders with Chart.js.

    Ground-up rewrite. Same output contract as before (block format, JSON
    schema, chart type strings) so the frontend needs no changes — but the
    detection and guidance logic is redesigned:

      1. Word-boundary matching + an exclusion list, so idiomatic uses of
         "chart" ("off the charts", "flowchart", "eye chart", "chart a
         course") don't falsely trigger the tool.
      2. A scored heuristic pre-selects the most likely chart type from the
         prompt's wording, instead of dumping a 10-option menu on a small
         local model and hoping it reasons well.
      3. Lightweight inline data extraction: obvious "Label: number" pairs
         already present in the prompt are pulled out and handed to the
         model directly, so it copies rather than invents them.
    """

    name = "chart_generator"

    # ------------------------------------------------------------------
    # Matching
    # ------------------------------------------------------------------

    # Each pattern is matched with word boundaries via re.search.
    _TRIGGER_PATTERNS = [
        r"charts?", r"graphs?", r"plots?",
        r"bar chart", r"line chart", r"pie chart", r"area chart",
        r"bar graph", r"line graph", r"pie graph", r"area graph",
        r"histogram", r"scatter ?plot", r"scatter chart",
        r"donut chart", r"doughnut chart", r"radar chart", r"spider chart",
        r"stacked bar", r"stacked chart", r"grouped bar",
        r"bubble chart", r"funnel chart", r"gauge chart",
        r"visuali[sz]e", r"visuali[sz]ation",
        r"plot (this|the data|it)", r"graph (this|it)", r"chart (this|it)",
        r"show me a (chart|graph|plot)", r"generate a (chart|graph|plot)",
        r"track over time", r"trend over time", r"show the trend",
        r"compare these numbers", r"compare the (data|figures)",
        r"show (the )?(breakdown|distribution|proportion)",
        r"(chart|graph|plot|breakdown) of",
    ]
    _TRIGGER_RE = re.compile(
        r"\b(" + "|".join(_TRIGGER_PATTERNS) + r")\b", re.IGNORECASE
    )

    # Phrases that contain a trigger word but are NOT data-visualization
    # requests. Checked first; any hit here blocks the match entirely.
    _EXCLUSION_PATTERNS = [
        r"flow ?chart", r"org(anization)?al? chart", r"seating chart",
        r"eye chart", r"chart (a course|my course)", r"off the charts?",
        r"chart[- ]?topping", r"chart your (progress|journey|path)"
        r"|chart out( a| my)? plan",
        r"gantt chart",  # project-management diagram, not a data chart here
        r"what is a (chart|graph|plot)", r"how (do|does) .*(chart|graph|plot)",
    ]
    _EXCLUSION_RE = re.compile(
        "(" + "|".join(_EXCLUSION_PATTERNS) + ")", re.IGNORECASE
    )

    def match(self, prompt):
        if self._EXCLUSION_RE.search(prompt):
            return False
        return bool(self._TRIGGER_RE.search(prompt))

    # ------------------------------------------------------------------
    # Chart type catalogue
    # ------------------------------------------------------------------

    CHART_TYPE_HINTS = {
        "bar": "Comparing discrete categories (e.g. sales by region).",
        "grouped_bar": "Comparing 2+ series side-by-side per category (e.g. revenue vs cost by quarter).",
        "stacked_bar": "Showing how parts make up a whole across categories (e.g. expenses by department per month).",
        "line": "Trends over a continuous axis like time (e.g. monthly revenue).",
        "area": "Like line, but emphasizes cumulative magnitude/volume under the curve.",
        "pie": "Proportions of a whole, single series, ideally <= 7 slices.",
        "donut": "Same use case as pie, hollow center, same data schema as pie.",
        "scatter": "Correlation between two numeric variables.",
        "radar": "Comparing multiple metrics across a small number of entities (e.g. skill ratings).",
        "histogram": "Distribution of a single numeric variable across buckets.",
    }

    # Scored keyword groups used to *suggest* a type instead of leaving a
    # small model to guess cold from a 10-item menu.
    _TYPE_SIGNALS = {
        "line": ["over time", "trend", "growth", "monthly", "weekly", "daily",
                 "yearly", "quarterly", "timeline", "progression", "history of"],
        "pie": ["proportion", "percentage", "share of", "breakdown", "split",
                "distribution of market", "makeup of", "composition"],
        "scatter": ["correlation", "relationship between", "versus", " vs ",
                    "plotted against"],
        "histogram": ["distribution", "frequency", "how often", "spread of"],
        "radar": ["skills", "ratings across", "multi-metric", "comparison across metrics"],
        "stacked_bar": ["by department", "by category and", "parts of a whole across"],
        "grouped_bar": ["side by side", "compare .* and .* by", "revenue vs cost",
                         "actual vs target", "actual vs budget"],
        "bar": ["compare", "comparison", "ranking", "top ", "highest", "lowest"],
    }

    def _suggest_type(self, text):
        """Score each type by keyword hits in the prompt; return the best
        match, or None if nothing stands out (let the model decide)."""
        best_type, best_score = None, 0
        for chart_type, signals in self._TYPE_SIGNALS.items():
            score = sum(1 for sig in signals if re.search(sig, text))
            if score > best_score:
                best_type, best_score = chart_type, score
        return best_type

    # ------------------------------------------------------------------
    # Lightweight inline data extraction
    # ------------------------------------------------------------------

    # Matches things like "Marketing: 12000", "Q1 - 45", "Apples, 30"
    _DATA_PAIR_RE = re.compile(
        r"([A-Za-z][A-Za-z0-9 _/&'\-]{0,40}?)\s*[:\-,]\s*\$?(-?\d[\d,]*\.?\d*)\b"
    )

    def _extract_data_pairs(self, text):
        pairs = []
        for label, value in self._DATA_PAIR_RE.findall(text):
            label = label.strip()
            if not label or len(pairs) >= 25:
                continue
            try:
                num = float(value.replace(",", ""))
            except ValueError:
                continue
            pairs.append((label, num))
        return pairs

    # ------------------------------------------------------------------
    # Prompt augmentation
    # ------------------------------------------------------------------

    def apply(self, prompt, history):
        text = prompt.lower()
        suggested_type = self._suggest_type(text)
        data_pairs = self._extract_data_pairs(prompt)

        type_guide = "\n".join(f'- "{k}": {v}' for k, v in self.CHART_TYPE_HINTS.items())

        suggestion_block = ""
        if suggested_type:
            suggestion_block = (
                f'\nSUGGESTED TYPE based on the request wording: "{suggested_type}" '
                f"({self.CHART_TYPE_HINTS[suggested_type]}) — use this unless the "
                f"data clearly fits a different type better.\n"
            )

        data_block = ""
        if data_pairs:
            listed = "\n".join(f'  - "{label}": {value:g}' for label, value in data_pairs)
            data_block = (
                "\nDATA DETECTED DIRECTLY IN THE USER'S MESSAGE — copy these labels "
                "and values exactly, do not re-derive or round them:\n" + listed + "\n"
            )

        instruction = f"""

[SYSTEM CHART TOOL ACTIVE]

You MUST respond ONLY with a chart data block in this EXACT format. Do NOT add any text before or after the block, and do NOT wrap it in markdown code fences.

[GENERATE_CHART: <type>]
{{
  "title": "Short descriptive title",
  "x_label": "X axis label (omit for pie or donut)",
  "y_label": "Y axis label (omit for pie or donut)",
  "series": [
    {{
      "name": "Series name (use the category/segment name itself for pie or donut)",
      "color": "#0a84ff",
      "data": [
        {{"label": "Category A", "value": 10}},
        {{"label": "Category B", "value": 20}}
      ]
    }}
  ]
}}
[/GENERATE_CHART]

Allowed <type> values and when to use each:
{type_guide}
{suggestion_block}{data_block}
SCHEMA RULES:
1. "series" is ALWAYS a list, even for single-series charts like a simple bar or pie chart — just include one object in the list.
2. For "bar", "line", "area", "grouped_bar", "stacked_bar", and "radar": include 2+ entries in "series" only when the user's data genuinely has multiple categories/groups to compare (e.g. "revenue and profit by quarter"). Otherwise use exactly one series.
3. For "pie" or "donut": You may use exactly one series where each "data" entry is a slice, OR you may use multiple series where each series represents a slice with a single "data" entry (e.g. {{"label": "", "value": 40}}).
4. For "scatter": each "data" entry should use "x" and "y" numeric keys instead of "label"/"value", e.g. {{"x": 5, "y": 12}}.
5. For "histogram": provide already-bucketed counts as {{"label": "<bucket name>", "value": <count>}} under a single series whenever the user's data can be grouped that way.
6. Extract every label and numeric value directly from what the user provided (see DATA DETECTED above if present), or from data already gathered earlier in this conversation (e.g. a prior tool result). Never invent numbers.
7. Pick the single best chart "type" for the data's shape: comparison across categories -> bar/grouped_bar; parts of a whole -> pie/donut; trend across time/sequence -> line/area; relationship between two numeric variables -> scatter; multi-metric comparison across few entities -> radar; distribution of one variable -> histogram.
8. "color" is optional per series — omit it to let the renderer choose a default palette. If the user specifies colors, use valid hex codes.
9. Keep "title" concise (under 8 words). Omit "x_label"/"y_label" entirely (do not include empty strings) for pie/donut charts.
10. Output ONLY the [GENERATE_CHART: type] block with strictly valid JSON inside — no trailing commas, no comments, no extra text.
11. If the user's request has no usable numeric data anywhere in this conversation, do NOT fabricate a chart — instead briefly ask what data to plot, without using the [GENERATE_CHART] block.
"""

        return prompt + instruction, history


router.register(ChartGeneratorTool())