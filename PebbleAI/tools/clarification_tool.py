from .base import Tool
from .router import router

class ClarificationTool(Tool):
    name = "clarifier"

    def match(self, prompt):
        text = prompt.lower()
        triggers = ["search for", "make a story", "write a story", "presentation", "generate a document"]
        return any(t in text for t in triggers)

    def apply(self, prompt, history):
        inst = """
[SYSTEM CLARIFICATION ACTIVE]
The user wants you to do a search, write a story, or make a presentation.
Before proceeding, if you need more details to provide a perfect result, you can ask them Multiple Choice Questions (MCQs).
If you decide to ask questions, you MUST output ONLY the following format and nothing else:

[MCQ]
Question: <your question here>
Options: <Option 1>, <Option 2>, <Option 3>
Question: <your second question>
Options: <Option 1>, <Option 2>
[/MCQ]

If you already have enough information, just proceed normally without asking anything.
"""
        return prompt + "\n" + inst, history

router.register(ClarificationTool())
