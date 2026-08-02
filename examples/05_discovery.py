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
    connected = pyspacemouse.get_connected_devices_by_path()
    if connected:
        for name in connected.values():
            print(f"  ✓ {name}")
    else:
        print("  (none found)")
    print()

    # 2. List all supported device types
    print("Supported device types:")
    supported = pyspacemouse.get_supported_devices()
    for supported_name, vid, pid in supported:
        # Check if this device type is connected
        count = 0
        path_if_connected = ""
        for path, name in connected.items():
            if name == supported_name:
                count += 1
                path_if_connected = f"   (path: {path})"
        count_str = " " if count == 0 else str(count)
        print(
            f"  [{count_str}] {supported_name} (VID: {vid:#06x}, PID: {pid:#06x}){path_if_connected}"
        )
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
