"""Device discovery example: List and inspect available devices.

This example shows how to discover what SpaceMouse devices are
connected and what device types are supported.
"""

import pyspacemouse


def main():
    print("=" * 60)
    print("PySpaceMouse Device Discovery")
    print("=" * 60)
    print()

    # 1. List connected SpaceMouse devices
    print("Connected SpaceMouse devices:")
    connected = pyspacemouse.get_connected_devices()
    if connected:
        for name in connected:
            print(f"  ✓ {name}")
    else:
        print("  (none found)")
    print()

    # 2. List all supported device types
    print("Supported device types:")
    supported = pyspacemouse.get_supported_devices()
    for name, vid, pid in supported:
        # Check if this device type is connected
        is_connected = name in connected
        status = "✓" if is_connected else " "
        print(f"  [{status}] {name} (VID: {vid:#06x}, PID: {pid:#06x})")
    print()

    # 3. List ALL HID devices (for debugging)
    print("All HID devices on system:")
    all_hid = pyspacemouse.get_all_hid_devices()
    if all_hid:
        for product, manufacturer, vid, pid in all_hid:
            product = product or "Unknown"
            manufacturer = manufacturer or "Unknown"
            print(f"  - {product} by {manufacturer}")
            print(f"      VID: {vid:#06x}, PID: {pid:#06x}")
    else:
        print("  (none found - is hidapi installed?)")
    print()

    # 4. Show device specs (advanced)
    print("Device specifications loaded from TOML:")
    specs = pyspacemouse.get_device_specs()
    print(f"  {len(specs)} device types configured")
    print()


if __name__ == "__main__":
    main()
