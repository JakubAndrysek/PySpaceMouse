"""SpaceMouse device representation.

This module contains the SpaceMouseDevice class which represents
a connected SpaceMouse device and handles reading/processing input.

Supports context manager protocol for safe resource cleanup:

    with pyspacemouse.open() as device:
        while True:
            state = device.read()
"""

from __future__ import annotations

import timeit
from typing import TYPE_CHECKING, Callable, List, Optional, Sequence

from easyhid import HIDException

from .callbacks import ButtonCallback, Config, DofCallback
from .types import AXIS_NAMES, ButtonState, DeviceInfo, SpaceMouseState

if TYPE_CHECKING:
    from easyhid import Device as HIDDevice

# High-accuracy clock for timing
high_acc_clock = timeit.default_timer


def _to_int16(y1: int, y2: int) -> int:
    """Convert two 8-bit bytes to a signed 16-bit integer."""
    x = y1 | (y2 << 8)
    if x >= 32768:
        x = -(65536 - x)
    return x


class SpaceMouseDevice:
    """Represents a connected SpaceMouse device.

    This class handles reading input from the device, processing HID data,
    and invoking callbacks based on state changes.

    Supports context manager protocol:
        with pyspacemouse.open() as device:
            state = device.read()

    Attributes:
        info: Static device information (read-only)
        state: Current device state
        connected: Whether the device is currently connected
    """

    __slots__ = (
        "_info",
        "_device",
        "_state",
        "_last_axis_time",
        "_callback",
        "_dof_callback",
        "_dof_callbacks",
        "_button_callback",
        "_button_callbacks",
        "_nonblocking",
        "_product_name",
        "_vendor_name",
        "_version_number",
        "_serial_number",
    )

    def __init__(self, info: DeviceInfo, device: Optional[HIDDevice] = None) -> None:
        """Initialize the SpaceMouseDevice.

        Args:
            info: Device specification from loader
            device: Optional HID device instance
        """
        self._info = info
        self._device = device

        # Initialize state
        self._state = SpaceMouseState(buttons=ButtonState([0] * len(info.button_specs)))
        self._last_axis_time = {axis: 0.0 for axis in AXIS_NAMES}

        # Callbacks (None by default)
        self._callback: Optional[Callable[[SpaceMouseState], None]] = None
        self._dof_callback: Optional[Callable[[SpaceMouseState], None]] = None
        self._dof_callbacks: Optional[Sequence[DofCallback]] = None
        self._button_callback: Optional[Callable[[SpaceMouseState, List[int]], None]] = None
        self._button_callbacks: Optional[Sequence[ButtonCallback]] = None
        self._nonblocking = True

        # Connection details (populated on open)
        self._product_name: str = ""
        self._vendor_name: str = ""
        self._version_number: str = ""
        self._serial_number: str = ""

    # -------------------------------------------------------------------------
    # Context manager protocol
    # -------------------------------------------------------------------------

    def __enter__(self) -> SpaceMouseDevice:
        """Enter context manager - device is already open."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager - close the device."""
        self.close()

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def info(self) -> DeviceInfo:
        """Get the static device information."""
        return self._info

    @property
    def name(self) -> str:
        """Get the device name."""
        return self._info.name

    @property
    def connected(self) -> bool:
        """Check if the device is connected."""
        return self._device is not None

    @property
    def state(self) -> SpaceMouseState:
        """Get the current device state (triggers a read)."""
        return self.read()

    @property
    def product_name(self) -> str:
        """Get the product name from the connected device."""
        return self._product_name

    @property
    def vendor_name(self) -> str:
        """Get the vendor name from the connected device."""
        return self._vendor_name

    @property
    def version_number(self) -> str:
        """Get the version number from the connected device."""
        return self._version_number

    @property
    def serial_number(self) -> str:
        """Get the serial number from the connected device."""
        return self._serial_number

    # -------------------------------------------------------------------------
    # Connection management
    # -------------------------------------------------------------------------

    def describe_connection(self) -> str:
        """Return a human-readable description of the connection."""
        if not self.connected:
            return f"{self.name} [disconnected]"
        return (
            f"{self.name} connected to {self._vendor_name} {self._product_name} "
            f"version: {self._version_number} [serial: {self._serial_number}]"
        )

    def open(self) -> None:
        """Open the connection to the device."""
        if self._device is None:
            raise RuntimeError("No HID device assigned to this SpaceMouseDevice")

        try:
            self._device.open()
        except HIDException as e:
            raise RuntimeError("Failed to open device") from e

        # Copy product details
        self._product_name = self._device.product_string or ""
        self._vendor_name = self._device.manufacturer_string or ""
        self._version_number = str(self._device.release_number or "")

        # Convert serial number to hex
        serial = self._device.serial_number or ""
        self._serial_number = "".join(f"{ord(c):02X}" for c in serial)

    def close(self) -> None:
        """Close the connection to the device."""
        if self._device is not None:
            self._device.close()
            self._device = None

    # -------------------------------------------------------------------------
    # Reading and processing
    # -------------------------------------------------------------------------

    def read(self) -> SpaceMouseState:
        """Read and process data from the device.

        Returns:
            The current state after processing any available data.
        """
        if not self.connected:
            return self._state

        data = self._device.read(self._info.bytes_to_read)
        if data:
            self._process(data)
        return self._state

    def _process(self, data: bytes) -> None:
        """Process incoming HID data and update state."""
        dof_changed = False
        button_changed = False

        # Process axis data
        for axis_name, spec in self._info.mappings.items():
            if data[0] == spec.channel:
                dof_changed = True
                if spec.byte1 < len(data) and spec.byte2 < len(data):
                    raw_value = _to_int16(data[spec.byte1], data[spec.byte2])
                    scaled_value = spec.scale * raw_value / self._info.axis_scale
                    setattr(self._state, axis_name, scaled_value)

        # Process button data
        for btn_idx, spec in enumerate(self._info.button_specs):
            if spec.channel is None:
                continue
            if data[0] == spec.channel:
                button_changed = True
                mask = 1 << spec.bit
                self._state.buttons[btn_idx] = 1 if (data[spec.byte] & mask) else 0

        # Update timestamp
        self._state.t = high_acc_clock()

        # Invoke callbacks
        self._invoke_callbacks(dof_changed, button_changed)

    def _invoke_callbacks(self, dof_changed: bool, button_changed: bool) -> None:
        """Invoke registered callbacks based on state changes."""
        state = self._state

        # General callback
        if self._callback:
            self._callback(state)

        # DoF callback
        if self._dof_callback and dof_changed:
            self._dof_callback(state)

        # Per-axis DoF callbacks
        if self._dof_callbacks and dof_changed:
            now = high_acc_clock()
            for dof_cb in self._dof_callbacks:
                axis_name = dof_cb.axis
                if now >= self._last_axis_time[axis_name] + dof_cb.sleep:
                    axis_val = getattr(state, axis_name)

                    if dof_cb.callback_minus is not None:
                        if axis_val > dof_cb.filter:
                            dof_cb.callback(state, axis_val)
                        elif axis_val < -dof_cb.filter:
                            dof_cb.callback_minus(state, axis_val)
                    elif abs(axis_val) > dof_cb.filter:
                        dof_cb.callback(state, axis_val)

                    self._last_axis_time[axis_name] = now

        # General button callback
        if self._button_callback and button_changed:
            self._button_callback(state, list(state.buttons))

        # Per-button callbacks
        if self._button_callbacks and button_changed:
            for btn_cb in self._button_callbacks:
                buttons = btn_cb.buttons
                if isinstance(buttons, int):
                    buttons = [buttons]

                if all(state.buttons[b] for b in buttons):
                    btn_cb.callback(state, list(state.buttons), btn_cb.buttons)

    def set_led(self, state: bool) -> None:
        """Set the LED state.

        Controls the LED indicator on the SpaceMouse device.

        Args:
            state: True to turn LED on, False to turn off

        Note:
            Not all devices have LEDs. If the device doesn't support LED
            control (info.led_id is None), this method does nothing.
            LED control failures are silently ignored.
        """
        if not self.connected:
            return
        if self._info.led_id is None:
            return  # Device has no LED

        # Send HID output report to control LED
        # led_id format: [report_id, on_value]
        report_id, on_value = self._info.led_id
        led_value = on_value if state else 0x00
        try:
            self._device.write(bytearray([report_id, led_value]))
        except Exception:
            pass  # Silently fail if LED control not supported

    # -------------------------------------------------------------------------
    # Configuration
    # -------------------------------------------------------------------------

    def set_config(self, config: Config) -> None:
        """Apply a configuration object to set callbacks."""
        self._callback = config.callback
        self._dof_callback = config.dof_callback
        self._dof_callbacks = config.dof_callbacks
        self._button_callback = config.button_callback
        self._button_callbacks = config.button_callbacks

    def configure(
        self,
        callback: Optional[Callable[[SpaceMouseState], None]] = None,
        dof_callback: Optional[Callable[[SpaceMouseState], None]] = None,
        dof_callbacks: Optional[Sequence[DofCallback]] = None,
        button_callback: Optional[Callable[[SpaceMouseState, List[int]], None]] = None,
        button_callbacks: Optional[Sequence[ButtonCallback]] = None,
    ) -> None:
        """Configure callbacks individually."""
        self._callback = callback
        self._dof_callback = dof_callback
        self._dof_callbacks = dof_callbacks
        self._button_callback = button_callback
        self._button_callbacks = button_callbacks

    def clear_callbacks(self) -> None:
        """Remove all registered callbacks."""
        self._callback = None
        self._dof_callback = None
        self._dof_callbacks = None
        self._button_callback = None
        self._button_callbacks = None

    def get_button_name(self, index: int) -> str:
        """Get the name of a button by its index."""
        return self._info.get_button_name(index)
