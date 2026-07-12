import json
import re
import requests
import datetime
import platform

from agent_config import MODEL, MAX_ITERATIONS, STREAMING
from history_manager import history_manager
from tool_registry import tool_registry

try:
    import psutil
except ImportError:
    psutil = None

# Import the tools router for prompt pre-processing
from tools import router as tools_router

OLLAMA_URL = "http://localhost:11434/api/chat"

# Map UI modes to models
MODE_MODEL_MAP = {
    "gemma": "gemma3:4b",
    "qwen": "qwen2.5:3b",
    "auto": "qwen2.5:3b",
    "qwen_lite": "qwen2.5:3b",
    "think_hard": "qwen2.5:3b",
    "social": "qwen2.5:3b",
    "agent": "qwen2.5:3b",
    "deepseek": "deepseek-r1:1.5b",
    "qwen3": "qwen3:4b",
}

def get_system_prompt():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os_name = platform.system()
    return f"""
You are PebbleAI, a powerful local AI assistant.
IDENTITY RULES (only trigger on direct relevant questions, never volunteer this unprompted):
- ONLY if the user explicitly asks who made/created/built you or who your developer is, reply with: "I am made by Supreme Leader Daksh Pratap Singh." Do not say this in any other situation, including greetings or unrelated replies.
- ONLY if the user explicitly asks "who is Sukant", reply with this Instagram link: https://www.instagram.com/sumed_47/?utm_source=ig_web_button_share_sheet and use the open_url tool.

Current Date/Time: {now}
Operating System: {os_name}

=== TWO-PHASE RESEARCH PROTOCOL (MANDATORY) ===
You cannot see the web directly. You can only read it through tools, one step at a time. Follow these rules exactly, in order, every time research is needed:

PHASE ONE — DISCOVERY:
  1. Call web_search to find candidate URLs.
  2. web_search gives you titles, URLs, and short snippets ONLY. This is NOT enough to answer from. Do not treat snippets as full page content.

PHASE TWO — EXTRACTION (REQUIRED, do not skip):
  3. After web_search returns, you MUST immediately call fetch_page_content on the single most relevant URL from the results. Do this before writing any answer.
  4. If fetch_page_content fails or returns an error, call it again on the next most relevant URL from the same search results. Keep trying different URLs until one succeeds.
  5. Never answer, and never tell the user to "check the link themselves," using only web_search snippets. Snippets alone are not a completed research task.

PHASE THREE — ANSWER:
  6. Only after fetch_page_content has successfully returned real page text, write your final answer using that extracted text as your source of facts.
  7. Always include the source link(s) you actually read from, in markdown format.
=== END PROTOCOL ===

You have access to the following tools. Use them when needed:
  - web_search: PHASE ONE (Discovery). Search the internet for current information. Returns a list of titles, URLs, and short snippets ONLY — it does NOT give you the full page content. Arguments: {{"query": "..."}}
  - fetch_page_content: PHASE TWO (Extraction). Reads the full text of one specific URL. This is your ONLY way to actually read a page. Arguments: {{"url": "..."}}
  - image_search: Search for a large, high-resolution image (e.g. a product photo). Arguments: {{"query": "..."}}
  - read_url: Manual alternative to fetch_page_content, same behavior. Arguments: {{"url": "..."}}
  - file_read: Read content from a file on the user's computer. Arguments: {{"filepath": "..."}}
  - file_write: Write or save content to a file. Arguments: {{"filepath": "...", "content": "..."}}
  - app_launch: Launch an application by name (e.g. chrome, notepad). Arguments: {{"app_name": "..."}}
  - open_url: Open a website URL in the default browser. Arguments: {{"url": "..."}}
  - file_read: Read content from a file on the user's computer. Arguments: {{"filepath": "..."}}
  - file_write: Write or save content to a file. Arguments: {{"filepath": "...", "content": "..."}}
  - app_launch: Launch an application by name (e.g. chrome, notepad). Arguments: {{"app_name": "..."}}
  - open_url: Open a website URL in the default browser. Arguments: {{"url": "..."}}

When you need to use a tool, output EXACTLY this format:
  <tool>tool_name</tool>
  <args>{{"param": "value"}}</args>

CRITICAL RULES FOR TOOL USAGE:
  1. You MUST use web_search when the user asks about:
     - Current events, news, today's information, recent happenings
     - Sports scores, match results, game outcomes
     - Weather, stock prices, or any real-time data
     - Any person, place, or thing you are unsure about
     - Questions containing words like "latest", "current", "today", "recent", "now", "2024", "2025", "2026"
     - Who won, what happened, election results, etc.
  2. If you don't know the answer or are not 100% certain, use web_search.
  3. After web_search returns, do NOT answer yet — you MUST call fetch_page_content next (see protocol above). After any OTHER tool result, use that data to give a complete, helpful answer.
  4. When providing information from web_search, you MUST provide the source links to the user in clickable markdown format (e.g., [Source Name](URL)).
  4b. If the user asks to see, show, or display a picture/photo/image of a product or anything visual, use the image_search tool. When you get back a result containing "IMAGE_URL: <url>", you MUST display it to the user by outputting EXACTLY this block (and nothing else around the image itself):
      [SHOW_IMAGE: <url>]<short caption>[/SHOW_IMAGE]
  5. If the user asks you to "redirect" them or "open" a page, use the open_url tool to launch it in their browser.
  6. Do NOT say "I don't have access to real-time data" — you DO via web_search.
  7. Do NOT refuse to search. If in doubt, SEARCH.
  8. When your task is fully complete, provide your final answer directly.
  9. Keep responses concise and helpful. You are running on limited RAM, be efficient.

EXAMPLE of using web_search:
User: "Who won the cricket match today?"
You should respond:
<tool>web_search</tool>
<args>{{"query": "cricket match result today {now[:10]}"}}</args>
"""

