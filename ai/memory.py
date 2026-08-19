import json
from pathlib import Path


# ============================================================
# JARVIS PERSISTENT MEMORY
# ============================================================

MEMORY_FILE = Path(__file__).resolve().parent.parent / "data" / "jarvis_memory.json"


def ensure_memory_file():
    """
    Create the data directory and memory file if they do not exist.
    """

    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not MEMORY_FILE.exists():

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4,
                ensure_ascii=False
            )


def load_memory():
    """
    Load persistent memory from disk.
    """

    ensure_memory_file()

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


def save_memory(memory):
    """
    Save persistent memory to disk.
    """

    ensure_memory_file()

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            memory,
            file,
            indent=4,
            ensure_ascii=False
        )


def add_memory(role, content):
    """
    Add a conversation message to persistent memory.
    """

    memory = load_memory()

    memory.append({
        "role": role,
        "content": content
    })

    save_memory(memory)


def clear_memory():
    """
    Delete all persistent conversation memory.
    """

    save_memory([])


def get_memory():
    """
    Return all persistent memory.
    """

    return load_memory()