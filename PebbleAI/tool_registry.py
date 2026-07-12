import json
import os
import re
import subprocess
import requests
import socket
import urllib.parse as urlparse
from bs4 import BeautifulSoup
from agent_config import TOOL_RESULT_MAX_CHARS, SEARCH_RESULT_MAX_CHARS, SEARCH_PER_PAGE_MAX_CHARS

def is_online():
    try:
        requests.head("https://www.google.com", timeout=3)
        return True
    except Exception:
        return False

def compress(text, max_chars=TOOL_RESULT_MAX_CHARS):
    if not text:
        return ""
    text = str(text).strip()
    if len(text) > max_chars:
        return text[:max_chars] + "..."
    return text

_UA_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def _fetch_page_text(url, max_chars=None, max_download=500 * 1024, timeout=12):
    """
    Fetches a URL and returns clean, readable body text (scripts/styles/nav
    stripped). Shared by fn_web_search (auto-fetch) and fn_read_url (manual
    fetch). Returns None on any failure so callers can fall back gracefully.
    """
    try:
        res = requests.get(url, headers=_UA_HEADERS, timeout=timeout, stream=True)
        res.raise_for_status()
        content_parts = []
        downloaded = 0
        for chunk in res.iter_content(chunk_size=8192, decode_unicode=True):
            if chunk:
                content_parts.append(chunk if isinstance(chunk, str) else chunk.decode("utf-8", errors="ignore"))
                downloaded += len(chunk)
                if downloaded > max_download:
                    break
        raw_html = "".join(content_parts)
        soup = BeautifulSoup(raw_html, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "aside", "header", "form", "svg"]):
            tag.extract()

        text = soup.get_text(separator=' ')
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        # Neutralize potential run action injection (Fix 3)
        text = re.sub(r'\[\s*RUN_ACTION\s*:[^\]]*\]', '[ACTION_REDACTED]', text, flags=re.IGNORECASE)

        if max_chars and len(text) > max_chars:
            text = text[:max_chars] + "..."
        return text if text else None
    except Exception:
        return None


