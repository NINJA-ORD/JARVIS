import json
import time
import queue
import sounddevice as sd

from vosk import Model, KaldiRecognizer
from rapidfuzz import fuzz


MODEL_PATH = "models/vosk-model-small-en-us-0.15"

MIC_DEVICE = 1
SAMPLE_RATE = 16000
CHANNELS = 1
BLOCKSIZE = 2000

WAKE_WORDS = [
    "jarvis",
    "jarvis sir",
    "hey jarvis",
    "okay jarvis",
    "ok jarvis",
]


print("Loading Vosk model...", flush=True)

model = Model(MODEL_PATH)

print("Vosk loaded.", flush=True)


audio_queue = queue.Queue(maxsize=20)


def callback(indata, frames, time_info, status):

    if status:
        print("AUDIO STATUS:", status, flush=True)

    try:
        audio_queue.put_nowait(bytes(indata))
    except queue.Full:
        pass


recognizer = KaldiRecognizer(
    model,
    SAMPLE_RATE
)


print()
print("==============================")
print("       WAKE WORD TEST")
print("==============================")
print()
print("Say: Jarvis")
print()


detected = False


with sd.RawInputStream(
    samplerate=SAMPLE_RATE,
    blocksize=BLOCKSIZE,
    device=MIC_DEVICE,
    dtype="int16",
    channels=CHANNELS,
    callback=callback
):

    while not detected:

        try:
            data = audio_queue.get(timeout=0.5)

        except queue.Empty:
            continue

        if recognizer.AcceptWaveform(data):

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

                    break


print(
    "WAKE TEST SUCCESS",
    flush=True
)