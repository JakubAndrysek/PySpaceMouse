"""Basic example: Read SpaceMouse input with context manager.

This is the simplest way to use PySpaceMouse. The context manager
ensures the device is properly closed when you're done.
"""

import time

import pyspacemouse

# Using context manager (recommended)
with pyspacemouse.open() as device:
    print(f"Connected to: {device.name}")
    print("Move the SpaceMouse to see values (Ctrl+C to exit)")

    while True:
        state = device.read()

        if any(
            abs(val) > 0.01
            for val in [state.x, state.y, state.z, state.roll, state.pitch, state.yaw]
        ):
            print(
                f"x={state.x:+.2f} y={state.y:+.2f} z={state.z:+.2f} "
                f"roll={state.roll:+.2f} pitch={state.pitch:+.2f} yaw={state.yaw:+.2f}"
            )
        time.sleep(0.01)