_THINK_BLOCK_RE = re.compile(r"<think>.*?</think>", re.IGNORECASE | re.DOTALL)


def _strip_think_blocks(text):
    """
    Reasoning models like deepseek-r1 wrap their chain-of-thought in
    <think>...</think> before the real answer. That reasoning text can
    contain stray '<tool>' mentions or hedging phrases ("I cannot",
    "I don't know") that aren't the model's actual final output. Strip it
    before running tool-call parsing or struggle detection so we only act
    on what the model is actually saying, not what it's thinking through.
    Streaming to the user is unaffected — this is only used for parsing.
    """
    return _THINK_BLOCK_RE.sub("", text)


def parse_tool_markers(response_text):
    """Extract <tool> and <args> from the LLM response. Returns (name, args) or None."""
    tool_match = re.search(r"<tool>(.*?)</tool>", response_text, re.IGNORECASE)
    args_match = re.search(r"<args>(.*?)</args>", response_text, re.IGNORECASE | re.DOTALL)

    if tool_match:
        tool_name = tool_match.group(1).strip()
        args_dict = {}
        if args_match:
            raw = args_match.group(1).strip()
            try:
                args_dict = json.loads(raw)
            except json.JSONDecodeError:
                # Try to salvage malformed JSON from the LLM
                try:
                    # Sometimes LLM wraps in extra text; find the first { ... }
                    brace_match = re.search(r"\{.*\}", raw, re.DOTALL)
                    if brace_match:
                        args_dict = json.loads(brace_match.group(0))
                except (json.JSONDecodeError, AttributeError):
                    pass
        return tool_name, args_dict
    return None


# Keywords that strongly suggest the user needs a web search,
# even if the LLM doesn't trigger one itself
_SEARCH_HINT_KEYWORDS = [
    "who won", "what happened", "latest", "current", "today",
    "recent", "news", "score", "result", "weather",
    "stock price", "how much is", "what is the price",
    "2024", "2025", "2026", "yesterday", "this week",
    "this month", "this year", "right now", "live",
    "trending", "update", "breaking",
]


def _should_force_search(user_input):
    """Check if the user's prompt strongly implies they need a web search."""
    text = user_input.lower()
    return any(kw in text for kw in _SEARCH_HINT_KEYWORDS)

def _normalize_history(history):
    """Ensure history is a list of properly formatted message dicts."""
    if not history:
        return []
    normalized = []
    for item in history:
        if isinstance(item, dict) and "role" in item and "content" in item:
            normalized.append(item)
    return normalized


