import json
import queue
import time

import numpy as np
import sounddevice as sd
from scipy.signal import resample_poly
from vosk import Model, KaldiRecognizer
from rapidfuzz import fuzz


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
# VOSK
# ============================================================

print("Loading Vosk model...", flush=True)

model = Model(MODEL_PATH)

print("Vosk loaded.", flush=True)

recognizer = KaldiRecognizer(
    model,
    VOSK_RATE
)


# ============================================================
# AUDIO QUEUE
# ============================================================

audio_queue = queue.Queue(maxsize=20)


def callback(indata, frames, time_info, status):

    if status:
        print(
            "AUDIO STATUS:",
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
# WAKE WORD TEST
# ============================================================

print()
print("==============================")
print("   48kHz -> 16kHz WAKE TEST")
print("==============================")
print()
print("Say: Jarvis")
print()


detected = False


with sd.RawInputStream(
    samplerate=MIC_RATE,
    blocksize=BLOCKSIZE,
    device=MIC_DEVICE,
    dtype="int16",
    channels=CHANNELS,
    callback=callback
):

    while not detected:

        try:

            data = audio_queue.get(
                timeout=0.5
            )

        except queue.Empty:

            continue

        # ----------------------------------------------------
        # 48 kHz INT16
        # ----------------------------------------------------

        audio_48k = np.frombuffer(
            data,
            dtype=np.int16
        )

        # ----------------------------------------------------
        # 48 kHz -> 16 kHz
        # ----------------------------------------------------

        audio_16k = resample_poly(
            audio_48k,
            VOSK_RATE,
            MIC_RATE
        )

        audio_16k = np.asarray(
            audio_16k,
            dtype=np.int16
        )

        # ----------------------------------------------------
        # VOSK
        # ----------------------------------------------------

        if recognizer.AcceptWaveform(
            audio_16k.tobytes()
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

            # ------------------------------------------------
            # WAKE WORD MATCH
            # ------------------------------------------------

            for wake_word in WAKE_WORDS:

                score = fuzz.partial_ratio(
                    wake_word,
                    text
                )

                print(
                    "MATCH:",
                    wake_word,
                    score,
                    flush=True
                )

                if score >= 75:

                    detected = True

                    print()
                    print(
                        "=============================="
                    )
                    print(
                        "JARVIS WAKE WORD DETECTED!"
                    )
                    print(
                        "=============================="
                    )
                    print()

                    break


print(
    "WAKE TEST SUCCESS",
    flush=True
)