#!/usr/bin/env python3
"""Example: Custom device configuration with axis remapping.

This example shows how to:
1. Get existing device specs
2. Modify axis directions for ROS/other conventions
3. Create entirely custom device configurations
"""

import time

import pyspacemouse


def example_modify_existing():
    """Modify an existing device spec to invert axes."""
    print("=" * 60)
    print("Example 1: Modify existing device spec")
    print("=" * 60)

    # Get all device specs from TOML
    specs = pyspacemouse.get_device_specs()
    print(f"Available devices: {list(specs.keys())}")

    # Get connected devices
    connected = pyspacemouse.get_connected_devices()
    if not connected:
        print("No devices connected!")
        return

    device_name = connected[0]
    print(f"Using device: {device_name}")

    # Get base spec and create modified version
    base_spec = specs[device_name]
    print(f"Original mappings: y scale = {base_spec.mappings['y'].scale}")

    # Create modified spec with inverted Y and Z (common for ROS)
    ros_spec = pyspacemouse.modify_device_info(
        base_spec,
        name=f"{device_name} (ROS)",
        invert_axes=["y", "z"],  # Invert these axes
    )
    print(f"Modified mappings: y scale = {ros_spec.mappings['y'].scale}")

    # Open with custom spec
    with pyspacemouse.open(device_spec=ros_spec) as device:
        print(f"\nConnected to: {device.name}")
        print("Move the SpaceMouse (Ctrl+C to exit)")
        print("Y and Z axes are now inverted!\n")

        for _ in range(50):  # Run for ~5 seconds
            state = device.read()
            if any([state.x, state.y, state.z]):
                print(f"x={state.x:+.2f} y={state.y:+.2f} z={state.z:+.2f} (Y/Z inverted)")
            time.sleep(0.1)


def example_invert_rotations():
    """Show how to fix rotation axes for specific conventions."""
    print("\n" + "=" * 60)
    print("Example 2: Fix rotation conventions")
    print("=" * 60)

    connected = pyspacemouse.get_connected_devices()
    if not connected:
        print("No devices connected!")
        return

    specs = pyspacemouse.get_device_specs()
    base_spec = specs[connected[0]]

    # Invert roll and yaw for right-handed coordinate system
    fixed_spec = pyspacemouse.modify_device_info(
        base_spec,
        name=f"{connected[0]} (Fixed Rotations)",
        invert_axes=["roll", "yaw"],
    )

    with pyspacemouse.open(device_spec=fixed_spec) as device:
        print(f"Connected to: {device.name}")
        print("Roll and Yaw are now inverted!\n")

        for _ in range(30):
            state = device.read()
            if any([state.roll, state.pitch, state.yaw]):
                print(f"roll={state.roll:+.2f} pitch={state.pitch:+.2f} yaw={state.yaw:+.2f}")
            time.sleep(0.1)


def example_create_custom():
    """Create entirely custom device configuration."""
    print("\n" + "=" * 60)
    print("Example 3: Create custom device spec (reference)")
    print("=" * 60)

    # This shows how to create a completely custom device spec
    # Useful for unsupported devices or complete remapping
    custom_spec = pyspacemouse.create_device_info(
        name="CustomSpaceMouse",
        vendor_id=0x256F,  # 3Dconnexion
        product_id=0xC635,  # SpaceMouse Compact
        mappings={
            # Each mapping: (channel, byte1, byte2, scale)
            # Scale: 1 = normal direction, -1 = inverted
            "x": (1, 1, 2, 1),
            "y": (1, 3, 4, 1),  # NOT inverted (unlike default)
            "z": (1, 5, 6, 1),  # NOT inverted (unlike default)
            "pitch": (2, 1, 2, 1),  # NOT inverted
            "roll": (2, 3, 4, 1),  # NOT inverted
            "yaw": (2, 5, 6, 1),
        },
        buttons={
            "LEFT": (3, 1, 0),
            "RIGHT": (3, 1, 1),
        },
    )

    print(f"Created custom spec: {custom_spec.name}")
    print(f"  VID/PID: {custom_spec.vendor_id:#06x}/{custom_spec.product_id:#06x}")
    print(f"  Axes: {list(custom_spec.mappings.keys())}")
    print(f"  Buttons: {custom_spec.button_names}")
    print("\n  (Not opening - this is just to show the API)")


if __name__ == "__main__":
    try:
        example_modify_existing()
        example_invert_rotations()
        example_create_custom()
    except KeyboardInterrupt:
        print("\nExiting...")
