import json
import time
import sounddevice as sd
import pyttsx3

from vosk import Model, KaldiRecognizer
from rapidfuzz import fuzz

from ai.brain import jarvis_brain


# ============================================================
# CONFIG
# ============================================================

MODEL_PATH = "models/vosk-model-small-en-us-0.15"

MIC_DEVICE = 1
SAMPLE_RATE = 16000
CHANNELS = 1

WAKE_WORDS = [
    "jarvis",
    "hey jarvis",
    "okay jarvis",
    "ok jarvis",
]


# ============================================================
# TTS
# ============================================================

engine = pyttsx3.init()

engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)


def speak(text):

    print("\nJARVIS:", text)

    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("TTS ERROR:", e)


# ============================================================
# VOSK
# ============================================================

print("Loading Vosk model...")

model = Model(MODEL_PATH)

print("Vosk loaded.")


# ============================================================
# WAKE WORD
# ============================================================

def wait_for_wake_word():

    recognizer = KaldiRecognizer(
        model,
        SAMPLE_RATE
    )

    print()
    print("================================")
    print("       JARVIS STANDBY")
    print("================================")
    print()
    print("Say: Jarvis")
    print()

    detected = False

    def callback(indata, frames, time_info, status):

        nonlocal detected

        if detected:
            return

        if status:
            print("Audio:", status)

        data = bytes(indata)

        if recognizer.AcceptWaveform(data):

            result = json.loads(
                recognizer.Result()
            )

            text = result.get(
                "text",
                ""
            ).lower().strip()

            if not text:
                return

            print("HEARD:", text)

            for wake_word in WAKE_WORDS:

                score = fuzz.partial_ratio(
                    wake_word,
                    text
                )

                if score >= 75:

                    detected = True
                    break

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        device=MIC_DEVICE,
        dtype="int16",
        channels=CHANNELS,
        callback=callback
    ):

        while not detected:
            sd.sleep(100)

    return True


# ============================================================
# LISTEN FOR COMMAND
# ============================================================

def listen_for_command():

    print()
    print("🎤 Listening for your command...")

    recognizer = KaldiRecognizer(
        model,
        SAMPLE_RATE
    )

    audio = sd.rec(
        int(5 * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        device=MIC_DEVICE
    )

    sd.wait()

    recognizer.AcceptWaveform(
        audio.tobytes()
    )

    result = json.loads(
        recognizer.FinalResult()
    )

    text = result.get(
        "text",
        ""
    ).strip()

    return text


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("================================")
    print("          JARVIS ONLINE")
    print("================================")

    speak(
        "JARVIS online. "
        "Say my name when you need me, sir."
    )

    while True:

        try:

            # -----------------------------------------------
            # WAIT FOR "JARVIS"
            # -----------------------------------------------

            wait_for_wake_word()

            print()
            print("🔥 WAKE WORD DETECTED!")

            speak("Yes sir?")

            # -----------------------------------------------
            # LISTEN FOR COMMAND
            # -----------------------------------------------

            command = listen_for_command()

            if not command:

                speak(
                    "Sorry sir, "
                    "I didn't hear your command."
                )

                continue

            print()
            print("🗣️ YOU:", command)

            # -----------------------------------------------
            # EXIT
            # -----------------------------------------------

            if command.lower() in [
                "exit",
                "quit",
                "shutdown",
                "goodbye",
                "stop"
            ]:

                speak(
                    "JARVIS shutting down, sir."
                )

                break

            # -----------------------------------------------
            # BRAIN
            # -----------------------------------------------

            print()
            print("🧠 Thinking...")

            response = jarvis_brain(
                command
            )

            # -----------------------------------------------
            # RESPONSE
            # -----------------------------------------------

            speak(response)

            time.sleep(0.5)

        except KeyboardInterrupt:

            print()

            speak(
                "JARVIS shutting down, sir."
            )

            break

        except Exception as e:

            print()
            print("ERROR:", e)

            speak(
                "Sorry sir, "
                "I encountered an error."
            )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()