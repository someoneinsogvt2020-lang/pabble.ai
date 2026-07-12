from .base import Tool
from .router import router

_SOCIAL_KEYWORDS = [
    "instagram", "insta", "facebook", "twitter", "x.com",
    "social media", "manage my social", "read my feed",
    "check instagram", "check facebook", "open insta",
]


class SocialManagerTool(Tool):
    name = "social_manager"

    def match(self, prompt):
        text = prompt.lower()
        return any(kw in text for kw in _SOCIAL_KEYWORDS)

    def apply(self, prompt, history):
        instruction = """

[SYSTEM SOCIAL MANAGER ACTIVE]

The user wants to manage or check their social media (like Instagram). 
Since background automated logins are frequently blocked and unsafe for user accounts, we use a safer approach: we open the site in their regular browser.

You must respond by using the Desktop Action tool format to manage the social media.

Example if they say "check my instagram":
[RUN_ACTION: social_manage | https://www.instagram.com]

This action will:
1. Open the URL in the user's default browser (using their existing login).
2. Wait 4 seconds for the feed to load.
3. Take a screenshot of the feed and save it to the Desktop.

Once the screenshot is saved, you can use the file_read tool (or ask the user if they want you to read it) to tell them what's going on!
"""
        return prompt + instruction, history


router.register(SocialManagerTool())
