from gpiozero import Servo
from time import sleep

# Global servo instance, starts as None
servo = None

# GPIO pin to control servo (e.g., 18 = physical pin 12)
SERVO_PIN = 18

def move_servo_direction(direction):
    """
    Moves the servo in the specified direction: 'left', 'right', or 'center'.
    Initializes the servo only on first use, and detaches after each move.
    """
    global servo

    if direction not in ["left", "right", "center"]:
        print(f"Invalid direction: {direction}")
        return

    if servo is None:
        print("Initializing servo...")
        servo = Servo(SERVO_PIN)

    print(f"Moving servo: {direction}")

    if direction == "left":
        servo.min()
    elif direction == "right":
        servo.max()
    elif direction == "center":
        servo.mid()

    sleep(0.5)  # Allow time to move

    print("Stopping servo signal.")
    servo.detach()
    servo.value = None
