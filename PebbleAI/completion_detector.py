from agent_config import COMPLETION_MARKERS, CONTINUE_MARKERS, RAM_THRESHOLD_PERCENT
import psutil

class CompletionDetector:
    @staticmethod
    def is_done(response: str, iteration: int, max_iterations: int) -> bool:
        """
        Determines whether the agent loop should stop.
        Called AFTER the LLM generates a response.
        """
        # Hard limit: iteration count (0-indexed, so use >)
        if iteration >= max_iterations - 1:
            return True

        # Hard limit: RAM
        try:
            ram_percent = psutil.virtual_memory().percent
            if ram_percent > RAM_THRESHOLD_PERCENT:
                return True
        except Exception:
            pass

        text = response.lower()

        # If the response contains a tool call, the agent should CONTINUE
        # (the tool needs to be executed and the result fed back)
        if "<tool>" in text:
            return False

        # Check completion markers (agent is signaling it's finished)
        for marker in COMPLETION_MARKERS:
            if marker.lower() in text:
                return True

        # Check continue markers (agent is signaling more work needed)
        for marker in CONTINUE_MARKERS:
            if marker.lower() in text:
                return False

        # If ambiguous -> STOP (safety first on 8GB RAM)
        return True

completion_detector = CompletionDetector()
