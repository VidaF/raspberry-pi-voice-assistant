import sys
import os
import time
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from audio.mic_stream import start_mic_stream, audio_q

def test_mic_captures_non_silent_chunk():
    stream = start_mic_stream()
    try:
        time.sleep(5.0)  # Let audio buffer fill a bit

        chunk = audio_q.get(timeout=3)
        assert chunk is not None
        assert chunk.shape[0] > 0

        # New: Check that the audio is not completely silent
        is_silent = np.all(chunk == 0)
        assert not is_silent, "Captured chunk is completely silent. Is the mic off?"

    finally:
        stream.stop()
        stream.close()
