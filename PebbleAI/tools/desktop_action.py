from .base import Tool
from .router import router

_ACTION_KEYWORDS = {
    "open_app": [
        "open app", "launch app", "start app", "run app",
        "open notepad", "open chrome", "open firefox", "open calculator",
        "open calc", "open browser", "open spotify", "open vlc",
        "open word", "open excel", "open powerpoint", "open vscode",
        "open code", "open terminal", "open cmd", "open powershell",
        "launch notepad", "launch chrome", "launch browser",
        "start notepad", "start chrome",
    ],
    "open_url": [
        "open url", "go to website", "open website", "visit website",
        "browse to", "navigate to", "open the link", "open this link",
        "open http", "open https", "open www",
        "redirect", "redirect to", "take me to",
    ],
    "screenshot": [
        "screenshot", "screen shot", "capture screen", "take a screenshot",
        "snap screen", "screen capture", "grab screen",
    ],
    "create_file": [
        "create file", "create a file", "make a file", "write a file",
        "save a file", "new file", "create text file",
    ],
    "notify": [
        "notify me", "send notification", "notification", "remind me",
        "alert me", "show notification", "desktop notification",
    ],
}


class DesktopActionTool(Tool):
    name = "desktop_action"

    def match(self, prompt):
        text = prompt.lower()
        for _action_type, keywords in _ACTION_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                return True
        return False

    def _detect_action(self, prompt):
        """Return the most likely action type for the prompt."""
        text = prompt.lower()
        for action_type, keywords in _ACTION_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                return action_type
        return None

    def apply(self, prompt, history):
        action = self._detect_action(prompt)
        if not action:
            return prompt, history

        instruction = f"""

[SYSTEM DESKTOP ACTION TOOL]

The user wants to perform a desktop action. Detect what they want and respond with EXACTLY this format:

[RUN_ACTION: {action} | parameter1 | parameter2]

Action types and their parameters:
- open_app: [RUN_ACTION: open_app | app_name]
- open_url: [RUN_ACTION: open_url | url]
- screenshot: [RUN_ACTION: screenshot]
- create_file: [RUN_ACTION: create_file | filepath | content]
- notify: [RUN_ACTION: notify | title | message]

Rules:
1. Output the action tag FIRST, then a brief confirmation sentence.
2. Use the correct action type.
3. Fill in the parameters from the user's request.
"""
        return prompt + instruction, history


router.register(DesktopActionTool())
