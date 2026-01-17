"""Open by path example: Connect to a specific HID device by filesystem path.

This is useful when you need to ensure you always connect to the same
physical device, regardless of enumeration order.

Note: Device paths vary by OS:
- Linux: /dev/hidraw0, /dev/hidraw1, etc.
- macOS: /dev/hidraw0 or similar (may require special setup)
- Windows: Uses different path format
"""

import time

import pyspacemouse


def main():
    # First, list all HID devices to find the path you need
    print("All HID devices:")
    for product, manufacturer, vid, pid in pyspacemouse.get_all_hid_devices():
        print(f"  {product or 'Unknown'} by {manufacturer or 'Unknown'}")
        print(f"    VID: {vid:#06x}, PID: {pid:#06x}")
    print()

    # Example: Open by specific path (Linux example)
    # Replace with actual path from your system
    device_path = "/dev/hidraw0"

    try:
        with pyspacemouse.open_by_path(device_path) as device:
            print(f"Connected to: {device.name} at {device_path}")
            print("Move the device (Ctrl+C to exit)")
            print()

            while True:
                state = device.read()
                print(f"x={state.x:+.2f} y={state.y:+.2f} z={state.z:+.2f}")
                time.sleep(0.01)

    except FileNotFoundError as e:
        print(f"Device path not found: {e}")
        print("Try running with a valid device path for your system.")
    except ValueError as e:
        print(f"Device not supported: {e}")


if __name__ == "__main__":
    main()
