#!/usr/bin/env python3
"""Example: Custom device configuration

This example shows how to create entirely custom device configurations,
In this case for a "Spacemouse Wireless New", following the left-handed Unity convention (Z forward, X right, Y up).
If you have a totally custom HID device, you just need to know the byte layout of the device and you can create a custom configuration for it.
"""

import time

import pyspacemouse


def example_unity_convention():
    """Create entirely custom device configuration with the Unity convention."""
    print("\n" + "=" * 60)
    print("Create custom device spec (Unity convention)")
    print("=" * 60)

    # This shows how to create a completely custom device spec
    # Useful for unsupported devices or complete remapping
    custom_spec = pyspacemouse.create_device_info(
        name="CustomSpaceMouse",
        vendor_id=0x256F,  # 3Dconnexion
        product_id=0xC63A,  # SpaceMouse Wireless New
        mappings={
            # Each mapping: (channel, byte1, byte2, scale)
            # Scale: 1 = normal direction, -1 = inverted
            "x": (1, 1, 2, 1),
            "y": (1, 5, 6, -1),
            "z": (1, 3, 4, -1),
            "yaw": (1, 9, 10, 1),
            "pitch": (1, 11, 12, 1),
            "roll": (1, 7, 8, -1),
        },
        buttons={
            "LEFT": (3, 1, 0),
            "RIGHT": (3, 1, 1),
        },
    )

    print(f"Created custom Unity spec: {custom_spec.name}")
    print(f"  VID/PID: {custom_spec.vendor_id:#06x}/{custom_spec.product_id:#06x}")
    print(f"  Axes: {list(custom_spec.mappings.keys())}")
    print(f"  Buttons: {custom_spec.button_names}")

    with pyspacemouse.open(device_spec=custom_spec) as device:
        print(f"Connected to: {device.name} with custom spec")

        for _ in range(5000):
            state = device.read()
            if any([state.x, state.y, state.z, state.roll, state.pitch, state.yaw]):
                print(
                    f"x={state.x:+.2f} y={state.y:+.2f} z={state.z:+.2f} "
                    f"roll={state.roll:+.2f} pitch={state.pitch:+.2f} yaw={state.yaw:+.2f}"
                )
            time.sleep(0.01)


if __name__ == "__main__":
    try:
        example_unity_convention()
    except KeyboardInterrupt:
        print("\nExiting...")
