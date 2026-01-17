"""LED control example: Blink the SpaceMouse LED.

This example demonstrates how to control the LED on SpaceMouse devices.
The LED will toggle on and off every 0.5 seconds.

Note: Not all devices have controllable LEDs.
"""

import time

import pyspacemouse

# Using context manager (recommended)
with pyspacemouse.open() as device:
    print(f"Connected to: {device.name}")
    print("LED will blink every 0.5 seconds (Ctrl+C to exit)")
    print()

    led_state = True
    while True:
        device.set_led(led_state)
        led_state = not led_state
        time.sleep(0.5)
