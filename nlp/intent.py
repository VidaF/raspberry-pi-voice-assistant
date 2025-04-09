import subprocess
import json
import re

OLLAMA_PATH = "/home/pi/ollama/ollama"
MODEL_NAME = "llama3.2:1b"

def fast_parse_command(text):
    text = text.lower()
    if "temperature" in text:
        return {"action": "temperature"}
    elif "servo" in text:
        if "left" in text:
            return {"action": "servo", "direction": "left"}
        elif "right" in text:
            return {"action": "servo", "direction": "right"}
        elif "center" in text:
            return {"action": "servo", "direction": "center"}
    return None

def parse_command(text):
    if not text:
        return None

    prompt = f"""
Your job is to convert a voice command into one of the following JSON intent formats.

ONLY respond with ONE of the following:
- {{ "action": "temperature" }}
- {{ "action": "servo", "direction": "left" }}
- {{ "action": "servo", "direction": "right" }}
- {{ "action": "servo", "direction": "center" }}
- {{ "action": "none" }}
If the input is unrelated, unclear, or not understood — respond with:
{{ "action": "none" }}
Do not add any explanation. Just return a JSON object like above.
ONLY return a valid JSON object. Do NOT prefix with `-` or wrap it in markdown or code blocks.
Input: "{text}"
"""

    try:
        result = subprocess.run(
            [OLLAMA_PATH, "run", MODEL_NAME, prompt],
            capture_output=True,
            text=True,
            timeout=60
        )

        output = result.stdout.strip()
        print("Raw Ollama output:", output)

        # Extract valid JSON object (first match)
        match = re.search(r'\{[\s\S]*?\}', output)
        if not match:
            print("[Intent Parser]  No JSON found in output.")
            return None

        json_str = match.group(0)
        return json.loads(json_str)

    except subprocess.TimeoutExpired:
        print("[Intent Parser] Ollama timed out.")
    except json.JSONDecodeError as e:
        print(f"[Intent Parser] JSON error: {e}")
    except Exception as e:
        print(f"[Intent Parser] Other error: {e}")

    return None
