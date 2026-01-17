"""Axis callbacks example: React to specific axis movements.

This example shows DofCallback for per-axis handling with:
- Positive/negative direction callbacks
- Filtering (deadzone)
- Rate limiting (sleep)
"""

import time

import pyspacemouse


def on_x_positive(state, value):
    """Called when X axis moves positive (right)."""
    print(f"→ X positive: {value:+.2f}")


def on_x_negative(state, value):
    """Called when X axis moves negative (left)."""
    print(f"← X negative: {value:+.2f}")


def on_z_move(state, value):
    """Called when Z axis moves (up/down)."""
    direction = "↑ UP" if value > 0 else "↓ DOWN"
    print(f"{direction}: {abs(value):.2f}")


# Configure per-axis callbacks
dof_callbacks = [
    # X axis with separate callbacks for positive/negative
    pyspacemouse.DofCallback(
        axis="x",
        callback=on_x_positive,
        callback_minus=on_x_negative,
        filter=0.1,  # Deadzone: ignore values < 0.1
        sleep=0.1,  # Rate limit: max 10 calls/second
    ),
    # Z axis with single callback for both directions
    pyspacemouse.DofCallback(
        axis="z",
        callback=on_z_move,
        filter=0.15,
        sleep=0.05,
    ),
]

with pyspacemouse.open(dof_callbacks=dof_callbacks) as device:
    print(f"Connected to: {device.name}")
    print("Move X axis (left/right) or Z axis (up/down)")
    print("Ctrl+C to exit")
    print()

    while True:
        device.read()
        time.sleep(0.01)
