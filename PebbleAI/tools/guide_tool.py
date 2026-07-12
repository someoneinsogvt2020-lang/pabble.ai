from .base import Tool
from .router import router

class GuideTool(Tool):
    name = "guide_tool"
    KEYWORDS = [
        "what can you do", "how do you work", "explain your modes", 
        "how does this app work", "what are your capabilities",
        "tell me about yourself", "how do i use you"
    ]
    def match(self, prompt):
        return any(w in prompt.lower() for w in self.KEYWORDS)
    def apply(self, prompt, history):
        inst = """
[SYSTEM GUIDE TOOL ACTIVE]
The user is asking about your capabilities. Clearly explain how each mode and feature works.
1. **Modes**:
   - **Auto Mode**: Decides the best model and tools automatically.
   - **Gemma / Qwen / Qwen3**: Use specific local models.
   - **DeepSeek R1**: A reasoning-focused local model that thinks through problems step by step before answering.
   - **Think Hard**: For complex reasoning.
   - **Agent Mode**: Fully autonomous mode using tools (web search, files, etc.) sequentially without permission until done.
   - **Social Manager**: Interacts with connected social accounts.
2. **Capabilities**:
   - Web Search & Reading URLs
   - Reading & Writing Local Files
   - Opening Apps & URLs on Desktop
   - Generating Documents (PDF, DOCX, MD, TXT)
   - Generating Charts (Bar, Grouped Bar, Stacked Bar, Line, Area, Pie, Donut, Scatter, Radar, Histogram)
   - Taking Screenshots
Provide a well-structured markdown response.
"""
        return prompt + "\n" + inst, history

router.register(GuideTool())