class PebbleAgent:
    def __init__(self, mode="auto"):
        self.mode = mode
        self.model = MODE_MODEL_MAP.get(mode, MODEL)
        self._escalated = False

    def generate_response(self, user_input, history=None):
        """
        Generator that yields dicts with type: token|text|system|ask_user|error|done.
        IMPORTANT: We build our own internal history and do NOT mutate the caller's list.
        """
        # --- Pre-process through tools router ---
        # This lets chart/document/desktop tools inject instructions into the prompt
        processed_input, _, matched_tool = tools_router.route(user_input, history or [])

        if matched_tool:
            print(f"[Agent] Tools router matched: {matched_tool}")

        # Build internal working history — never mutate the caller's list
        working_history = [{"role": "system", "content": get_system_prompt()}]

        # Carry over recent conversation context from the caller if available
        if history:
            for msg in _normalize_history(history):
                if msg.get("role") != "system":
                    working_history.append(msg)

        working_history.append({"role": "user", "content": processed_input})

        for iteration in range(MAX_ITERATIONS):
            trimmed_history = history_manager.trim(working_history)

            try:
                full_reply = ""
                
                payload = {
                    "model": self.model,
                    "messages": trimmed_history,
                    "stream": STREAMING
                }

                res = requests.post(OLLAMA_URL, json=payload, stream=STREAMING, timeout=300)
                res.raise_for_status()

                if STREAMING:
                    for line in res.iter_lines():
                        if line:
                            try:
                                chunk = json.loads(line)
                            except (json.JSONDecodeError, ValueError):
                                continue
                            token = chunk.get("message", {}).get("content", "")
                            if token:
                                full_reply += token
                                yield {"type": "token", "content": token}
                            if chunk.get("done"):
                                break
                else:
                    data = res.json()
                    full_reply = data.get("message", {}).get("content", "")
                    yield {"type": "text", "content": full_reply}

                working_history.append({"role": "assistant", "content": full_reply})

                # Strip <think>...</think> reasoning (e.g. deepseek-r1) before
                # parsing — we only want to act on the model's actual output.
                parsed_reply = _strip_think_blocks(full_reply)

                # Check if the LLM wants to call a tool
                tool_call = parse_tool_markers(parsed_reply)
                
                # Check if the LLM struggled (only in auto mode)
                failure_phrases = ["i cannot", "i am unable", "i don't know", "i can't help", "i'm sorry, but i can't"]
                struggling = any(phrase in parsed_reply.lower() for phrase in failure_phrases)

                # If the LLM refused but the query looks like it needs search, force a search
                if tool_call is None and struggling and _should_force_search(user_input):
                    tool_call = ("web_search", {"query": user_input})
                    yield {"type": "system", "content": "\n[Auto-searching the web for you...]"}
                
                # Escalate model if struggling and haven't escalated yet
                if self.mode == "auto" and struggling and not self._escalated:
                    if not tool_call and iteration > 0:
                        yield {"type": "system", "content": "\n\n*Switching to a stronger model for a better answer…*\n\n"}
                        self.model = MODE_MODEL_MAP["think_hard"]
                        self._escalated = True
                        # Continue the loop with the new model instead of recursing
                        continue

                if tool_call is None:
                    # No tool call — this is a final answer, stop the loop
                    break
                else:
                    tool_name, args = tool_call
                    yield {"type": "system", "content": f"\n[Executing tool: {tool_name}]"}

                    raw_result = tool_registry.execute(tool_name, args)

                    yield {"type": "system", "content": f"\n[Tool result received]"}

                    if "Error" in raw_result or "Failed" in raw_result or "not found" in raw_result:
                        if tool_name == "fetch_page_content" or tool_name == "read_url":
                            feedback_prompt = f"fetch_page_content failed on that URL:\n\n{raw_result}\n\nCall fetch_page_content again, but use a DIFFERENT URL from the web_search results above. Do not give up after one failed attempt — try the next most relevant URL."
                        else:
                            feedback_prompt = f"The tool '{tool_name}' failed with this result:\n\n{raw_result}\n\nPlease try a DIFFERENT approach or a DIFFERENT tool. Do not repeat the exact same tool call."
                    elif tool_name == "web_search":
                        # Enforcement step — Phase One complete, force the model into Phase Two.
                        # Do NOT let it answer from snippets alone.
                        feedback_prompt = f"web_search results (Phase One — titles, URLs, and snippets only, NOT full content):\n\n{raw_result}\n\nYou must now call fetch_page_content on the single most relevant URL above to read its actual content before answering. Do not answer yet. Output the fetch_page_content tool call now."
                    else:
                        if self.mode == "agent":
                            feedback_prompt = f"Tool '{tool_name}' returned the following data:\n\n{raw_result}\n\nYou are in autonomous agent mode. Do work, do not ask the user for permission. Process this data and immediately call the next necessary tool to complete the user's task. If the task is fully complete, provide a final response."
                        else:
                            feedback_prompt = f"Tool '{tool_name}' returned the following data:\n\n{raw_result}\n\nUse this data to give a complete, helpful answer to the user's original question. Present the information clearly. Do NOT call any more tools unless absolutely necessary."

                    # Feed tool result back to the LLM for the next iteration
                    working_history.append({
                        "role": "user",
                        "content": feedback_prompt
                    })
                    # Continue the loop — the LLM will process the tool result

            except requests.exceptions.ConnectionError:
                yield {"type": "error", "content": "Could not connect to Ollama. Make sure Ollama is running on localhost:11434."}
                break
            except requests.exceptions.Timeout:
                yield {"type": "system", "content": "\n[Model is taking longer than usual — still working...]"}
                continue
            except Exception as e:
                yield {"type": "error", "content": f"Agent error: {e}"}
                break

        # Persist the final exchange back to the caller's history
        if history is not None:
            history.append({"role": "user", "content": user_input})
            # Find the last assistant message from our working history
            for msg in reversed(working_history):
                if msg.get("role") == "assistant":
                    history.append(msg)
                    break

        yield {"type": "done", "content": ""}