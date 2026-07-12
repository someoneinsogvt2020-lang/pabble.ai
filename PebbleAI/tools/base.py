class Tool:
    name = "base_tool"

    def match(self, prompt):
        """Returns True if this tool should be activated for the given prompt."""
        return False

    def apply(self, prompt, history):
        """
        Applies the tool logic.
        Returns a tuple of (modified_prompt, modified_history).
        """
        return prompt, history
