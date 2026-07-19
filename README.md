<div align="center">
  <h1>🪨 PebbleAI</h1>
  <p><strong>A powerful, privacy-first local AI assistant running entirely on your computer.</strong></p>

  [![Status](https://img.shields.io/badge/Status-Now%20Available-brightgreen.svg)](#)
  [![Version](https://img.shields.io/badge/Version-v0.1.0-blue.svg)](#)
  [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
  [![Ollama](https://img.shields.io/badge/Ollama-Supported-orange.svg)](https://ollama.com/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)
</div>

<br>

PebbleAI is a powerful privacy-first local AI assistant that runs entirely on your computer using open-source language models through Ollama.

It provides intelligent conversations, AI tools, local file processing, web search capabilities, and desktop automation while keeping your data private.

**No cloud dependency. No API costs. Everything runs locally.**

---

# ✅ Status

**PebbleAI v0.1.0 — First Public Test Build**

PebbleAI is now available for testing.

---

# ✨ Features

- 🔒 **100% Local & Private**
  - Your conversations and files stay on your computer.
  - No external servers required.

- 🧠 **Intelligent Model Support**
  - Works with open-source models through Ollama.
  - Supports multiple AI models for different tasks.

- 🛠️ **AI Agent Tools**
  - Web search.
  - Read and write local files.
  - Desktop automation.
  - Launch applications.
  - Process documents.

- 💻 **Web Interface**
  - Clean browser-based chat interface.
  - Powered by Flask.

- ⚡ **Hardware Acceleration**
  - Supports NVIDIA CUDA.
  - Supports AMD ROCm.

---

# 🚀 Prerequisites

Before installing PebbleAI, install:

### 1. Python 3.10+

Make sure Python is installed and added to your system PATH.

Check:

```cmd
python --version
```

### 2. Ollama

Install Ollama and ensure the Ollama service is running.

---

# 🛠 Installation & Setup

## Windows

### 1. Clone the repository

```cmd
git clone https://github.com/someoneinsogvt2020-lang/pabble.ai.git
```

### 2. Enter the project folder

```cmd
cd pabble.ai
cd PebbleAI
```

### 3. Run setup

```cmd
setup.bat
```

### 4. Start PebbleAI

Run:

```cmd
python app.py
```

> ⚠️ **Important:** Always run PebbleAI using `python app.py` from the terminal.  
> Do not double-click `app.py` or open it directly in VS Code/File Explorer.  
> Windows may associate `.py` files with a text editor, causing the file to open instead of running.

---

## Linux / macOS

### 1. Clone the repository

```bash
git clone https://github.com/someoneinsogvt2020-lang/pabble.ai.git
```

### 2. Enter the project folder

```bash
cd pabble.ai
cd PebbleAI
```

### 3. Run setup

```bash
chmod +x setup.sh
./setup.sh
```

### 4. Start PebbleAI

```bash
python3 app.py
```

> ⚠️ Run PebbleAI through Python from the terminal. Opening the file directly will not start the application.

---

# 📖 How to Use

## 🌐 Web Interface (Recommended)

1. Start PebbleAI:

```cmd
python app.py
```

2. Open your browser.

3. Visit:

```
http://127.0.0.1:5000/
```

4. Start chatting with PebbleAI.

You can:

- Ask questions.
- Generate code.
- Summarize documents.
- Search the web.
- Process local files.
- Use AI-powered tools.

---

## 💻 Terminal Mode

Run:

```cmd
python main.py
```

Commands:

```
/clear  - Clear conversation memory
/exit   - Exit PebbleAI
```

---

# 🤖 Supported Models

PebbleAI supports:

- `gemma3:4b`
- `qwen2.5:3b`
- `deepseek-r1:1.5b`
- `qwen3:4b`

Additional Ollama-compatible models can be added.

---

# 🛡 Security & Privacy

PebbleAI is designed around privacy.

✅ Runs locally  
✅ No API keys required  
✅ No subscription fees  
✅ No cloud processing  
✅ Your data stays on your device  

All AI inference happens locally through Ollama.

---

# 📦 Release Information

## PebbleAI v0.1.0 — First Public Test Build

### Tested

- Windows setup
- Ollama integration
- Local model loading
- Flask web interface
- Basic AI conversations

### Known Rough Edges

- Some features may still need refinement.
- Hardware performance depends on your system.
- First-time setup requires Python and Ollama installation.

---

<div align="center">

# 🪨 PebbleAI

**Private. Fast. Local.**

Built with ❤️ for local AI enthusiasts.

</div>
