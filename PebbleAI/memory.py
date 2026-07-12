memory = []


def load_memory():
    global memory

    try:
        with open("memory.txt", "r") as file:
            memory = [line.strip() for line in file]

    except FileNotFoundError:
        memory = []


def save_memory(item):
    memory.append(item)

    with open("memory.txt", "a") as file:
        file.write(item + "\n")


def get_memory():
    return memory


def clear_memory():
    global memory

    memory = []

    with open("memory.txt", "w") as file:
        pass