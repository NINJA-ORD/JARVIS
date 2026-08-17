import json
import queue
import sounddevice as sd
import numpy as np

from scipy.signal import resample_poly
from vosk import Model, KaldiRecognizer


MODEL_PATH = "models/vosk-model-small-en-us-0.15"

MIC_DEVICE = 1

MIC_RATE = 48000
VOSK_RATE = 16000

CHANNELS = 1
BLOCKSIZE = 4800


print("Loading Vosk model...", flush=True)

model = Model(MODEL_PATH)

print("Vosk loaded.", flush=True)


# Only allow wake-word related recognition
grammar = json.dumps([
    "jarvis",
    "jarvis sir",
    "hey jarvis",
    "okay jarvis",
    "ok jarvis",
    "[unk]"
])


recognizer = KaldiRecognizer(
    model,
    VOSK_RATE,
    grammar
)


audio_queue = queue.Queue(maxsize=20)


def callback(indata, frames, time_info, status):

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
        pass


print()
print("==============================")
print("     JARVIS GRAMMAR TEST")
print("==============================")
print()
print("Say: Jarvis")
print()


with sd.RawInputStream(
    samplerate=MIC_RATE,
    blocksize=BLOCKSIZE,
    device=MIC_DEVICE,
    dtype="int16",
    channels=CHANNELS,
    callback=callback
):

    while True:

        try:
            data = audio_queue.get(
                timeout=0.5
            )

        except queue.Empty:
            continue

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

            if text:

                print(
                    "HEARD:",
                    text,
                    flush=True
                )

                if "jarvis" in text:

                    print()
                    print("==============================")
                    print("🔥 JARVIS DETECTED!")
                    print("==============================")
                    print()

                    break