import sounddevice as sd
import time

blocks = 0


def callback(indata, frames, time_info, status):

    global blocks

    if status:
        print("STATUS:", status, flush=True)

    blocks += 1

    print(
        "AUDIO BLOCK:",
        blocks,
        "frames:",
        frames,
        flush=True
    )


print("Testing callback...", flush=True)

with sd.RawInputStream(
    samplerate=16000,
    blocksize=4000,
    device=1,
    dtype="int16",
    channels=1,
    callback=callback
):

    time.sleep(5)

print("CALLBACK TEST DONE", flush=True)
