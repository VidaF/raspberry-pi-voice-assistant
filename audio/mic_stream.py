import sounddevice as sd
import numpy as np
from queue import Queue

AUDIO_RATE = 16000         # Whisper-compatible
AUDIO_BLOCK_SIZE = 1024
audio_q = Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(f"Audio callback status: {status}")
    audio_q.put(indata.copy())
    #print(f "Captured chunk: shape={indata.shape}, dtype={indata.dtype}")

def start_mic_stream(device=None):
    print(f"Starting mic stream at {AUDIO_RATE}Hz...")

    stream = sd.InputStream(
        samplerate=AUDIO_RATE,
        blocksize=AUDIO_BLOCK_SIZE,
        channels=1,
        dtype='int16',
        callback=audio_callback,
        device=device
    )
    stream.start()
    return stream

