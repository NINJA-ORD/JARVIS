import json
import wave
import time
import sounddevice as sd
import numpy as np
import pyttsx3

from vosk import Model, KaldiRecognizer
from ai.brain import jarvis_brain


# ============================================================
# JARVIS VOICE CONFIG
# ============================================================

MODEL_PATH = "models/vosk-model-small-en-us-0.15"

MIC_DEVICE = 1
SAMPLE_RATE = 16000
CHANNELS = 1

RECORD_SECONDS = 5


# ============================================================
# TEXT TO SPEECH
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
# LOAD VOSK
# ============================================================

print("Loading JARVIS speech model...")

model = Model(MODEL_PATH)

print("Vosk model loaded.")


# ============================================================
# RECORD MICROPHONE
# ============================================================

def record_audio():

    print("\n🎤 Speak now...")

    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        device=MIC_DEVICE
    )

    sd.wait()

    return audio


# ============================================================
# SPEECH TO TEXT
# ============================================================

def speech_to_text(audio):

    recognizer = KaldiRecognizer(
        model,
        SAMPLE_RATE
    )

    audio_bytes = audio.tobytes()

    recognizer.AcceptWaveform(audio_bytes)

    result = json.loads(
        recognizer.FinalResult()
    )

    text = result.get("text", "").strip()

    return text


# ============================================================
# MAIN LOOP
# ============================================================

def main():

    print()
    print("================================")
    print("        JARVIS LIVE MODE")
    print("================================")
    print()
    print("Speak to JARVIS.")
    print("Say 'exit' to stop.")
    print()

    speak("JARVIS online. I am ready, sir.")

    while True:

        try:

            audio = record_audio()

            text = speech_to_text(audio)

            if not text:

                print("JARVIS: I didn't hear anything.")

                continue

            print("\n🗣️ YOU:", text)

            # ------------------------------------------------
            # EXIT
            # ------------------------------------------------

            if text.lower() in [
                "exit",
                "quit",
                "goodbye",
                "bye"
            ]:

                speak("Goodbye sir.")

                break

            # ------------------------------------------------
            # BRAIN
            # ------------------------------------------------

            print("\n🧠 Thinking...")

            response = jarvis_brain(text)

            # ------------------------------------------------
            # VOICE RESPONSE
            # ------------------------------------------------

            speak(response)

            time.sleep(0.3)

        except KeyboardInterrupt:

            print("\n")

            speak("JARVIS shutting down, sir.")

            break

        except Exception as e:

            print("\nERROR:", e)

            speak(
                "Sorry sir, something went wrong."
            )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()