# PebbleAI

PebbleAI is a powerful local AI assistant running entirely on your computer. It focuses on privacy, performance, and utilizing local compute.

## Prerequisites

Before installing PebbleAI, ensure you have the following installed:
1. **Python 3.10+**: Make sure Python is added to your system PATH.
2. **Ollama**: Required to run the local language models. Download it from [ollama.com](https://ollama.com/) and ensure it is running in the background.

## Installation

We've provided scripts to easily set up PebbleAI and download the necessary local models.

### Windows
1. Double-click `setup.bat` or run it from the command prompt:
   ```cmd
   git clone <your-repo-url-here>
   cd PebbleAI
   setup.bat
   ```
2. Once the setup is complete, start the application:
   ```cmd
   python app.py
   ```

### Linux / macOS
1. Open a terminal and make the setup script executable:
   ```bash
   git clone <your-repo-url-here>
   cd PebbleAI
   chmod +x setup.sh
   ```
2. Run the setup script:
   ```bash
   ./setup.sh
   ```
3. Once the setup is complete, start the application:
   ```bash
   python3 app.py
   ```

## Usage

After starting `app.py`, open your web browser and navigate to the local URL (usually `http://127.0.0.1:5000/`) provided in the terminal to interact with PebbleAI.
