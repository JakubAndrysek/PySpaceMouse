"""Helper functions for creating custom device configurations.

This module provides utilities to create and modify DeviceInfo objects
for custom axis mappings and device configurations.

Example:
    import pyspacemouse
    from pyspacemouse import create_device_info, modify_device_info

    # Modify existing device to invert Y axis
    specs = pyspacemouse.get_device_specs()
    base = specs["SpaceNavigator"]
    custom = modify_device_info(base, invert_axes=["y", "pitch"])

    with pyspacemouse.open(device_spec=custom) as device:
        state = device.read()
"""

from __future__ import annotations

from .types import AxisSpec, ButtonSpec, DeviceInfo


def create_device_info(
    name: str,
    vendor_id: int,
    product_id: int,
    mappings: dict[str, tuple[int, int, int, int]],
    buttons: dict[str, tuple[int, int, int]] | None = None,
    led_id: tuple[int, int] | None = None,
    axis_scale: float = 350.0,
) -> DeviceInfo:
    """Create a DeviceInfo from Python dictionaries.

    This allows defining custom device configurations entirely in Python
    without modifying the devices.toml file.

    Args:
        name: Human-readable device name
        vendor_id: USB vendor ID (e.g., 0x256F for 3Dconnexion)
        product_id: USB product ID
        mappings: Dict mapping axis names to (channel, byte1, byte2, scale).
                  Valid axes: x, y, z, roll, pitch, yaw
        buttons: Optional dict mapping button names to (channel, byte, bit)
        led_id: Optional tuple (report_id, on_value) for LED control
        axis_scale: Scaling factor for axis values (default 350.0)

    Returns:
        DeviceInfo instance ready for use with open()

    Example:
        custom = create_device_info(
            name="MyCustomDevice",
            vendor_id=0x256F,
            product_id=0xC635,
            mappings={
                "x": (1, 1, 2, 1),
                "y": (1, 3, 4, -1),  # Inverted
                "z": (1, 5, 6, -1),
                "pitch": (2, 1, 2, -1),
                "roll": (2, 3, 4, -1),
                "yaw": (2, 5, 6, 1),
            },
            buttons={"LEFT": (3, 1, 0), "RIGHT": (3, 1, 1)},
        )
    """
    # Parse mappings
    axis_specs = {}
    for axis, values in mappings.items():
        axis_specs[axis] = AxisSpec(
            channel=values[0],
            byte1=values[1],
            byte2=values[2],
            scale=values[3],
        )

    # Parse buttons
    button_specs = []
    button_names = []
    if buttons:
        for btn_name, values in buttons.items():
            button_names.append(btn_name)
            button_specs.append(ButtonSpec(channel=values[0], byte=values[1], bit=values[2]))

    return DeviceInfo(
        name=name,
        vendor_id=vendor_id,
        product_id=product_id,
        led_id=led_id,
        axis_scale=axis_scale,
        mappings=axis_specs,
        button_specs=tuple(button_specs),
        button_names=tuple(button_names),
    )


def modify_device_info(
    base: DeviceInfo,
    name: str | None = None,
    invert_axes: list[str] | None = None,
    axis_scale: float | None = None,
) -> DeviceInfo:
    """Create a modified DeviceInfo from an existing one.

    This is useful for adjusting axis conventions without redefining
    the entire device configuration.

    Args:
        base: Existing DeviceInfo to modify
        name: Optional new name for the device
        invert_axes: List of axis names to invert (e.g., ["y", "roll"])
        axis_scale: Optional new axis scale value

    Returns:
        New DeviceInfo with modifications applied

    Example:
        # Get existing device spec and invert axes for ROS conventions
        specs = pyspacemouse.get_device_specs()
        base = specs["SpaceNavigator"]
        ros_compatible = modify_device_info(
            base,
            name="SpaceNavigator (ROS)",
            invert_axes=["y", "z", "roll", "yaw"],
        )
    """
    # Start with base values
    new_name = name if name is not None else base.name
    new_scale = axis_scale if axis_scale is not None else base.axis_scale

    # Copy and optionally invert mappings
    new_mappings = {}
    for axis, spec in base.mappings.items():
        if invert_axes and axis in invert_axes:
            new_mappings[axis] = AxisSpec(
                channel=spec.channel,
                byte1=spec.byte1,
                byte2=spec.byte2,
                scale=-spec.scale,  # Invert
            )
        else:
            new_mappings[axis] = spec

    return DeviceInfo(
        name=new_name,
        vendor_id=base.vendor_id,
        product_id=base.product_id,
        led_id=base.led_id,
        axis_scale=new_scale,
        mappings=new_mappings,
        button_specs=base.button_specs,
        button_names=base.button_names,
    )
