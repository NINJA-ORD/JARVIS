import json
import urllib.request
import urllib.error
from datetime import datetime


# ============================================================
# JARVIS CONFIG
# ============================================================

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
OLLAMA_MODEL = "qwen3:1.7b"


# ============================================================
# OLLAMA BRAIN
# ============================================================

def ask_ollama(message: str, teacher_mode: bool = False) -> str:

    if teacher_mode:
        system_prompt = """
You are JARVIS, an expert personal teacher and AI assistant.

The user is learning cybersecurity and ethical hacking.

TEACHING RULES:
1. Teach from beginner level to advanced level.
2. Explain concepts step by step.
3. Use simple Hinglish when appropriate.
4. Use examples.
5. Use text diagrams like a classroom whiteboard when useful.
6. Explain WHY something works, not only WHAT it is.
7. After important concepts, ask a small question to test understanding.
8. Never assume the student already knows advanced concepts.
9. Never overwhelm the student with too much information at once.
10. For cybersecurity, stay within legal and ethical learning.
11. Do not provide instructions for harming real systems.
12. If the student asks for a practical lab, prefer safe local labs,
    CTFs, TryHackMe, Hack The Box, or intentionally vulnerable machines.

CLASSROOM STYLE:

Topic
  ↓
Simple explanation
  ↓
Example
  ↓
Whiteboard diagram
  ↓
Practical safe example
  ↓
Mini question

Keep explanations clear and conversational.
"""

    else:
        system_prompt = """
You are JARVIS, a helpful local desktop AI assistant.

Rules:
1. Give short and useful answers.
2. Be polite and natural.
3. Call the user "sir" when appropriate.
4. Do not generate shell commands unless specifically requested.
5. Do not pretend you executed an action.
6. Do not invent tools.
7. Keep normal voice-assistant responses concise.
"""

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": message
            }
        ],
        "stream": False
    }

    try:

        data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            OLLAMA_URL,
            data=data,
            headers={
                "Content-Type": "application/json"
            },
            method="POST"
        )

        with urllib.request.urlopen(request, timeout=120) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        answer = (
            result
            .get("message", {})
            .get("content", "")
            .strip()
        )

        if not answer:
            return "I couldn't generate a response, sir."

        # Remove Qwen thinking section if present
        if "<think>" in answer and "</think>" in answer:
            answer = answer.split("</think>", 1)[1].strip()

        return answer

    except urllib.error.URLError:
        return (
            "Ollama is not running, sir. "
            "Please start Ollama and try again."
        )

    except Exception as e:
        return f"Ollama error: {e}"


# ============================================================
# JARVIS BRAIN
# ============================================================

def jarvis_brain(message: str) -> str:

    message = message.strip()

    if not message:
        return "Please tell me something, sir."

    lower = message.lower()


    # ========================================================
    # FAST LOCAL COMMANDS
    # ========================================================

    if lower in [
        "hello",
        "hi",
        "hey",
        "hello jarvis",
        "hi jarvis",
        "hey jarvis"
    ]:
        return "Hello sir. JARVIS is ready."


    # ========================================================
    # TIME
    # ========================================================

    if (
        lower == "time"
        or "what is the time" in lower
        or "what's the time" in lower
        or "current time" in lower
        or "time batao" in lower
    ):

        current_time = datetime.now().strftime("%I:%M %p")

        return f"The current time is {current_time}, sir."


    # ========================================================
    # DATE
    # ========================================================

    if (
        lower == "date"
        or "what is the date" in lower
        or "what's the date" in lower
        or "today's date" in lower
        or "date batao" in lower
    ):

        current_date = datetime.now().strftime("%d %B %Y")

        return f"Today is {current_date}, sir."


    # ========================================================
    # TEACHER MODE
    # ========================================================

    teacher_keywords = [
        "teach me",
        "teach me cybersecurity",
        "teach cybersecurity",
        "cybersecurity sikhao",
        "cyber security sikhao",
        "mujhe cybersecurity sikhao",
        "cybersecurity ke bare me batao",
        "cyber security ke bare me batao",
        "teacher mode",
        "start teaching",
        "padhai shuru karo"
    ]

    teacher_mode = any(
        keyword in lower
        for keyword in teacher_keywords
    )


    if teacher_mode:

        return ask_ollama(
            message,
            teacher_mode=True
        )


    # ========================================================
    # NORMAL AI CHAT
    # ========================================================

    return ask_ollama(
        message,
        teacher_mode=False
    )


# ============================================================
# SIMPLE TEST
# ============================================================

if __name__ == "__main__":

    print("================================")
    print("       JARVIS BRAIN TEST")
    print("================================")

    while True:

        user_input = input("\nYou: ").strip()

        if user_input.lower() in [
            "exit",
            "quit",
            "bye"
        ]:
            print("JARVIS: Goodbye, sir.")
            break

        response = jarvis_brain(user_input)

        print("\nJARVIS:", response)