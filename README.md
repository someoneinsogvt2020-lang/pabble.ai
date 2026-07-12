# PebbleAI

> A lightweight, local AI assistant powered by open-source models and designed to run privately on your own machine.

## Overview

PebbleAI is a personal AI assistant project focused on creating a simple, customizable, and privacy-friendly AI experience.

Unlike cloud-only assistants, PebbleAI is designed to run locally using locally hosted language models through **Ollama**, giving users more control over their data, models, and AI environment.

The goal of PebbleAI is to create a compact but powerful AI system that can be expanded with tools, memory, and intelligent automation features.

---

## Features

### 🤖 Local AI Chat

* Chat with locally running AI models
* No dependency on external AI services
* Privacy-focused conversations
* Supports multiple open-source models

### 🧠 Multi-Model Support

PebbleAI can work with different local models depending on hardware capability:

* Gemma
* Qwen
* DeepSeek
* Other Ollama-compatible models

Users can choose models based on speed, intelligence, and available system resources.

---

## Architecture

PebbleAI uses a modular architecture:

```
PebbleAI
│
├── Flask Backend
│   ├── API Routes
│   ├── AI Agent System
│   ├── Tool Management
│   └── Model Communication
│
├── Frontend Interface
│   ├── Chat UI
│   ├── Message System
│   └── User Interaction
│
├── Ollama
│   └── Local Language Models
│
└── Configuration
    ├── Environment Variables
    └── User Settings
```

---

## Technology Stack

### Backend

* Python
* Flask
* Requests
* Local AI APIs

### AI Runtime

* Ollama
* Open-source Large Language Models

### Frontend

* HTML
* CSS
* JavaScript

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/PebbleAI.git
cd PebbleAI
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Ollama

Download Ollama from:

https://ollama.com

### 4. Download an AI model

Example:

```bash
ollama pull gemma3:4b
```

### 5. Start PebbleAI

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

## Configuration

PebbleAI uses environment variables for private settings.

Create a `.env` file:

```env
OLLAMA_URL=http://localhost:11434
MODEL=gemma3:4b
```

Do not upload your `.env` file to GitHub.

---

## Project Goals

The long-term vision of PebbleAI is to build a complete personal AI ecosystem with:

* Memory system
* Custom tools
* Better reasoning capabilities
* File understanding
* Automation features
* Improved user interface
* Hardware-aware model selection

---

## Privacy

PebbleAI is designed around local processing.

Your conversations and data stay on your own machine unless you intentionally connect external services.

---

## Development Status

🚧 Active Development

Current focus:

* Improving AI agent capabilities
* Expanding tool support
* Enhancing UI experience
* Improving model management

---

## License

This project is currently under development. License information will be added in the future.

---

## Author

Created by **Daksh Studio**

Building experimental AI tools and software projects.

