import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from actions.temp_sensor import get_temperature_and_humidity

def test_real_temp_sensor():
    print("\nReading DHT11 sensor...")
    retries = 3
    for attempt in range(retries):
        try:
            temp, hum = get_temperature_and_humidity()

            assert isinstance(temp, (float, int)), "Temperature should be a number"
            assert isinstance(hum, (float, int)), "Humidity should be a number"
            assert 0 <= temp <= 60, f"Temperature out of expected range: {temp}°C"
            assert 0 <= hum <= 100, f"Humidity out of expected range: {hum}%"

            print(f"Temp: {temp}°C |  Humidity: {hum}%")
            return  # Success!

        except Exception as e:
            print(f"Attempt {attempt+1}/{retries} failed: {e}")
            time.sleep(2)

    assert False, "Failed to read valid temperature/humidity after 3 attempts"
