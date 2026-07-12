from .base import Tool
from .router import router

_DOC_KEYWORDS = [
    # File types
    "pdf", "docx", "doc", "word document",
    # Document types
    "document", "report", "resume", "cv", "curriculum vitae",
    "cover letter", "letter", "essay", "article", "memo",
    "proposal", "summary report", "case study", "whitepaper", "white paper",
    "markdown", "md", "txt", "text file", "outline", "agenda",
    "invoice", "contract", "policy document",
    # Action phrases
    "write a report", "write a document", "write a letter",
    "write an essay", "write a memo", "write an article",
    "write a proposal", "write a resume", "write a cv",
    "create a report", "create a document", "create a letter",
    "generate a report", "generate a document",
    "make a pdf", "make a document", "make a report",
    "save as pdf", "save as docx", "save as document",
    "download as pdf", "download as document",
    "draft a", "compose a",
]

# Phrases that mention doc keywords but are NOT document generation requests
_DOC_EXCLUSIONS = [
    "what is a pdf", "what is pdf", "explain pdf",
    "how to open", "how to read", "upload",
    "what is markdown", "what is a document",
    "what does md mean",
]

# Lightweight signals for output length, used to size the generated document
# instead of always producing the same length regardless of what's asked.
_LENGTH_HINTS = {
    "short": ["short", "brief", "quick", "one page", "1 page", "concise", "summary"],
    "long": ["detailed", "in-depth", "in depth", "comprehensive", "thorough", "long", "extensive"],
}

# Document "shapes" that benefit from a specific structural template rather
# than generic prose, so the LLM doesn't write a resume as if it were an essay.
_DOC_TEMPLATES = {
    "resume": (
        "Use a resume structure: Name & contact line, then sections for "
        "Summary, Experience (role, company, dates, 2-4 bullet achievements each), "
        "Education, and Skills. Use concise bullet points, not paragraphs."
    ),
    "cv": (
        "Use a resume structure: Name & contact line, then sections for "
        "Summary, Experience (role, company, dates, 2-4 bullet achievements each), "
        "Education, and Skills. Use concise bullet points, not paragraphs."
    ),
    "cover letter": (
        "Use a formal letter structure: date, greeting, 3-4 short paragraphs "
        "(opening hook, relevant experience, why this role/company, closing call to action), "
        "and a sign-off."
    ),
    "report": (
        "Use a report structure: Title, Executive Summary, then 3-6 clearly headed "
        "sections covering the body, and a closing Conclusion/Recommendations section. "
        "Use a markdown table wherever the content involves comparable rows of data."
    ),
    "proposal": (
        "Use a proposal structure: Title, Overview/Problem Statement, Proposed Solution, "
        "Scope or Deliverables (as a bulleted or tabular list), Timeline, and "
        "Pricing/Next Steps if relevant."
    ),
    "memo": (
        "Use a memo structure: a header block (To / From / Date / Re), then short, "
        "direct paragraphs or bullets making the point — no unnecessary preamble."
    ),
    "case study": (
        "Use a case-study structure: Title, Background/Challenge, Approach/Solution, "
        "Results (with a markdown table of metrics if numbers are involved), and Takeaways."
    ),
    "invoice": (
        "Use an invoice structure: header with invoice number/date, billed-to block, "
        "a markdown table of line items (description, quantity, unit price, total), "
        "and a grand total."
    ),
    "agenda": (
        "Use an agenda structure: meeting title, date/time, then a numbered list of "
        "topics each with an owner and allotted time."
    ),
    "essay": (
        "Use an essay structure: a clear thesis in the opening paragraph, 3-5 body "
        "paragraphs each developing one supporting point, and a concluding paragraph."
    ),
}


class DocumentGeneratorTool(Tool):
    name = "document_generator"

    def match(self, prompt):
        text = prompt.lower()

        # Don't match if it's a question about document formats
        if any(excl in text for excl in _DOC_EXCLUSIONS):
            return False

        return any(word in text for word in _DOC_KEYWORDS)

    def _detect_doc_type(self, text):
        if "pdf" in text:
            return "pdf"
        if "docx" in text or "doc" in text or "word" in text:
            return "docx"
        if "markdown" in text or " md " in text or text.endswith(" md"):
            return "md"
        return "md"

    def _detect_template(self, text):
        # Longest-keyword-first so "cover letter" wins over the bare "letter".
        for key in sorted(_DOC_TEMPLATES, key=len, reverse=True):
            if key in text:
                return _DOC_TEMPLATES[key]
        return None

    def _detect_length(self, text):
        for level, hints in _LENGTH_HINTS.items():
            if any(h in text for h in hints):
                return level
        return "medium"

    def apply(self, prompt, history):
        text = prompt.lower()
        doc_type = self._detect_doc_type(text)
        template = self._detect_template(text)
        length = self._detect_length(text)

        length_guidance = {
            "short": "Keep it tight — roughly half a page. Prioritize the most essential points only.",
            "medium": "Aim for a normal, complete document — typically 1-2 pages worth of content.",
            "long": "Go in-depth — cover the topic thoroughly across multiple well-developed sections.",
        }[length]

        template_block = f"\nSTRUCTURE TO FOLLOW:\n{template}\n" if template else ""

        instruction = f"""

[SYSTEM DOCUMENT TOOL ACTIVE]

The user wants a downloadable document. You MUST respond ONLY with a document block in this EXACT format:

[GENERATE_DOC: {doc_type}]
Full document content goes here, written in Markdown (headings with #/##, bullet/numbered lists, and
pipe-style markdown tables where the content is naturally tabular).
[/GENERATE_DOC]

Supported types: pdf, docx, txt, md
{template_block}
LENGTH: {length_guidance}

STRICT RULES:
1. Output ONLY the [GENERATE_DOC: type] block. Do NOT write any text before or after it, and do NOT wrap it in code fences.
2. Put the ENTIRE document content between the tags, written in clean Markdown — proper heading levels, bullet/numbered lists, and tables where appropriate.
3. Use real facts and figures only from what the user provided or from information already established earlier in this conversation (e.g. a prior web search or tool result). Never fabricate statistics, dates, names, or sources.
4. If the user's request is missing information essential to a good result (e.g. a resume with no work history, a report with no subject matter) and a [SYSTEM CLARIFICATION ACTIVE] block has NOT already been triggered, make reasonable, clearly-labeled placeholder assumptions (e.g. "[Your Company Name]") rather than refusing.
5. Match tone to document type: formal and precise for reports/proposals/contracts/cover letters, plain and direct for memos, polished and achievement-focused for resumes.
6. Do not pad the document with generic filler to hit a length target — every paragraph or bullet should carry real content.
"""

        return prompt + instruction, history


router.register(DocumentGeneratorTool())