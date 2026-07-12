import os

# Agent Configuration

# Primary model for agent loop
MODEL = "qwen2.5:3b"

# Conversation History Limits
MAX_HISTORY_TOKENS = 4000
# Enough messages to retain tool results and multi-turn context
MAX_MESSAGES_TO_KEEP = 16

# Agent Loop Limits
MAX_ITERATIONS = 10
RAM_THRESHOLD_PERCENT = 85

# Data Compression Limits
TOOL_RESULT_MAX_CHARS = 3000
# Phase Two (fetch_page_content) extracts real page text, so it gets a bigger budget
SEARCH_RESULT_MAX_CHARS = 6000
# Cap on extracted text per fetch_page_content call
SEARCH_PER_PAGE_MAX_CHARS = 3500

# Streaming capability
STREAMING = True

# Completion and Continuation Markers (used by completion_detector)
COMPLETION_MARKERS = [
    "Done", 
    "Done!",
    "Completed", 
    "Here's your answer",
    "Here's your result", 
    "Here is the",
    "I've completed", 
    "I have completed",
    "Finished", 
    "Task complete"
]

CONTINUE_MARKERS = [
    "Let me", 
    "I'll", 
    "I'll now",
    "I need to", 
    "I should",
    "First,", 
    "Next,", 
    "Now I'll",
    "Step",
    "<tool>"
]