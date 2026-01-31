"""Public API for PySpaceMouse.

This module provides the main functions for discovering and opening SpaceMouse devices.

Usage:
    # Simple usage with context manager
    with pyspacemouse.open() as device:
        while True:
            state = device.read()
            print(state.x, state.y, state.z)

    # Open specific device by path
    with pyspacemouse.open_by_path("/dev/hidraw0") as device:
        state = device.read()
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, List, Optional, Sequence, Tuple

from easyhid import Enumeration

from .callbacks import ButtonCallback, Config, DofCallback
from .device import SpaceMouseDevice
from .loader import get_device_specs
from .types import DeviceInfo, SpaceMouseState


def get_connected_spacemice() -> List[Tuple[str, str]]:
    """Return the paths and names of the supported devices currently connected.

    Returns:
        Tuple of two lists: (device_paths, device_names)
        Empty list if no supported devices are found.

    Raises:
        RuntimeError: If HID API is not installed.
    """
    try:
        hid = Enumeration()
    except AttributeError as e:
        raise RuntimeError(
            "HID API is probably not installed. See https://spacemouse.kubaandrysek.cz for details."
        ) from e

    device_specs = get_device_specs()
    devices_by_path = {}

    for hid_device in hid.find():
        for name, spec in device_specs.items():
            if hid_device.vendor_id == spec.vendor_id and hid_device.product_id == spec.product_id:
                devices_by_path[hid_device.path] = name

    return list(devices_by_path.items())


def get_supported_devices() -> List[Tuple[str, int, int]]:
    """Return a list of all supported device types (from configuration).

    Returns:
        List of tuples: (device_name, vendor_id, product_id)
    """
    return [(name, spec.vendor_id, spec.product_id) for name, spec in get_device_specs().items()]


def get_all_hid_devices() -> List[Tuple[str, str, int, int]]:
    """Return a list of all HID devices connected to the system.

    Returns:
        List of tuples: (product_string, manufacturer_string, vendor_id, product_id)

    Raises:
        RuntimeError: If HID API is not installed.
    """
    try:
        hid = Enumeration()
    except AttributeError as e:
        raise RuntimeError(
            "HID API is probably not installed. See https://spacemouse.kubaandrysek.cz for details."
        ) from e

    return [
        (
            dev.product_string or "",
            dev.manufacturer_string or "",
            dev.vendor_id,
            dev.product_id,
        )
        for dev in hid.find()
    ]


def _create_and_open_device(
    spec: DeviceInfo,
    hid_device,
    callback: Optional[Callable[[SpaceMouseState], None]] = None,
    dof_callback: Optional[Callable[[SpaceMouseState], None]] = None,
    dof_callbacks: Optional[Sequence[DofCallback]] = None,
    button_callback: Optional[Callable[[SpaceMouseState, List[int]], None]] = None,
    button_callbacks: Optional[Sequence[ButtonCallback]] = None,
    nonblocking: bool = True,
) -> SpaceMouseDevice:
    """Create, configure and open a SpaceMouseDevice.

    This is a shared helper to avoid duplication between open() and open_by_path().
    """
    mouse = SpaceMouseDevice(info=spec, device=hid_device)
    mouse.configure(
        callback=callback,
        dof_callback=dof_callback,
        dof_callbacks=dof_callbacks,
        button_callback=button_callback,
        button_callbacks=button_callbacks,
    )
    mouse.open()
    hid_device.set_nonblocking(nonblocking)
    return mouse


def open_by_path(
    path: str | Path,
    callback: Optional[Callable[[SpaceMouseState], None]] = None,
    dof_callback: Optional[Callable[[SpaceMouseState], None]] = None,
    dof_callbacks: Optional[Sequence[DofCallback]] = None,
    button_callback: Optional[Callable[[SpaceMouseState, List[int]], None]] = None,
    button_callbacks: Optional[Sequence[ButtonCallback]] = None,
    nonblocking: bool = True,
    device_spec: Optional[DeviceInfo] = None,
) -> SpaceMouseDevice:
    """Open a SpaceMouse device by its filesystem path.

    This is mutually exclusive with open() - use this when you know the
    exact device path, use open() for automatic device discovery.

    Args:
        path: Filesystem path to the HID device (e.g., "/dev/hidraw0")
        callback: Called on every state change
        dof_callback: Called on axis state changes
        dof_callbacks: List of per-axis callbacks
        button_callback: Called on button state changes
        button_callbacks: List of per-button callbacks
        nonblocking: If True, use non-blocking reads (required for callbacks)
        device_spec: Optional custom DeviceInfo. If provided, uses this
                     instead of looking up by VID/PID. Useful for custom
                     axis mappings or unsupported devices.

    Returns:
        SpaceMouseDevice instance (use as context manager for auto-cleanup)

    Raises:
        FileNotFoundError: If the specified path does not exist
        ValueError: If the device at path is not a supported SpaceMouse
                    (unless device_spec is provided)
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Device path '{path}' does not exist.")

    # Resolve path in case it's relative or a symlink
    path = path.resolve()

    # Find the HID device at this path
    hid = Enumeration()
    hid_device = None

    for dev in hid.device_list:
        dev_path = Path(dev.path).resolve()
        if dev_path == path:
            hid_device = dev
            break

    if hid_device is None:
        raise FileNotFoundError(f"No HID device found at path '{path}'.")

    # Use provided spec or find matching device specification
    if device_spec is not None:
        spec = device_spec
    else:
        all_specs = get_device_specs()
        spec = None

        for device_s in all_specs.values():
            if (
                hid_device.vendor_id == device_s.vendor_id
                and hid_device.product_id == device_s.product_id
            ):
                spec = device_s
                break

        if spec is None:
            raise ValueError(
                f"Device at '{path}' (VID={hid_device.vendor_id:#06x}, "
                f"PID={hid_device.product_id:#06x}) is not a supported SpaceMouse. "
                f"Use device_spec parameter for custom/unsupported devices."
            )

    print(f"{spec.name} found at {path}")

    return _create_and_open_device(
        spec=spec,
        hid_device=hid_device,
        callback=callback,
        dof_callback=dof_callback,
        dof_callbacks=dof_callbacks,
        button_callback=button_callback,
        button_callbacks=button_callbacks,
        nonblocking=nonblocking,
    )


