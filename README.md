<div align="center">
  <h1>🪨 PebbleAI</h1>
  <p><strong>A powerful, privacy-first local AI assistant running entirely on your computer.</strong></p>

  [![Status](https://img.shields.io/badge/Status-Now%20Available-brightgreen.svg)](#)
  [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
  [![Ollama](https://img.shields.io/badge/Ollama-Supported-orange.svg)](https://ollama.com/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)
</div>

<br>

PebbleAI is a powerful local AI assistant that runs entirely on your computer using open-source language models through Ollama. It delivers fast responses, complete privacy, and zero API costs while giving you access to intelligent tools, web search, file management, and desktop automation—all without sending your data to the cloud.

## ✅ Status

**PebbleAI is now available.**

## ✨ Features

- 🔒 **100% Local & Private** – Your conversations and files never leave your computer.
- 🧠 **Intelligent Model Routing** – Automatically chooses the best model for each task.
- 🛠️ **Built-in AI Tools**
  - Live web search
  - Read and write local files
  - Launch applications and open websites
  - Process PDFs, Word documents, and data files
- 💻 **Modern Web Interface** – Clean, responsive Flask-based UI.
- ⚡ **Hardware Acceleration** – Automatically uses NVIDIA CUDA or AMD ROCm when available.

---

# 🚀 Prerequisites

Before installing PebbleAI, install:

1. **Python 3.10 or newer**
2. **Ollama**
   - Install Ollama.
   - Make sure the Ollama service is running before launching PebbleAI.

---

# 🛠 Installation

## Windows

```cmd
git clone https://github.com/your-username/PebbleAI.git
cd PebbleAI

setup.bat

python app.py
```

## Linux / macOS

```bash
git clone https://github.com/your-username/PebbleAI.git
cd PebbleAI

chmod +x setup.sh
./setup.sh

python3 app.py
```

---

# 📖 How to Use

### Web Interface (Recommended)

1. Launch PebbleAI:

```cmd
python app.py
```

2. Open your browser.

3. Visit:

```
http://127.0.0.1:5000/
```

4. Start chatting with PebbleAI.

5. Ask questions, generate code, summarize documents, search the web, or use any of its built-in AI tools.

---

### Terminal Mode

If you prefer using the terminal:

```cmd
python main.py
```

Type your prompt and press **Enter**.

Useful commands:

- `/clear` — Clear conversation history
- `/exit` — Quit PebbleAI

---

# 🤖 Supported Models

PebbleAI works with multiple Ollama models, including:

- gemma3:4b
- qwen2.5:3b
- deepseek-r1:1.5b
- qwen3:4b

Additional Ollama-compatible models can also be configured.

---

# 🛡 Security & Privacy

PebbleAI runs entirely on your computer.

- No cloud processing
- No API keys required
- No subscription fees
- No conversation data sent to external servers

All AI inference is performed locally through Ollama, ensuring maximum privacy and control over your data.

---

<div align="center">
  <b>🪨 PebbleAI — Private. Fast. Local.</b>

  <br><br>

  <i>Built with ❤️ for local AI enthusiasts.</i>
</div>
