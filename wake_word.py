import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from rapidfuzz import fuzz


MODEL_PATH = "models/vosk-model-small-en-us-0.15"

MIC_DEVICE = 1
SAMPLE_RATE = 16000
CHANNELS = 1

WAKE_WORDS = [
    "jarvis",
    "jarvis sir",
    "hey jarvis",
    "okay jarvis",
    "ok jarvis",
]


print("Loading Vosk...")
model = Model(MODEL_PATH)
print("Vosk loaded.")


recognizer = KaldiRecognizer(
    model,
    SAMPLE_RATE
)


def callback(indata, frames, time, status):

    if status:
        print("Audio:", status)

    data = bytes(indata)

    if recognizer.AcceptWaveform(data):

        result = json.loads(
            recognizer.Result()
        )

        text = result.get("text", "").lower().strip()

        if not text:
            return

        print("HEARD:", text)

        for wake_word in WAKE_WORDS:

            score = fuzz.partial_ratio(
                wake_word,
                text
            )

            if score >= 75:

                print()
                print("==============================")
                print("🔥 JARVIS WAKE WORD DETECTED!")
                print("==============================")
                print()

                recognizer.Reset()

                break


print()
print("==============================")
print("       JARVIS WAKE WORD")
print("==============================")
print()
print("Say: Jarvis")
print("Press CTRL+C to stop.")
print()


try:

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        device=MIC_DEVICE,
        dtype="int16",
        channels=CHANNELS,
        callback=callback
    ):

        while True:
            sd.sleep(1000)


except KeyboardInterrupt:

    print()
    print("Wake word detector stopped.")