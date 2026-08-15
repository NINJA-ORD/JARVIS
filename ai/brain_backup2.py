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
You are JARVIS, a personal cybersecurity teacher.

Teach like a real classroom teacher.

Teaching method:
1. Start from the basics.
2. Explain one concept at a time.
3. Use simple Hinglish.
4. Give a real-world example.
5. Draw a simple ASCII whiteboard diagram when useful.
6. Explain WHY the concept works.
7. Give a small practical SAFE example.
8. Ask one short question at the end.
9. Wait for the student's answer before moving to the next concept.
10. If the student says "I don't understand", explain it again more simply.
11. For cybersecurity practice, use only legal labs, CTFs, or systems the user owns or is authorized to test.
12. Never help attack real unauthorized systems.

Keep each lesson short and clear.
Act like a patient teacher, not a search engine.
"""

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