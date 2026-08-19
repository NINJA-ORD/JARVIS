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
# CONVERSATION MEMORY
# ============================================================

MAX_HISTORY_MESSAGES = 10

conversation_history = []


def reset_memory():
    """
    Clear current JARVIS conversation memory.
    """

    global conversation_history

    conversation_history = []

    print(
        "JARVIS memory cleared.",
        flush=True
    )


def add_to_memory(role, content):
    """
    Add a message to conversation history.
    """

    conversation_history.append({
        "role": role,
        "content": content
    })

    # Keep memory small for Qwen 1.7B
    if len(conversation_history) > MAX_HISTORY_MESSAGES:

        del conversation_history[
            :len(conversation_history) - MAX_HISTORY_MESSAGES
        ]


# ============================================================
# OLLAMA BRAIN
# ============================================================

def ask_ollama(
    message: str,
    teacher_mode: bool = False
) -> str:

    # ========================================================
    # TEACHER MODE
    # ========================================================

    if teacher_mode:

        system_prompt = """
You are JARVIS, a personal cybersecurity teacher.

Teach the student like a real classroom teacher.

Teaching rules:

1. Start from beginner level.
2. Explain one concept at a time.
3. Use simple Hinglish.
4. Use easy language.
5. Give a real-world example.
6. Use simple ASCII whiteboard diagrams when useful.
7. Explain WHY the concept works.
8. Give safe practical examples.
9. Use only legal labs, CTFs and authorized systems.
10. Never help attack unauthorized real systems.
11. Ask one small question at the end.
12. If the student says they don't understand, explain it again more simply.
13. Do not overload the student with too much information.
14. Remember the current conversation context when answering follow-up questions.

Classroom format:

TOPIC
↓
Simple Explanation
↓
Real World Example
↓
Whiteboard Diagram
↓
Safe Practical Example
↓
Mini Question

Keep lessons clear, short and conversational.
Act like a patient teacher.
"""

    # ========================================================
    # NORMAL MODE
    # ========================================================

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
7. Keep normal answers concise.
8. Use previous conversation context when answering follow-up questions.
"""


    # ========================================================
    # ADD USER MESSAGE TO MEMORY
    # ========================================================

    add_to_memory(
        "user",
        message
    )


    # ========================================================
    # BUILD OLLAMA MESSAGES
    # ========================================================

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    messages.extend(
        conversation_history
    )


    # ========================================================
    # OLLAMA REQUEST
    # ========================================================

    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False
    }


    try:

        data = json.dumps(
            payload
        ).encode("utf-8")

        request = urllib.request.Request(
            OLLAMA_URL,
            data=data,
            headers={
                "Content-Type": "application/json"
            },
            method="POST"
        )

        with urllib.request.urlopen(
            request,
            timeout=180
        ) as response:

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

            # Remove failed user message
            if conversation_history:

                conversation_history.pop()

            return (
                "I couldn't generate a response, sir."
            )


        # ====================================================
        # REMOVE QWEN THINKING
        # ====================================================

        if (
            "<think>" in answer
            and "</think>" in answer
        ):

            answer = answer.split(
                "</think>",
                1
            )[1].strip()


        # ====================================================
        # ADD ASSISTANT RESPONSE TO MEMORY
        # ====================================================

        add_to_memory(
            "assistant",
            answer
        )


        return answer


    except urllib.error.URLError:

        # Remove user message if request failed
        if conversation_history:

            conversation_history.pop()

        return (
            "Ollama is not running, sir. "
            "Please start Ollama and try again."
        )


    except TimeoutError:

        if conversation_history:

            conversation_history.pop()

        return (
            "Ollama is taking too long to respond, sir. "
            "Please try again."
        )


    except Exception as e:

        if conversation_history:

            conversation_history.pop()

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
    # RESET MEMORY
    # ========================================================

    if lower in [
        "forget everything",
        "forget our conversation",
        "clear memory",
        "clear conversation",
        "reset memory",
        "reset conversation"
    ]:

        reset_memory()

        return (
            "Conversation memory cleared, sir."
        )


    # ========================================================
    # GREETINGS
    # ========================================================

    if lower in [
        "hello",
        "hi",
        "hey",
        "hello jarvis",
        "hi jarvis",
        "hey jarvis"
    ]:

        return (
            "Hello sir. JARVIS is ready."
        )


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

        current_time = datetime.now().strftime(
            "%I:%M %p"
        )

        return (
            f"The current time is "
            f"{current_time}, sir."
        )


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

        current_date = datetime.now().strftime(
            "%d %B %Y"
        )

        return (
            f"Today is "
            f"{current_date}, sir."
        )


    # ========================================================
    # TEACHER MODE
    # ========================================================

    teacher_keywords = [

        "teach me",

        "teach me cybersecurity",

        "teach cybersecurity",

        "teach me cyber security",

        "cybersecurity sikhao",

        "cyber security sikhao",

        "mujhe cybersecurity sikhao",

        "mujhe cyber security sikhao",

        "cybersecurity ke bare me batao",

        "cyber security ke bare me batao",

        "cybersecurity ke baare mein batao",

        "teacher mode",

        "start teaching",

        "padhai shuru karo",

        "mujhe networking sikhao",

        "teach me networking",

        "teach me linux",

        "teach me ethical hacking"
    ]


    teacher_mode = any(
        keyword in lower
        for keyword in teacher_keywords
    )


    # ========================================================
    # TEACHER MODE REQUEST
    # ========================================================

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
# TERMINAL TEST MODE
# ============================================================

if __name__ == "__main__":

    print(
        "================================"
    )

    print(
        "       JARVIS BRAIN TEST"
    )

    print(
        "================================"
    )

    print()

    print(
        "Type 'exit' to stop."
    )

    print(
        "Type 'clear memory' to reset memory."
    )

    print()


    while True:

        try:

            user_input = input(
                "\nYou: "
            ).strip()


            if user_input.lower() in [
                "exit",
                "quit",
                "bye"
            ]:

                print(
                    "\nJARVIS: Goodbye sir."
                )

                break


            response = jarvis_brain(
                user_input
            )


            print(
                "\nJARVIS:",
                response
            )


        except KeyboardInterrupt:

            print(
                "\n\nJARVIS: Goodbye sir."
            )

            break


        except Exception as e:

            print(
                "\nJARVIS ERROR:",
                e
            )