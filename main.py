import os
import time
import numpy as np
import sounddevice as sd
from queue import Empty

from audio.mic_stream import start_mic_stream, audio_q
from actions.temp_sensor import get_temperature_and_humidity
from actions.servo import move_servo_direction
from nlp.intent import parse_command, fast_parse_command

import whisper

AUDIO_RATE = 16000
AUDIO_BLOCK_SIZE = 1024
SEGMENT_SECONDS =  3.0
CHUNKS_PER_SEGMENT = int(SEGMENT_SECONDS * AUDIO_RATE / AUDIO_BLOCK_SIZE)

model = whisper.load_model("tiny.en")

def transcribe_audio_from_buffer(frames):
    if frames.ndim == 1:
        frames = frames.reshape(-1, 1)

    print(f"Audio duration: {len(frames) / AUDIO_RATE:.2f} sec")
    # Convert int16 → float32 (normalize from -1 to 1)
    audio_np = frames.flatten().astype(np.float32) / 32768.0

    try:
        result = model.transcribe(audio_np, fp16=False)
        text = result["text"].strip()
        print(f"Transcription result: {text}")
        return text
    except Exception as e:
        print(f"Transcription error: {e}")
        return None

def handle_command(text):
    print(f"Heard: {text}")
    intent = fast_parse_command(text)
    if not intent:
        intent = parse_command(text)

    if not intent:
        print("Could not parse intent.")
        return

    action = intent.get("action", "").lower()
    if "temp" in action:
        temp, hum = get_temperature_and_humidity()
        print(f"Temp: {temp}°C |  Humidity: {hum}%")
    elif "servo" in action:
        direction = intent.get("direction", "center")
        print(f"Moving servo: {direction}")
        move_servo_direction(direction)
    else:
        print("Unknown action.")

def main():
    print("Starting voice assistant...")
    print("Default device:", sd.default.device)

    stream = start_mic_stream()
    buffer = []

    try:
        while True:
            buffer.clear()
            print("Listening for command...")

            while len(buffer) < CHUNKS_PER_SEGMENT:
                try:
                    chunk = audio_q.get(timeout=1)
                    buffer.append(chunk)
                except Empty:
                    print("No audio. Retrying...")

            print("Captured full segment. Processing...")
            stream.stop()

            audio = np.concatenate(buffer, axis=0)
            text = transcribe_audio_from_buffer(audio)

            if text:
                handle_command(text)
            else:
                print("No transcription.")

            # Flush queue
            while not audio_q.empty():
                audio_q.get_nowait()

            time.sleep(0.5)
            stream.start()

    except KeyboardInterrupt:
        print("Exiting...")
        stream.stop()
        stream.close()

if __name__ == "__main__":
    main()
