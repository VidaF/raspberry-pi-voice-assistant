import time
import board
import adafruit_dht

# DHT11 sensor on GPIO4 (pin 7)
dht_sensor = adafruit_dht.DHT11(board.D4)

def get_temperature_and_humidity():
    try:
        temperature = dht_sensor.temperature
        humidity = dht_sensor.humidity

        if temperature is None or humidity is None:
            raise RuntimeError("Sensor returned None values.")

        return float(round(temperature, 2)), float(round(humidity, 2))

    except RuntimeError as e:
        raise RuntimeError(f"Reading error: {e}")
