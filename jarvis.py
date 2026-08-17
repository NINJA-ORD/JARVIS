import json
import time
import queue

import numpy as np
import sounddevice as sd
import pyttsx3

from scipy.signal import resample_poly
from vosk import Model, KaldiRecognizer

from ai.brain import jarvis_brain


# ============================================================
# CONFIG
# ============================================================

MODEL_PATH = "models/vosk-model-small-en-us-0.15"

MIC_DEVICE = 1

MIC_RATE = 48000
VOSK_RATE = 16000

CHANNELS = 1
BLOCKSIZE = 4800

WAKE_WORDS = [
    "jarvis",
    "jarvis sir",
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

    print("\nJARVIS:", text, flush=True)

    try:

        engine.say(text)
        engine.runAndWait()

    except Exception as e:

        print(
            "TTS ERROR:",
            e,
            flush=True
        )


# ============================================================
# VOSK
# ============================================================

print(
    "Loading Vosk model...",
    flush=True
)

model = Model(MODEL_PATH)

print(
    "Vosk loaded.",
    flush=True
)


# ============================================================
# WAKE WORD GRAMMAR
# ============================================================

WAKE_GRAMMAR = json.dumps([
    "jarvis",
    "jarvis sir",
    "hey jarvis",
    "okay jarvis",
    "ok jarvis",
    "[unk]"
])


# ============================================================
# AUDIO QUEUE
# ============================================================

audio_queue = queue.Queue(
    maxsize=20
)


def audio_callback(
    indata,
    frames,
    time_info,
    status
):

    if status:

        print(
            "AUDIO:",
            status,
            flush=True
        )

    try:

        audio_queue.put_nowait(
            bytes(indata)
        )

    except queue.Full:

        print(
            "WARNING: Audio queue full",
            flush=True
        )


# ============================================================
# CONVERT 48kHz -> 16kHz
# ============================================================

def convert_audio(data):

    audio_48k = np.frombuffer(
        data,
        dtype=np.int16
    )

    audio_16k = resample_poly(
        audio_48k,
        VOSK_RATE,
        MIC_RATE
    )

    audio_16k = np.asarray(
        audio_16k,
        dtype=np.int16
    )

    return audio_16k.tobytes()


# ============================================================
# WAIT FOR WAKE WORD
# ============================================================

def wait_for_wake_word():

    recognizer = KaldiRecognizer(
        model,
        VOSK_RATE,
        WAKE_GRAMMAR
    )

    print()
    print(
        "================================",
        flush=True
    )
    print(
        "       JARVIS STANDBY",
        flush=True
    )
    print(
        "================================",
        flush=True
    )
    print()
    print(
        "Say: Jarvis",
        flush=True
    )
    print()

    # Clear old audio
    while not audio_queue.empty():

        try:
            audio_queue.get_nowait()

        except queue.Empty:
            break

    detected = False

    with sd.RawInputStream(
        samplerate=MIC_RATE,
        blocksize=BLOCKSIZE,
        device=MIC_DEVICE,
        dtype="int16",
        channels=CHANNELS,
        callback=audio_callback
    ):

        while not detected:

            try:

                data = audio_queue.get(
                    timeout=0.5
                )

            except queue.Empty:

                continue

            audio_16k = convert_audio(
                data
            )

            if recognizer.AcceptWaveform(
                audio_16k
            ):

                result = json.loads(
                    recognizer.Result()
                )

                text = result.get(
                    "text",
                    ""
                ).lower().strip()

                if not text:

                    continue

                print(
                    "HEARD:",
                    text,
                    flush=True
                )

                if "jarvis" in text:

                    detected = True

                    print()
                    print(
                        "==============================",
                        flush=True
                    )
                    print(
                        "JARVIS WAKE WORD DETECTED!",
                        flush=True
                    )
                    print(
                        "==============================",
                        flush=True
                    )
                    print()

    return True


# ============================================================
# LISTEN FOR COMMAND
# ============================================================

def listen_for_command():

    print()
    print(
        "Listening for your command...",
        flush=True
    )

    recognizer = KaldiRecognizer(
        model,
        VOSK_RATE
    )

    command_queue = queue.Queue(
        maxsize=20
    )

    command_done = False

    def command_callback(
        indata,
        frames,
        time_info,
        status
    ):

        if status:

            print(
                "COMMAND AUDIO:",
                status,
                flush=True
            )

        try:

            command_queue.put_nowait(
                bytes(indata)
            )

        except queue.Full:

            pass

    start_time = time.time()

    with sd.RawInputStream(
        samplerate=MIC_RATE,
        blocksize=BLOCKSIZE,
        device=MIC_DEVICE,
        dtype="int16",
        channels=CHANNELS,
        callback=command_callback
    ):

        while time.time() - start_time < 5:

            try:

                data = command_queue.get(
                    timeout=0.5
                )

            except queue.Empty:

                continue

            audio_16k = convert_audio(
                data
            )

            recognizer.AcceptWaveform(
                audio_16k
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
# CONTINUOUS CONVERSATION MODE
# ============================================================

def conversation_mode():

    print()
    print(
        "================================",
        flush=True
    )
    print(
        "    JARVIS CONVERSATION MODE",
        flush=True
    )
    print(
        "================================",
        flush=True
    )
    print()
    print(
        "Continuous conversation active.",
        flush=True
    )
    print(
        "Say 'sleep' to return to standby.",
        flush=True
    )
    print(
        "Say 'shutdown' to stop JARVIS.",
        flush=True
    )
    print()

    speak(
        "I'm listening, sir."
    )

    while True:

        try:

            command = listen_for_command()

            if not command:

                print(
                    "JARVIS: I didn't hear anything.",
                    flush=True
                )

                continue

            print()
            print(
                "YOU:",
                command,
                flush=True
            )

            command_lower = (
                command
                .lower()
                .strip()
            )

            # ------------------------------------------------
            # STANDBY
            # ------------------------------------------------

            if command_lower in [
                "sleep",
                "sleep jarvis",
                "go to sleep",
                "stop listening",
                "standby",
                "go standby"
            ]:

                speak(
                    "Going back to standby, sir."
                )

                return "standby"

            # ------------------------------------------------
            # SHUTDOWN
            # ------------------------------------------------

            if command_lower in [
                "exit",
                "quit",
                "shutdown",
                "goodbye",
                "bye"
            ]:

                speak(
                    "JARVIS shutting down, sir."
                )

                return "shutdown"

            # ------------------------------------------------
            # BRAIN
            # ------------------------------------------------

            print()
            print(
                "Thinking...",
                flush=True
            )

            response = jarvis_brain(
                command
            )

            # ------------------------------------------------
            # RESPONSE
            # ------------------------------------------------

            if response:

                speak(
                    response
                )

            else:

                speak(
                    "I don't have a response for that, sir."
                )

            time.sleep(
                0.3
            )

        except KeyboardInterrupt:

            print()

            speak(
                "JARVIS shutting down, sir."
            )

            return "shutdown"

        except Exception as e:

            print()
            print(
                "CONVERSATION ERROR:",
                e,
                flush=True
            )

            speak(
                "Sorry sir, something went wrong."
            )

            time.sleep(
                0.5
            )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print(
        "================================",
        flush=True
    )
    print(
        "          JARVIS ONLINE",
        flush=True
    )
    print(
        "================================",
        flush=True
    )
    print()

    speak(
        "JARVIS online. "
        "Say my name when you need me, sir."
    )

    while True:

        try:

            wait_for_wake_word()

            print()
            print(
                "WAKE WORD DETECTED!",
                flush=True
            )

            speak(
                "Yes sir?"
            )

            result = conversation_mode()

            if result == "shutdown":

                break

            if result == "standby":

                print()
                print(
                    "JARVIS returned to standby.",
                    flush=True
                )

                continue

        except KeyboardInterrupt:

            print()

            speak(
                "JARVIS shutting down, sir."
            )

            break

        except Exception as e:

            print()
            print(
                "MAIN ERROR:",
                e,
                flush=True
            )

            speak(
                "Sorry sir, "
                "I encountered an error."
            )

            time.sleep(
                1
            )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()