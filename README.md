# 🤖 JARVIS — Personal Desktop AI Assistant

A personal desktop AI voice assistant built from scratch with Python.

JARVIS is designed to understand voice commands, respond using a local AI model, maintain conversation context, remember important information, and interact with the local computer.

## 🚀 Current Features

* 🎙️ Voice input
* 🔊 Voice output
* 🧠 Local AI using Ollama
* 🤖 Qwen 3 1.7B model
* 👂 "Jarvis" wake-word detection
* 💬 Continuous conversation mode
* 🧠 Persistent conversation memory
* 🔑 Important memory storage
* 🧹 Conversation memory reset
* 🪟 Windows microphone support
* ⚡ Fast local processing
* 🛠️ Desktop application/tool integration

## 🧠 Memory System

JARVIS currently supports persistent memory.

Important information can be stored and loaded even after restarting JARVIS.

Example:

```text
User: Remember my name is Prithvi.

JARVIS: I'll remember that.

User: What is my name?

JARVIS: Your name is Prithvi.
```

Memory is stored locally in:

```text
data/jarvis_memory.json
```

## 🎙️ Voice Pipeline

```text
Microphone
    ↓
SoundDevice
    ↓
48 kHz Audio
    ↓
Resampling
    ↓
16 kHz Audio
    ↓
Vosk Speech Recognition
    ↓
Wake Word / Command
    ↓
JARVIS Brain
    ↓
Ollama + Qwen
    ↓
Response
    ↓
Text-to-Speech
    ↓
Speaker
```

## 🛠️ Technologies

* Python
* Vosk
* SoundDevice
* NumPy
* SciPy
* Ollama
* Qwen 3 1.7B
* pyttsx3
* FastAPI
* Git & GitHub

## 📅 Development Progress

| Day    | Milestone                                        |
| ------ | ------------------------------------------------ |
| Day 01 | FastAPI foundation                               |
| Day 02 | Desktop application tools                        |
| Day 03 | AI brain integration                             |
| Day 04 | Voice input/output                               |
| Day 05 | Microphone and speech recognition debugging      |
| Day 06 | Wake-word system                                 |
| Day 07 | Continuous conversation                          |
| Day 08 | Reliable wake-word and conversation improvements |
| Day 09 | Persistent conversation memory                   |
| Day 10 | Smart persistent memory                          |

## 🎯 Future Plans

* Advanced memory management
* System information and control
* File and folder automation
* Browser automation
* Better voice activity detection
* Advanced cybersecurity teacher mode
* Tool execution framework
* Safer command execution
* Performance optimization
* More natural conversations
* JARVIS v1.0 final integration

## 📂 Project Structure

```text
JARVIS/
│
├── ai/
│   ├── brain.py
│   ├── memory.py
│   └── ...
│
├── data/
│   └── jarvis_memory.json
│
├── tools/
│   └── apps.py
│
├── jarvis.py
├── main.py
├── voice_assistant.py
└── README.md
```

## 🔐 Project Status

🚧 **Active Development**

JARVIS is currently being developed step-by-step as a personal desktop AI assistant.

Current milestone: **Day 10 — Smart Persistent Memory**

## 👨‍💻 Author

**Prithviraj Patil**

Built as a personal learning and development project.

---

⭐ If you find this project interesting, consider starring the repository.
