import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from actions.servo import move_servo_direction
import time

def test_servo_real_left():
    print("\nMoving servo LEFT")
    move_servo_direction("left")
    time.sleep(1)

def test_servo_real_center():
    print("\nMoving servo CENTER")
    move_servo_direction("center")
    time.sleep(1)

def test_servo_real_right():
    print("\nMoving servo RIGHT")
    move_servo_direction("right")
    time.sleep(1)
