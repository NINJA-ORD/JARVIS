import json
from pathlib import Path


# ============================================================
# JARVIS PERSISTENT MEMORY
# ============================================================

MAX_MEMORY = 100

MEMORY_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "jarvis_memory.json"
)


def ensure_memory_file():
    """Create the data directory and memory file if needed."""

    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not MEMORY_FILE.exists():
        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump(
                [],
                file,
                indent=4,
                ensure_ascii=False
            )


def load_memory():
    """Load persistent memory from disk."""

    ensure_memory_file()

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except (json.JSONDecodeError, OSError):
        return []


def save_memory(memory):
    """Save persistent memory to disk."""

    ensure_memory_file()

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            memory,
            file,
            indent=4,
            ensure_ascii=False
        )


def add_memory(role, content):
    """Add useful conversation message to persistent memory."""

    content = content.strip()

    # Ignore empty or extremely short speech-recognition results
    if len(content) < 3:
        return

    memory = load_memory()

    memory.append({
        "role": role,
        "content": content
    })

    if len(memory) > MAX_MEMORY:
        memory = memory[-MAX_MEMORY:]

    save_memory(memory)


def clear_memory():
    """Delete all persistent conversation memory."""

    save_memory([])


def get_memory():
    """Return all persistent memory."""

    return load_memory()


def save_important_memory(key, value):
    """Save an important piece of information."""

    memory = load_memory()

    memory.append({
        "type": "important",
        "key": key,
        "value": value
    })

    save_memory(memory)


def get_important_memories():
    """Return all important memories."""

    memory = load_memory()

    return [
        item
        for item in memory
        if item.get("type") == "important"
    ]