#!/usr/bin/env python3
"""Example: Inverting axes

This example shows how to invert specific axes (e.g. x, roll, ... )
"""

import time

import pyspacemouse
from pyspacemouse import AxisConvention


def example_invert_rotations():
    """Show how to fix rotation axes for specific conventions."""
    print("\n" + "=" * 60)
    print("Example 2: Invert rotation conventions")
    print("=" * 60)

    connected = pyspacemouse.get_connected_devices()
    if not connected:
        print("No devices connected!")
        return

    specs = pyspacemouse.get_device_specs()
    base_spec_legacy = specs[connected[0]]
    base_spec = pyspacemouse.apply_axis_convention(base_spec_legacy, AxisConvention.HID_Z_UP)

    # Invert roll, pitch, and yaw so rotations are left-handed
    fixed_spec = pyspacemouse.modify_device_info(
        base_spec,
        name=f"{connected[0]} (Fixed Rotations)",
        # Translation axes (x, y, z) can also be inverted here
        invert_axes=["roll", "pitch", "yaw"],
    )

    with pyspacemouse.open(device_spec=fixed_spec) as device:
        print(f"Connected to: {device.name}")
        print("Rotations are now inverted!\n")

        for _ in range(500):
            state = device.read()
            if any([state.roll, state.pitch, state.yaw]):
                print(
                    f"x={state.x:+.2f} y={state.y:+.2f} z={state.z:+.2f} "
                    f"roll={state.roll:+.2f} pitch={state.pitch:+.2f} yaw={state.yaw:+.2f}"
                )
            time.sleep(0.01)


if __name__ == "__main__":
    try:
        example_invert_rotations()
    except KeyboardInterrupt:
        print("\nExiting...")
