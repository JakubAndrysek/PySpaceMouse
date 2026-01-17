"""Type definitions for PySpaceMouse.

This module contains all the core data structures used throughout the library.
All types are immutable (frozen dataclasses) for thread safety and clarity.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

# Axis names as a literal type for type safety
Axis = Literal["x", "y", "z", "roll", "pitch", "yaw"]

# All valid axis names
AXIS_NAMES: tuple[Axis, ...] = ("x", "y", "z", "roll", "pitch", "yaw")


@dataclass(frozen=True, slots=True)
class AxisSpec:
    """Specification for reading an axis value from HID data.

    Attributes:
        channel: HID channel number for this axis data
        byte1: First byte index in the HID data array
        byte2: Second byte index in the HID data array
        scale: Multiplier for the axis value (usually 1 or -1)
    """

    channel: int
    byte1: int
    byte2: int
    scale: int


@dataclass(frozen=True, slots=True)
class ButtonSpec:
    """Specification for reading a button state from HID data.

    Attributes:
        channel: HID channel number for button data
        byte: Byte index in the HID data array
        bit: Bit position within the byte
    """

    channel: int
    byte: int
    bit: int


class ButtonState(list):
    """List of button states that can be converted to a bitmask integer.

    Each element is 0 (not pressed) or 1 (pressed).
    """

    def __int__(self) -> int:
        """Convert button states to integer bitmask."""
        return sum((b << i) for (i, b) in enumerate(reversed(self)))


@dataclass(slots=True)
class SpaceMouseState:
    """Current state of the SpaceMouse device.

    Attributes:
        t: Timestamp (seconds since program start)
        x: X-axis translation [-1.0, 1.0]
        y: Y-axis translation [-1.0, 1.0]
        z: Z-axis translation [-1.0, 1.0]
        roll: Roll rotation [-1.0, 1.0]
        pitch: Pitch rotation [-1.0, 1.0]
        yaw: Yaw rotation [-1.0, 1.0]
        buttons: List of button states (0 or 1)
    """

    t: float = -1.0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    roll: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0
    buttons: ButtonState = field(default_factory=lambda: ButtonState([]))

    def __getitem__(self, key: str) -> float:
        """Allow dict-like access for backward compatibility."""
        return getattr(self, key)


@dataclass(frozen=True, slots=True)
class DeviceInfo:
    """Static information about a device type.

    Attributes:
        name: Human-readable device name
        vendor_id: USB vendor ID
        product_id: USB product ID
        led_id: LED HID usage (page, usage) or None if no LED
        axis_scale: Scaling factor for axis values (default 350.0)
        mappings: Dict of axis name to AxisSpec
        button_specs: Tuple of ButtonSpec for each button
        button_names: Tuple of button names corresponding to button_specs
    """

    name: str
    vendor_id: int
    product_id: int
    led_id: tuple[int, int] | None
    axis_scale: float
    mappings: dict[Axis, AxisSpec]
    button_specs: tuple[ButtonSpec, ...]
    button_names: tuple[str, ...]

    @property
    def hid_id(self) -> tuple[int, int]:
        """Return (vendor_id, product_id) tuple for backward compatibility."""
        return (self.vendor_id, self.product_id)

    @property
    def bytes_to_read(self) -> int:
        """Calculate the number of bytes needed to read from HID device."""
        if not self.mappings:
            return 0
        byte_indices = []
        for spec in self.mappings.values():
            byte_indices.extend([spec.byte1, spec.byte2])
        return max(byte_indices) + 1 if byte_indices else 0

    def get_button_name(self, index: int) -> str:
        """Get button name by index, or 'BUTTON_N' if not found."""
        if 0 <= index < len(self.button_names):
            return self.button_names[index]
        return f"BUTTON_{index}"
