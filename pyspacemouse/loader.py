"""TOML configuration loader for PySpaceMouse device specifications.

This module handles loading device specifications from the devices.toml file
using a lazy-loading pattern without module-level global state.
"""

from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path
from typing import Dict

from .types import AxisSpec, ButtonSpec, DeviceInfo

# TOML parser: use tomllib (3.11+) or tomli (3.8-3.10)
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        raise ImportError(
            "tomli package required for Python < 3.11. Install with: pip install tomli"
        )


def _parse_device_data(device_name: str, device_data: dict) -> DeviceInfo:
    """Parse a single device entry from TOML data."""
    # Parse mappings
    mappings = {}
    if "mappings" in device_data:
        for axis, values in device_data["mappings"].items():
            mappings[axis] = AxisSpec(
                channel=values[0],
                byte1=values[1],
                byte2=values[2],
                scale=values[3],
            )

    # Parse buttons
    button_specs = []
    button_names = []
    if "buttons" in device_data:
        for btn_name, values in device_data["buttons"].items():
            button_names.append(btn_name)
            button_specs.append(ButtonSpec(channel=values[0], byte=values[1], bit=values[2]))

    # Handle led_id (optional in TOML)
    led_id = device_data.get("led_id")
    if led_id is not None:
        led_id = tuple(led_id)

    # Get HID IDs
    hid_id = device_data["hid_id"]

    return DeviceInfo(
        name=device_name,
        vendor_id=hid_id[0],
        product_id=hid_id[1],
        led_id=led_id,
        axis_scale=device_data.get("axis_scale", 350.0),
        mappings=mappings,
        button_specs=tuple(button_specs),
        button_names=tuple(button_names),
    )


def load_device_specs(toml_path: Path | str | None = None) -> Dict[str, DeviceInfo]:
    """Load device specifications from TOML file.

    Args:
        toml_path: Path to devices.toml file. If None, uses default location.

    Returns:
        Dictionary mapping device names to DeviceInfo instances.
    """
    if toml_path is None:
        toml_path = Path(__file__).parent / "devices.toml"
    elif isinstance(toml_path, str):
        toml_path = Path(toml_path)

    with open(toml_path, "rb") as f:
        data = tomllib.load(f)

    return {
        device_name: _parse_device_data(device_name, device_data)
        for device_name, device_data in data.items()
    }


@lru_cache(maxsize=1)
def get_device_specs() -> Dict[str, DeviceInfo]:
    """Get device specifications, cached after first load.

    Uses functools.lru_cache instead of module-level global variable
    for cleaner lazy initialization.

    Returns:
        Dictionary mapping device names to DeviceInfo instances.
    """
    return load_device_specs()
