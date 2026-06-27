"""Helper functions for creating custom device configurations.

This module provides utilities to create and modify DeviceInfo objects
for custom axis mappings and device configurations.

Example:
    import pyspacemouse
    from pyspacemouse import modify_device_info

    # Grab a built-in spec and invert Y in its current convention.
    specs = pyspacemouse.get_device_specs()
    custom = modify_device_info(specs["SpaceNavigator"], invert_axes=["y"])

    with pyspacemouse.open(device_spec=custom) as device:
        state = device.read()
"""

from __future__ import annotations

from typing import Dict, Literal, Tuple, Union

from .types import AXIS_NAMES, Axis, AxisConvention, AxisSpec, ButtonSpec, DeviceInfo

# Maps each *output* axis to the *source* axis whose data it should read,
# optionally with a sign. Direction is output <- source:
#   {"x": "z"}            output x reads source z          (sign +1)
#   {"x": ("z", -1)}      output x reads source z, negated
#   {"x": "y", "y": "x"}  swap x and y (applied atomically; see modify_device_info)
# typing.Dict/Tuple/Union (not PEP 604) is required: this alias is evaluated at
# runtime and must import on Python 3.8.
AxisRemap = Dict[Axis, Union[Axis, Tuple[Axis, Literal[-1, 1]]]]

# Remaps from the HID convention to each named convention.
_HID_TO_CONVENTION: dict[AxisConvention, AxisRemap] = {
    AxisConvention.LEGACY: {
        "x": ("x", 1),
        "y": ("y", -1),
        "z": ("z", -1),
        "roll": ("pitch", -1),
        "pitch": ("roll", -1),
        "yaw": ("yaw", 1),
    },
    AxisConvention.HID_Z_UP: {
        "x": ("x", 1),
        "y": ("y", -1),
        "z": ("z", -1),
        "roll": ("roll", 1),
        "pitch": ("pitch", -1),
        "yaw": ("yaw", -1),
    },
    AxisConvention.ROS: {
        "x": ("y", -1),
        "y": ("x", -1),
        "z": ("z", -1),
        "roll": ("pitch", -1),
        "pitch": ("roll", -1),
        "yaw": ("yaw", -1),
    },
    AxisConvention.UNITY: {
        "x": ("x", 1),
        "y": ("z", -1),
        "z": ("y", -1),
        "roll": ("roll", -1),
        "pitch": ("yaw", 1),
        "yaw": ("pitch", 1),
    },
}


def _parse_axis_remap(
    target_axis: str, remap: Axis | tuple[Axis, Literal[-1, 1]]
) -> tuple[Axis, int]:
    if target_axis not in AXIS_NAMES:
        raise ValueError(f"Unknown target axis: {target_axis!r}. Valid axes: {list(AXIS_NAMES)}")

    if isinstance(remap, tuple):
        source_axis, sign = remap
    else:
        source_axis, sign = remap, 1

    if source_axis not in AXIS_NAMES:
        raise ValueError(f"Unknown source axis: {source_axis!r}. Valid axes: {list(AXIS_NAMES)}")
    if sign not in (-1, 1):
        raise ValueError(f"Axis remap sign for {target_axis!r} must be 1 or -1.")

    return source_axis, sign


def _copy_axis_spec(spec: AxisSpec, sign: int = 1) -> AxisSpec:
    return AxisSpec(
        channel=spec.channel,
        byte1=spec.byte1,
        byte2=spec.byte2,
        scale=spec.scale * sign,
    )


def _normalize_to_hid(spec: DeviceInfo) -> DeviceInfo:
    """Convert any named-convention DeviceInfo to HID convention.

    For LEGACY input, applies the LEGACY→HID forward remap.
    For any other named convention C, inverts the HID→C remap: because
    sign ∈ {-1, 1}, the inverse has the same sign, only source and target
    are swapped.
    """
    if spec.convention == AxisConvention.HID:
        return spec

    if spec.convention not in _HID_TO_CONVENTION:
        raise ValueError(
            f"Cannot normalize {spec.convention!r} to HID — only named conventions "
            "can be automatically normalized. "
            "A spec with no convention (None) has no defined inverse."
        )

    # Invert HID→C to get C→HID:
    # HID[hid_target] = C[c_source] * sign  →  C[c_source] = HID[hid_target] * sign
    new_mappings = {}
    for hid_target, src in _HID_TO_CONVENTION[spec.convention].items():
        c_source, sign = _parse_axis_remap(hid_target, src)
        new_mappings[hid_target] = _copy_axis_spec(spec.mappings[c_source], sign)

    return DeviceInfo(
        name=spec.name,
        vendor_id=spec.vendor_id,
        product_id=spec.product_id,
        led_id=spec.led_id,
        axis_scale=spec.axis_scale,
        mappings=new_mappings,
        button_specs=spec.button_specs,
        button_names=spec.button_names,
        convention=AxisConvention.HID,
    )