def open(
    callback: Optional[Callable[[SpaceMouseState], None]] = None,
    dof_callback: Optional[Callable[[SpaceMouseState], None]] = None,
    dof_callbacks: Optional[Sequence[DofCallback]] = None,
    button_callback: Optional[Callable[[SpaceMouseState, List[int]], None]] = None,
    button_callbacks: Optional[Sequence[ButtonCallback]] = None,
    nonblocking: bool = True,
    device: Optional[str] = None,
    device_index: int = 0,
    device_spec: Optional[DeviceInfo] = None,
) -> SpaceMouseDevice:
    """Open a SpaceMouse device by name or auto-detection.

    Use as a context manager for automatic cleanup:

        with pyspacemouse.open() as device:
            state = device.read()

    Args:
        callback: Called on every state change
        dof_callback: Called on axis state changes
        dof_callbacks: List of per-axis callbacks
        button_callback: Called on button state changes
        button_callbacks: List of per-button callbacks
        nonblocking: If True, use non-blocking reads (required for callbacks)
        device: Device name to open. If None, uses first found device.
        device_index: Which instance to open if multiple same devices connected
        device_spec: Optional custom DeviceInfo. If provided, uses this
                     instead of looking up from TOML. Useful for custom
                     axis mappings. The device/device_index are still used
                     to find the HID device.

    Returns:
        SpaceMouseDevice instance (use as context manager for auto-cleanup)

    Raises:
        RuntimeError: If no device is found
        ValueError: If the specified device name is not recognized
    """
    device_specs = get_device_specs()

    # Auto-detect device if not specified
    if device is None:
        connected = get_connected_spacemice()
        if not connected:
            raise RuntimeError("No connected or supported devices found.")
        device = connected[0][1]

    if device not in device_specs:
        raise ValueError(f"Unknown device: '{device}'. Available: {list(device_specs.keys())}")

    # Use provided spec or get from TOML
    spec = device_spec if device_spec is not None else device_specs[device]

    # Find matching HID devices
    hid = Enumeration()
    found = []

    for hid_dev in hid.find():
        if hid_dev.vendor_id == spec.vendor_id and hid_dev.product_id == spec.product_id:
            found.append(hid_dev)

    if not found:
        raise RuntimeError(f"Device '{device}' not found.")

    # Select device by index
    if device_index >= len(found):
        device_index = 0

    hid_dev = found[device_index]
    print(f"{device} found")

    return _create_and_open_device(
        spec=spec,
        hid_device=hid_dev,
        callback=callback,
        dof_callback=dof_callback,
        dof_callbacks=dof_callbacks,
        button_callback=button_callback,
        button_callbacks=button_callbacks,
        nonblocking=nonblocking,
    )


def open_with_config(
    config: Config,
    nonblocking: bool = True,
    device: Optional[str] = None,
    device_index: int = 0,
) -> SpaceMouseDevice:
    """Open a SpaceMouse device using a Config object.

    Args:
        config: Configuration with callback definitions
        nonblocking: If True, use non-blocking reads
        device: Device name to open
        device_index: Which instance to open if multiple connected

    Returns:
        SpaceMouseDevice instance (use as context manager for auto-cleanup)
    """
    return open(
        callback=config.callback,
        dof_callback=config.dof_callback,
        dof_callbacks=config.dof_callbacks,
        button_callback=config.button_callback,
        button_callbacks=config.button_callbacks,
        nonblocking=nonblocking,
        device=device,
        device_index=device_index,
    )
