"""Reading without busy-waiting or getting old/laggy data

Shows you how to read slowly and still get the most recent data.
"""

import time

import pyspacemouse
from pyspacemouse import AxisConvention

with pyspacemouse.open(axis_convention=AxisConvention.HID_Z_UP) as device:
    print(f"Connected to: {device.name}")
    print("Move the SpaceMouse to see values (Ctrl+C to exit)")

    while True:
        # with block=True, we avoid polling and wasting CPU,
        # because when the device is stationary at 0, it doesn't send any data.
        state = device.read_latest(block=True)

        # Note how we don't need to check state.has_motion() here,
        # because when there is no motion, the read_latest() just blocks.
        print(
            f"x={state.x:+.2f} y={state.y:+.2f} z={state.z:+.2f} "
            f"roll={state.roll:+.2f} pitch={state.pitch:+.2f} yaw={state.yaw:+.2f}"
        )

        # This sleep would cause problems if we used just device.read(),
        # but with read_latest(), we can read as slowly as we want!
        time.sleep(0.1)
