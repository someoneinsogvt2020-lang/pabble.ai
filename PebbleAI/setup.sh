#!/bin/bash
echo "PebbleAI Setup..."
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo ""
echo "Pulling necessary Ollama models..."
echo "Make sure Ollama is installed and running!"
ollama pull qwen2.5:3b
ollama pull gemma3:4b
ollama pull deepseek-r1:1.5b
ollama pull qwen3:4b
echo ""
echo "Setup Complete! You can now run PebbleAI by typing:"
echo "python3 app.py"
