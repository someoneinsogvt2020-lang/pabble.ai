class ToolRouter:
    """
    Routes incoming user prompts through registered Tool instances.
    Each tool's `match()` method is checked; if it matches, the tool's
    `apply()` method is called to augment the prompt/history before the
    LLM sees them.
    """

    def __init__(self):
        self._tools = []

    def register(self, tool):
        """Register a Tool instance."""
        self._tools.append(tool)

    def route(self, prompt, history):
        """
        Run through all registered tools.  The *first* tool whose
        `match()` returns True gets to `apply()` its modifications.
        Returns (modified_prompt, modified_history, matched_tool_name | None).
        """
        for tool in self._tools:
            try:
                if tool.match(prompt):
                    new_prompt, new_history = tool.apply(prompt, history)
                    return new_prompt, new_history, tool.name
            except Exception as e:
                print(f"[ToolRouter] Error in tool '{tool.name}': {e}")
                continue

        # No tool matched — pass through unchanged
        return prompt, history, None


router = ToolRouter()