def create_device_info(
    name: str,
    vendor_id: int,
    product_id: int,
    mappings: dict[str, tuple[int, int, int, int]],
    buttons: dict[str, tuple[int, int, int]] | None = None,
    led_id: tuple[int, int] | None = None,
    axis_scale: float = 350.0,
    convention: AxisConvention | None = None,
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
        convention: Axis convention used by the spec, or None for a spec
                    that follows no named convention (default None).

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
    axis_specs = {}
    for axis, values in mappings.items():
        axis_specs[axis] = AxisSpec(
            channel=values[0],
            byte1=values[1],
            byte2=values[2],
            scale=values[3],
        )

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
        convention=convention,
    )


def apply_axis_convention(base: DeviceInfo, convention: AxisConvention) -> DeviceInfo:
    """Convert a DeviceInfo from any named convention to another.

    Normalizes the input to HID first (via _normalize_to_hid), then applies
    the HID→target remap from _HID_TO_CONVENTION.  Works for any pair of named
    conventions.

    Args:
        base: DeviceInfo in any named convention (LEGACY, HID, ROS, …).
        convention: Target AxisConvention.

    Returns:
        New DeviceInfo in the requested convention.  Returns *base* unchanged
        if it is already in the requested convention.

    Raises:
        ValueError: If base has no named convention (convention is None) and so
            cannot be normalized to HID.
    """
    convention = AxisConvention(convention)

    if base.convention == convention:
        return base

    hid_base = _normalize_to_hid(base)

    if convention == AxisConvention.HID:
        return hid_base

    remap = _HID_TO_CONVENTION[convention]
    new_mappings = dict(hid_base.mappings)
    for target_axis, src in remap.items():
        source_axis, sign = _parse_axis_remap(target_axis, src)
        new_mappings[target_axis] = _copy_axis_spec(hid_base.mappings[source_axis], sign)

    return DeviceInfo(
        name=base.name,
        vendor_id=base.vendor_id,
        product_id=base.product_id,
        led_id=base.led_id,
        axis_scale=base.axis_scale,
        mappings=new_mappings,
        button_specs=base.button_specs,
        button_names=base.button_names,
        convention=convention,
    )


def modify_device_info(
    base: DeviceInfo,
    name: str | None = None,
    remap_axes: AxisRemap | None = None,
    invert_axes: list[Axis] | None = None,
    axis_scale: float | None = None,
) -> DeviceInfo:
    """Create a modified DeviceInfo from an existing one.

    remap_axes and invert_axes operate directly on the slots of the input spec
    in its current convention. The input convention is preserved for name/scale-only
    changes; convention is set to None when axes are modified.

    Args:
        base: Existing DeviceInfo to modify.
        name: Optional new name for the device.
        remap_axes: Optional mapping of each output axis to the source axis whose
                    data it should read (direction: output <- source). A value is
                    either a source axis name, or an (axis, sign) tuple to flip
                    sign in the same step. Reads are taken from the *original*
                    spec, so swaps such as {"x": "y", "y": "x"} apply atomically.
                    Example: {"x": ("z", -1)} makes output x read negated z.
        invert_axes: Axis names to negate, e.g. ["y", "roll"]. A convenience for
                     the common case; invert_axes=["y"] equals
                     remap_axes={"y": ("y", -1)}. Mutually exclusive with
                     remap_axes — when remapping, express inversions as (axis, -1)
                     tuples there instead.
        axis_scale: Optional new axis scale value.

    Returns:
        New DeviceInfo with modifications applied.

    Raises:
        ValueError: If both remap_axes and invert_axes are given.

    Example:
        specs = pyspacemouse.get_device_specs()
        tweaked = modify_device_info(
            specs["SpaceNavigator"],
            invert_axes=["y"],
        )
    """
    if remap_axes and invert_axes:
        raise ValueError(
            "remap_axes and invert_axes are mutually exclusive; express inversions "
            "as (axis, -1) tuples inside remap_axes instead, e.g. {'z': ('z', -1)}."
        )

    new_name = name if name is not None else base.name
    new_scale = axis_scale if axis_scale is not None else base.axis_scale

    new_mappings = dict(base.mappings)
    if remap_axes:
        for target_axis, remap in remap_axes.items():
            source_axis, sign = _parse_axis_remap(target_axis, remap)
            if source_axis not in base.mappings:
                raise ValueError(f"Cannot remap missing source axis: {source_axis!r}.")
            new_mappings[target_axis] = _copy_axis_spec(base.mappings[source_axis], sign)

    for axis in invert_axes or []:
        if axis not in AXIS_NAMES:
            raise ValueError(f"Unknown axis to invert: {axis!r}. Valid axes: {list(AXIS_NAMES)}")
        if axis not in new_mappings:
            raise ValueError(f"Cannot invert missing axis: {axis!r}.")
        new_mappings[axis] = _copy_axis_spec(new_mappings[axis], -1)

    axes_modified = bool(remap_axes or invert_axes)
    return DeviceInfo(
        name=new_name,
        vendor_id=base.vendor_id,
        product_id=base.product_id,
        led_id=base.led_id,
        axis_scale=new_scale,
        mappings=new_mappings,
        button_specs=base.button_specs,
        button_names=base.button_names,
        convention=None if axes_modified else base.convention,
    )
