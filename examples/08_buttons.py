"""Button names example: Show button names when pressed.

This example demonstrates how to get the configured button names
from devices.toml when buttons are pressed.
"""

import time

import pyspacemouse


def on_button_change(state, buttons):
    """Print names of all currently pressed buttons."""
    # Find indices of pressed buttons
    pressed_indices = [i for i, b in enumerate(buttons) if b]

    if pressed_indices:
        # Get button names from device
        names = [device.get_button_name(i) for i in pressed_indices]
        print(f"Pressed: {', '.join(names)}")


# Open device
with pyspacemouse.open(button_callback=on_button_change) as device:
    print(f"Connected to: {device.name}")
    print(f"Device has {len(device.info.button_names)} buttons:")
    for i, name in enumerate(device.info.button_names):
        print(f"  [{i}] {name}")
    print()
    print("Press buttons to see their names (Ctrl+C to exit)")
    print()

    while True:
        device.read()
        time.sleep(0.01)
