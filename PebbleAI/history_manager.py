from agent_config import MAX_HISTORY_TOKENS, MAX_MESSAGES_TO_KEEP

class HistoryManager:
    @staticmethod
    def trim(history: list) -> list:
        """
        Returns a NEW trimmed list (never mutates the original).
        Keeps: system prompt(s), the first user message, and the most recent messages
        within the token budget.
        """
        if not history:
            return []

        # Work on a copy so we never mutate the caller's list
        history = list(history)

        system_msgs = [m for m in history if m.get("role") == "system"]
        other_msgs = [m for m in history if m.get("role") != "system"]

        # Preserve the original user request (first non-system message)
        first_user = None
        if other_msgs and other_msgs[0].get("role") == "user":
            first_user = other_msgs[0]
            other_msgs = other_msgs[1:]

        # Keep only the most recent messages
        if len(other_msgs) > MAX_MESSAGES_TO_KEEP:
            trimmed_others = other_msgs[-MAX_MESSAGES_TO_KEEP:]
        else:
            trimmed_others = list(other_msgs)

        # Simple token estimator: ~1 token per 4 chars
        def estimate_tokens(msgs):
            return sum(len(m.get("content", "") if m else "") for m in msgs) // 4

        # Build the candidate list for token counting
        anchor_msgs = list(system_msgs)
        if first_user:
            anchor_msgs.append(first_user)

        # Trim oldest messages until we fit within token budget
        while trimmed_others and estimate_tokens(anchor_msgs + trimmed_others) > MAX_HISTORY_TOKENS:
            trimmed_others.pop(0)

        final_history = list(anchor_msgs)
        final_history.extend(trimmed_others)

        return final_history

history_manager = HistoryManager()
