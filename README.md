<div align="center">
  <h1>🪨 PebbleAI</h1>
  <p><strong>A powerful, privacy-first local AI assistant running entirely on your computer.</strong></p>

  [![Status](https://img.shields.io/badge/Status-Now%20Available-brightgreen.svg)](#)
  [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
  [![Ollama](https://img.shields.io/badge/Ollama-Supported-orange.svg)](https://ollama.com/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)
</div>

<br>

PebbleAI is a powerful, privacy-first local AI assistant that runs entirely on your computer using open-source language models through Ollama. It delivers fast responses, complete privacy, and zero API costs while giving you access to intelligent tools, web search, file management, and desktop automation.

---

# ✅ Status

**PebbleAI is now available.**

---

# ✨ Features

- 🔒 **100% Local & Private** – Your conversations and files never leave your computer.
- 🧠 **Intelligent Model Routing** – Automatically selects the best AI model for each task.
- 🛠️ **Built-in AI Tools**
  - Live web search
  - Read and write local files
  - Launch applications
  - Open websites
  - Process PDFs, DOCX files, and structured data
- 💻 **Modern Web Interface** – Clean Flask-based interface.
- ⚡ **Hardware Acceleration** – Supports NVIDIA CUDA and AMD ROCm automatically.

---

# 🚀 Prerequisites

Install the following before running PebbleAI:

1. Python **3.10+**
2. **Ollama**
   - Install Ollama.
   - Ensure the Ollama service is running before launching PebbleAI.

---

# 🛠 Installation

## Windows

```cmd
git clone https://github.com/someoneinsogvt2020-lang/pabble.ai.git
cd pabble.ai

setup.bat

python app.py
```

## Linux / macOS

```bash
git clone https://github.com/someoneinsogvt2020-lang/pabble.ai.git
cd pabble.ai

chmod +x setup.sh
./setup.sh

python3 app.py
```

---

# 📖 How to Use

## Web Interface (Recommended)

1. Start PebbleAI:

```cmd
python app.py
```

2. Open your browser.

3. Visit:

```
http://127.0.0.1:5000/
```

4. Begin chatting with PebbleAI.

You can:

- Ask questions
- Generate code
- Summarize documents
- Search the web
- Read and write local files
- Launch desktop applications

---

## Terminal Mode

Run:

```cmd
python main.py
```

Useful commands:

- `/clear` — Clear conversation history
- `/exit` — Close PebbleAI

---

# 🤖 Supported Models

PebbleAI supports the following Ollama models out of the box:

- gemma3:4b
- qwen2.5:3b
- deepseek-r1:1.5b
- qwen3:4b

Additional Ollama-compatible models can be configured.

---

# 🛡 Security & Privacy

PebbleAI runs completely on your computer.

- No cloud processing
- No API keys required
- No subscription fees
- No data leaves your device

All AI inference is performed locally through Ollama for maximum privacy and control.

---

<div align="center">

## 🪨 PebbleAI

**Private. Fast. Local.**

Built with ❤️ for local AI enthusiasts.

</div>
