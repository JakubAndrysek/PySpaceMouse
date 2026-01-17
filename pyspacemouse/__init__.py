"""PySpaceMouse - Python interface for 3DConnexion SpaceMouse devices.

This library provides a Pythonic interface to read input from 3DConnexion
SpaceMouse 6-DOF controllers.

Basic usage:
    import pyspacemouse

    # Using context manager (recommended)
    with pyspacemouse.open() as device:
        while True:
            state = device.read()
            print(state.x, state.y, state.z)

    # Without context manager
    device = pyspacemouse.open()
    try:
        state = device.read()
    finally:
        device.close()
"""

from __future__ import annotations

# Version handling for dynamic versioning with hatch-vcs
try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    from importlib_metadata import PackageNotFoundError, version  # type: ignore

try:
    __version__ = version("pyspacemouse")
except PackageNotFoundError:
    __version__ = "0.0.0.dev0"

# Core types
# Public API
from .api import (
    get_all_hid_devices,
    get_connected_devices,
    get_supported_devices,
    open,
    open_by_path,
    open_with_config,
)

# Callback types
from .callbacks import (
    ButtonCallback,
    Config,
    DofCallback,
)

# Config helpers (for custom device configurations)
from .config_helpers import create_device_info, modify_device_info

# Device class
from .device import SpaceMouseDevice

# Loader (for advanced usage)
from .loader import get_device_specs, load_device_specs
from .types import (
    AXIS_NAMES,
    Axis,
    AxisSpec,
    ButtonSpec,
    ButtonState,
    DeviceInfo,
    SpaceMouseState,
)

# Utility functions
from .utils import (
    print_buttons,
    print_state,
    silent_callback,
)

__all__ = [
    # Version
    "__version__",
    # Types
    "Axis",
    "AXIS_NAMES",
    "AxisSpec",
    "ButtonSpec",
    "ButtonState",
    "DeviceInfo",
    "SpaceMouseState",
    # Callbacks
    "ButtonCallback",
    "Config",
    "DofCallback",
    # Device
    "SpaceMouseDevice",
    # API
    "get_all_hid_devices",
    "get_connected_devices",
    "get_supported_devices",
    "open",
    "open_by_path",
    "open_with_config",
    # Utils
    "print_buttons",
    "print_state",
    "silent_callback",
    # Loader
    "get_device_specs",
    "load_device_specs",
    # Config helpers
    "create_device_info",
    "modify_device_info",
]
