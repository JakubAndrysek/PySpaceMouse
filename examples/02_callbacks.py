"""Callbacks example: React to button presses and axis movements.

This example shows how to use callbacks for:
- Button presses (individual or combinations)
- Axis movements with filtering
"""

import time

import pyspacemouse


# Button callbacks receive (state, buttons, pressed_buttons)
def on_button_left(state, buttons, pressed):
    print("LEFT button pressed!")


def on_button_right(state, buttons, pressed):
    print("RIGHT button pressed!")


def on_both_buttons(state, buttons, pressed):
    print("BOTH buttons pressed together!")


# General button callback for any button change
def on_any_button(state, buttons):
    active = [i for i, b in enumerate(buttons) if b]
    if active:
        print(f"Buttons active: {active}")


# Configure button callbacks
button_callbacks = [
    pyspacemouse.ButtonCallback(0, on_button_left),
    pyspacemouse.ButtonCallback(1, on_button_right),
    pyspacemouse.ButtonCallback([0, 1], on_both_buttons),  # Both at once
]

# Open with callbacks
with pyspacemouse.open(
    dof_callback=pyspacemouse.print_state,  # Built-in DOF printer
    button_callback=on_any_button,
    button_callbacks=button_callbacks,
) as device:
    print(f"Connected to: {device.name}")
    print("Move the SpaceMouse or press buttons (Ctrl+C to exit)")
    print()

    while True:
        device.read()  # Must call read() to process callbacks
        time.sleep(0.01)
