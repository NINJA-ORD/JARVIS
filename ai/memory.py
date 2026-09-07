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


# ============================================================
# FILE MANAGEMENT
# ============================================================

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


def _load_all_memory():
    """Load all memory entries from disk."""

    ensure_memory_file()

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except (json.JSONDecodeError, OSError):
        return []


def _save_all_memory(memory):
    """Save all memory entries to disk."""

    ensure_memory_file()

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            memory,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# NORMAL CONVERSATION MEMORY
# ============================================================

def load_memory():
    """
    Load only normal conversation memory.

    Important memories are automatically excluded.
    """

    memory = _load_all_memory()

    return [
        item
        for item in memory
        if item.get("role") in ["user", "assistant"]
    ]


def save_memory(memory):
    """
    Save normal conversation memory
    while preserving important memories.
    """

    all_memory = _load_all_memory()

    important_memories = [
        item
        for item in all_memory
        if item.get("type") == "important"
    ]

    conversation_memory = [
        item
        for item in memory
        if item.get("role") in ["user", "assistant"]
    ]

    if len(conversation_memory) > MAX_MEMORY:
        conversation_memory = conversation_memory[-MAX_MEMORY:]

    _save_all_memory(
        conversation_memory + important_memories
    )


def add_memory(role, content):
    """Add a normal conversation message."""

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
    """
    Clear normal conversation memory
    without deleting important memories.
    """

    all_memory = _load_all_memory()

    important_memories = [
        item
        for item in all_memory
        if item.get("type") == "important"
    ]

    _save_all_memory(important_memories)


def get_memory():
    """Return normal conversation memory."""

    return load_memory()


# ============================================================
# IMPORTANT MEMORY
# ============================================================

def save_important_memory(key, value):
    """
    Save or update an important memory.

    If the key already exists, update it instead
    of creating a duplicate.
    """

    key = str(key).strip()
    value = str(value).strip()

    if not key or not value:
        return

    memory = _load_all_memory()

    updated = False

    for item in memory:

        if (
            item.get("type") == "important"
            and item.get("key") == key
        ):

            item["value"] = value
            updated = True
            break

    if not updated:

        memory.append({
            "type": "important",
            "key": key,
            "value": value
        })

    _save_all_memory(memory)


def get_important_memories():
    """Return all important memories."""

    memory = _load_all_memory()

    return [
        item
        for item in memory
        if item.get("type") == "important"
    ]


# ============================================================
# CLEAR EVERYTHING
# ============================================================

def clear_all_memory():
    """
    Delete both normal conversation
    and important memories.
    """

    _save_all_memory([])