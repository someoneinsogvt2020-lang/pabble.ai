<div align="center">
  <h1>🪨 PebbleAI</h1>
  <p><strong>A powerful, privacy-first local AI assistant running entirely on your computer.</strong></p>
  
  [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
  [![Ollama](https://img.shields.io/badge/Ollama-Supported-orange.svg)](https://ollama.com/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)
</div>

<br>

PebbleAI is an intelligent local assistant that leverages the power of open-source language models (like Gemma, Qwen, and DeepSeek) through Ollama. It operates 100% locally on your machine, ensuring complete privacy, fast performance, and no hidden API costs.

## ✨ Features

- **🔒 100% Local & Private**: No data leaves your machine. Your conversations and files remain entirely on your device.
- **🧠 Intelligent Routing**: Automatically switches between models based on the task (e.g., using Qwen for coding and Gemma for general queries).
- **🛠️ Agentic Tools**: Includes a built-in tool registry allowing the AI to:
  - Perform live web searches and read web pages.
  - Read and write files on your local filesystem.
  - Automate desktop actions (launch apps, open URLs).
  - Process documents (PDFs, Docx) and handle data.
- **💻 Web Interface**: A sleek Flask-based frontend for seamless interaction.
- **⚡ Hardware Acceleration**: Automatically detects and utilizes NVIDIA (CUDA) or AMD (ROCm) GPUs for faster inference.

## 🚀 Prerequisites

Before installing PebbleAI, ensure you have the following installed:

1. **Python 3.10+**: Make sure Python is added to your system PATH.
2. **[Ollama](https://ollama.com/)**: Required to run the local language models. Download it, install it, and ensure the service is running in the background.

## 🛠️ Installation & Setup

We've provided quick setup scripts to automatically install dependencies and download the necessary local models.

### Windows

1. Clone the repository and navigate to the folder:
   ```cmd
   git clone https://github.com/your-username/PebbleAI.git
   cd PebbleAI
   ```
2. Run the setup script:
   ```cmd
   setup.bat
   ```
3. Once the setup completes, start the application:
   ```cmd
   python app.py
   ```

### Linux / macOS

1. Clone the repository and navigate to the folder:
   ```bash
   git clone https://github.com/your-username/PebbleAI.git
   cd PebbleAI
   ```
2. Make the setup script executable and run it:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
3. Start the application:
   ```bash
   python3 app.py
   ```

## 🎮 Usage

After running `app.py` or `main.py`, you can interact with PebbleAI in two ways:

### Web UI (Recommended)
Open your web browser and navigate to the local URL provided in the terminal (usually `http://127.0.0.1:5000/`). Enjoy a rich chat interface!

### Terminal Mode
You can also run `python main.py` to chat with PebbleAI directly in your terminal. Use commands like `/clear` to clear conversation memory.

## 🤖 Supported Models

PebbleAI is configured to work with the following models out-of-the-box (handled by the setup scripts):
- `gemma3:4b`
- `qwen2.5:3b`
- `deepseek-r1:1.5b`
- `qwen3:4b`

## 🛡️ Security & Privacy
PebbleAI is built with security in mind. It includes basic protections against prompt extraction and logs blocked security events locally. Since it runs via Ollama, all inference happens completely offline.

---
<div align="center">
  <i>Built with ❤️ for local AI enthusiasts.</i>
</div>
