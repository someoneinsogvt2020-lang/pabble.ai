# PebbleAI

**A locally-run AI assistant with agentic tool use — no cloud, no API keys, no data leaving your machine.**

PebbleAI runs entirely on your own computer using [Ollama](https://ollama.com/) to serve local language models. It combines a Flask web interface with an agent loop that can search the web, read pages, work with files, and launch apps on your behalf — all without sending your data to a third party.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Install (Windows)](#quick-install-windows)
- [Step-by-Step Installation](#step-by-step-installation)
- [Running PebbleAI](#running-pebbleai)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [System Requirements](#system-requirements)
- [License](#license)

---

## Features

- **Fully local inference** — powered by Ollama; nothing is sent to an external API.
- **Multi-model support** — ships configured for `qwen2.5:3b`, `gemma3:4b`, `deepseek-r1:1.5b`, and `qwen3:4b`.
- **Agentic tool use**, including:
  - Web search
  - Page content fetching
  - Image search
  - URL reading
  - File read/write
  - Local application launching
- **Conversation memory** across sessions, with manual clear/inspect commands.
- **Web-based chat interface** served locally via Flask (`http://127.0.0.1:5000/`).

---

## Prerequisites

Install these three things before proceeding:

| Requirement | Where to get it | Notes |
|---|---|---|
| **Python 3.10+** | [python.org/downloads](https://www.python.org/downloads/) | Check **"Add Python to PATH"** during install |
| **Ollama** | [ollama.com](https://ollama.com/) | Must be running in the background (check your system tray) |
| **Git** | [git-scm.com/downloads](https://git-scm.com/downloads) | Needed to clone the repository |

---

## Quick Install (Windows)

Open **Command Prompt** and paste this entire block:

```cmd
git clone https://github.com/someoneinsogvt2020-lang/pabble.ai.git
cd pabble.ai\PebbleAI
setup.bat
python app.py
```

Then open your browser to:

```
http://127.0.0.1:5000/
```

`setup.bat` handles two things for you automatically: installing everything in `requirements.txt`, and pulling the four required Ollama models. If you'd rather see every step spelled out instead of running the script, use this fully manual version — it does exactly the same thing, just explicitly:

```cmd
git clone https://github.com/someoneinsogvt2020-lang/pabble.ai.git
cd pabble.ai\PebbleAI
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama pull gemma3:4b
ollama pull deepseek-r1:1.5b
ollama pull qwen3:4b
python app.py
```

That's it either way. The sections below explain what each step does, in case anything goes wrong.

---

## Step-by-Step Installation

### 1. Clone the repository

```cmd
git clone https://github.com/someoneinsogvt2020-lang/pabble.ai.git
```

### 2. Move into the project folder

```cmd
cd pabble.ai\PebbleAI
```

### 3. Run setup

```cmd
setup.bat
```

This installs all Python dependencies from `requirements.txt` and pulls the four Ollama models PebbleAI needs. **This downloads several GB of model data** — the time this takes depends entirely on your internet connection, so let it run to completion without closing the window.

### 4. Launch the app

```cmd
python app.py
```

### 5. Open it in your browser

Navigate to `http://127.0.0.1:5000/` — the terminal will also print this URL once the server starts.

---

## Project Structure

```
PebbleAI/
├── app.py                  # Flask web server / main entry point
├── main.py                 # CLI entry point (terminal-based interaction)
├── agent.py                 # Core agent loop
├── agent_config.py          # Model, history, and iteration settings
├── ai.py                    # Model inference wrapper
├── memory.py / memory.txt   # Persistent conversation memory
├── history_manager.py       # Conversation history handling
├── tool_registry.py         # Web search, file I/O, app launch, etc.
├── completion_detector.py   # Detects when an agent task is finished
├── templates/                # Frontend HTML
├── tools/                    # Individual tool implementations
├── requirements.txt
├── setup.bat                 # Windows setup script
└── setup.sh                  # Linux/macOS setup script
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `'python' is not recognized` | Python wasn't added to PATH — reinstall Python and check that box, or try `py app.py` instead |
| `ollama pull` fails or hangs | Confirm the Ollama app is actually running (check system tray) before running `setup.bat` |
| `pip install` errors during setup | Run `python -m pip install --upgrade pip`, then re-run `setup.bat` |
| Port 5000 already in use | Close whatever else is using that port, or change the port in `app.py` |
| Setup seems frozen on model downloads | It's likely still downloading — model pulls are several GB each and show minimal progress output |

---

## System Requirements

- Python 3.10+
- ~8GB free disk space (for local models)
- 8GB+ RAM recommended
- No dedicated GPU required

---

## License

*(Add your license here — e.g. MIT, Apache 2.0, or "All rights reserved" if proprietary under GlobalAI Private Limited.)*

