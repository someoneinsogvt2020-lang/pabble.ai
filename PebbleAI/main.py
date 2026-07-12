from memory import load_memory, save_memory, get_memory, clear_memory
from ai import ask_ai

load_memory()

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        break

    if user_input.lower() == "/clear":
        clear_memory()
        print("PebbleAI: Memory cleared.")
        continue

    if user_input.lower() == "memory":
        print("PebbleAI:", get_memory())
        continue

    save_memory(user_input)

    response = ask_ai(user_input)

    print("PebbleAI:", response)