def fn_web_search(args):
    """
    PHASE ONE — Discovery only. Returns titles, URLs, and short snippets so
    the model can identify the most relevant source(s). Does NOT fetch full
    page content — that is the explicit job of fetch_page_content (Phase Two).
    """
    if not is_online():
        return "Internet connection is required."
    query = args.get("query", "")
    if not query:
        return "No query provided."
    try:
        from urllib.parse import quote_plus
        import time
        encoded_query = quote_plus(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        
        max_retries = 3
        output = ""
        last_error = None
        
        for attempt in range(max_retries):
            try:
                res = requests.get(url, headers=_UA_HEADERS, timeout=15)
                res.raise_for_status()
                
                # Check for CAPTCHA/blocking page
                lower_html = res.text.lower()
                if "captcha" in lower_html or "verify you are a human" in lower_html or "security check" in lower_html:
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    return "Search provider blocked the request (CAPTCHA/Rate Limit). Please try again later."
                
                soup = BeautifulSoup(res.text, "html.parser")
                
                # Primary Selector
                results = soup.find_all("div", class_="result", limit=5)
                
                # Fallback Selectors
                if not results:
                    results = soup.find_all("div", class_="links_main", limit=5)
                if not results:
                    results = soup.find_all("table", class_="result-snippet", limit=5)

                if not results:
                    # Still no results, might be a soft block or actual zero results
                    if "no results" in lower_html:
                        return "No results found for your query."
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    return "Could not parse search results. The page layout may have changed."

                for result in results:
                    # Try primary inner selectors
                    title_tag = result.find("a", class_="result__a")
                    snippet_tag = result.find("a", class_="result__snippet")
                    
                    # Fallback inner selectors
                    if not title_tag:
                        links = result.find_all("a")
                        title_tag = next((a for a in links if a.text.strip()), None)
                    if not snippet_tag:
                        snippet_tag = result.find("div", class_="result__snippet") or result.find("div", class_="snippet")
                        
                    if not title_tag:
                        continue
                        
                    title = title_tag.text.strip()
                    snippet = snippet_tag.text.strip() if snippet_tag else ""
                    raw_url = title_tag.get('href', '')
                    
                    if not raw_url:
                        continue
                        
                    parsed = urlparse.urlparse(raw_url)
                    qsl = urlparse.parse_qs(parsed.query)
                    actual_url = qsl['uddg'][0] if 'uddg' in qsl else raw_url
                    
                    if not actual_url.startswith("http"):
                        continue
                        
                    output += f"{title}\nURL: {actual_url}\n{snippet}\n\n"
                    
                if output:
                    break
                else:
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                    
        if not output:
            if last_error:
                return f"Web search failed: {last_error}"
            return "No results found."
            
        return output
    except Exception as e:
        return f"Web search failed: {e}"


def fn_fetch_page_content(args):
    """
    PHASE TWO — Extraction. Fetches and returns the real, cleaned body text
    of a specific URL (normally one surfaced by a prior web_search call).
    This is the model's sole mechanism for actually reading a page.
    """
    if not is_online():
        return "Internet connection is required."
    url = args.get("url", "")
    if not url:
        return "No URL provided."
    text = _fetch_page_text(url, max_chars=SEARCH_PER_PAGE_MAX_CHARS)
    if text is None:
        return f"Failed to extract content from {url}. Try the next most relevant URL from the search results."
    return text


def fn_image_search(args):
    if not is_online():
        return "Internet connection is required."
    query = args.get("query", "")
    if not query:
        return "No query provided."
    try:
        from urllib.parse import quote_plus
        # Step 1: get a vqd token (required by DDG's image endpoint)
        token_res = requests.get(
            f"https://duckduckgo.com/?q={quote_plus(query)}&iax=images&ia=images",
            headers=_UA_HEADERS, timeout=15
        )
        vqd_match = re.search(r"vqd=['\"]?([\d-]+)", token_res.text)
        if not vqd_match:
            return "No image results found."
        vqd = vqd_match.group(1)

        img_res = requests.get(
            "https://duckduckgo.com/i.js",
            params={"q": query, "vqd": vqd, "o": "json"},
            headers=_UA_HEADERS, timeout=15
        )
        img_res.raise_for_status()
        data = img_res.json()
        results = data.get("results", [])
        if not results:
            return "No image results found."

        # Pick the largest available image (by reported width*height) for a "massive" product shot
        best = max(results, key=lambda r: r.get("width", 0) * r.get("height", 0))
        image_url = best.get("image") or best.get("thumbnail")
        title = best.get("title", query)
        if not image_url:
            return "No image results found."
        return f"IMAGE_URL: {image_url}\nTITLE: {title}"
    except Exception as e:
        return f"Image search failed: {e}"

def fn_read_url(args):
    if not is_online():
        return "Internet connection is required."
    url = args.get("url", "")
    if not url:
        return "No URL provided."
    text = _fetch_page_text(url)
    if text is None:
        return f"Failed to read URL content. Provide the link directly to the user."
    return text

def fn_file_read(args):
    filepath = args.get("filepath", "")
    if not filepath:
        return "No filepath provided."
    try:
        path = os.path.expanduser(filepath)
        if not os.path.exists(path):
            return f"File not found: {filepath}"
        if not os.path.isfile(path):
            return f"Not a file: {filepath}"
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"File read failed: {e}"

def fn_file_write(args):
    filepath = args.get("filepath", "")
    content = args.get("content", "")
    if not filepath:
        return "No filepath provided."
    try:
        path = os.path.expanduser(filepath)
        parent = os.path.dirname(os.path.abspath(path))
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Saved to: {filepath}"
    except Exception as e:
        return f"File write failed: {e}"

def fn_app_launch(args):
    app_name = args.get("app_name", "")
    if not app_name:
        return "No app name provided."
    try:
        import platform
        if platform.system() == "Windows":
            subprocess.Popen(f'start "" "{app_name}"', shell=True)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", "-a", app_name])
        else:
            subprocess.Popen([app_name], shell=True)
        return f"Launched: {app_name}"
    except Exception as e:
        return f"App launch failed: {e}"

def fn_open_url(args):
    if not is_online():
        return "Internet connection is required."
    url = args.get("url", "")
    if not url:
        return "No URL provided."
    try:
        import webbrowser
        webbrowser.open(url)
        return f"Opened in browser: {url}"
    except Exception as e:
        return f"Open URL failed: {e}"


class ToolRegistry:
    def __init__(self):
        self.TOOLS = {
            "web_search": {
                "description": "Phase One (Discovery): search the web via DuckDuckGo for titles, URLs, and short snippets. Does not read full pages.",
                "params": ["query"],
                "execute": fn_web_search,
                "ram_cost": "low"
            },
            "fetch_page_content": {
                "description": "Phase Two (Extraction): fetch and read the full text of a specific URL. Mandatory follow-up after web_search before answering.",
                "params": ["url"],
                "execute": fn_fetch_page_content,
                "max_chars": SEARCH_RESULT_MAX_CHARS,
                "ram_cost": "medium"
            },
            "image_search": {
                "description": "Search for a large, high-resolution image (e.g. product photo) and return its direct URL",
                "params": ["query"],
                "execute": fn_image_search,
                "ram_cost": "low"
            },
            "read_url": {
                "description": "Read the main text content of a webpage URL. Use this to read the links returned by web_search.",
                "params": ["url"],
                "execute": fn_read_url,
                "ram_cost": "low"
            },
            "file_read": {
                "description": "Read a file from disk",
                "params": ["filepath"],
                "execute": fn_file_read,
                "ram_cost": "low"
            },
            "file_write": {
                "description": "Write content to a file",
                "params": ["filepath", "content"],
                "execute": fn_file_write,
                "ram_cost": "low"
            },
            "app_launch": {
                "description": "Launch an application (e.g., notepad, chrome, calc)",
                "params": ["app_name"],
                "execute": fn_app_launch,
                "ram_cost": "low"
            },
            "open_url": {
                "description": "Open a website URL in the default browser",
                "params": ["url"],
                "execute": fn_open_url,
                "ram_cost": "low"
            }
        }

    def execute(self, tool_name, args):
        tool_name = tool_name.strip().lower()
        tool = self.TOOLS.get(tool_name)
        if not tool:
            return compress(f"Error: Tool '{tool_name}' not found. Available: {', '.join(self.TOOLS.keys())}")

        try:
            raw_result = tool["execute"](args)
            return compress(raw_result, max_chars=tool.get("max_chars", TOOL_RESULT_MAX_CHARS))
        except Exception as e:
            return compress(f"Error executing {tool_name}: {e}")

tool_registry = ToolRegistry()