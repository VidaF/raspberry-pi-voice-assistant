import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nlp.intent import parse_command

def test_parse_temperature_command():
    command = "what's the temperature?"
    intent = parse_command(command)
    print(f"Command: {command}\n Intent: {intent}\n")
    assert isinstance(intent, dict)
    assert "action" in intent

def test_parse_servo_left():
    command = "turn servo left"
    intent = parse_command(command)
    print(f"Command: {command}\nIntent: {intent}\n")
    assert isinstance(intent, dict)
    assert intent.get("action") == "servo"

def test_parse_unknown_but_flexible():
    command = "sing me a song"
    intent = parse_command(command)
    print(f"Command: {command}\nIntent: {intent}\n")
    assert isinstance(intent, dict)  # allow guessing
