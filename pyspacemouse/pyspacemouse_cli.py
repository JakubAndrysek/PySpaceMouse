"""PySpaceMouse command-line interface."""

import argparse
import time

import pyspacemouse


def print_version_cli():
    """Print the pyspacemouse version."""
    print(f"pyspacemouse version {pyspacemouse.__version__}")


def list_spacemouse_cli():
    """List connected SpaceMouse devices."""
    devices = pyspacemouse.get_connected_devices()
    if devices:
        print("Connected SpaceMouse devices:")
        for device in devices:
            print(f"  - {device}")
    else:
        print("No connected SpaceMouse devices found.")


def list_all_hid_devices_cli():
    """List all connected HID devices."""
    devices = pyspacemouse.get_all_hid_devices()
    if devices:
        print("All HID devices:")
        for product_string, manufacturer_string, vendor_id, product_id in devices:
            product = product_string or "Unknown"
            manufacturer = manufacturer_string or "Unknown"
            print(
                f"  - {product} by {manufacturer} [VID: {vendor_id:#06x}, PID: {product_id:#06x}]"
            )
    else:
        print("No HID devices found.")


def list_supported_devices_cli():
    """List all supported SpaceMouse device types."""
    available_devices = pyspacemouse.get_supported_devices()
    if available_devices:
        print("Supported SpaceMouse devices:")
        for device_name, vid_id, pid_id in available_devices:
            print(f"  - {device_name} [VID: {vid_id:#06x}, PID: {pid_id:#06x}]")
    else:
        print("No device configurations found.")


def test_connect_cli():
    """Test connection to the first available device."""
    try:
        with pyspacemouse.open() as device:
            print(f"Connected to: {device.name}")
            print("Reading x, y, z values (Ctrl+C to exit)...")
            print("Move the SpaceMouse to see values")
            time.sleep(0.5)

            while True:
                state = device.read()
                if any(
                    abs(val) > 0.01
                    for val in [state.x, state.y, state.z, state.roll, state.pitch, state.yaw]
                ):
                    print(
                        f"x={state.x:+.2f} y={state.y:+.2f} z={state.z:+.2f} "
                        f"roll={state.roll:+.2f} pitch={state.pitch:+.2f} yaw={state.yaw:+.2f}"
                    )
                time.sleep(0.01)

    except RuntimeError as e:
        print(f"Failed to open SpaceMouse: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PySpaceMouse CLI",
        epilog="For more information, visit https://spacemouse.kubaandrysek.cz/",
    )
    parser.add_argument("--version", action="store_true", help="Show pyspacemouse version")
    parser.add_argument(
        "--list-connected",
        action="store_true",
        help="List connected SpaceMouse devices",
    )
    parser.add_argument(
        "--list-supported",
        action="store_true",
        help="List all supported SpaceMouse device types",
    )
    parser.add_argument("--list-hid", action="store_true", help="List all connected HID devices")
    parser.add_argument(
        "--test", action="store_true", help="Test connection to first available device"
    )

    args = parser.parse_args()

    if args.version:
        print_version_cli()
    elif args.list_connected:
        list_spacemouse_cli()
    elif args.list_supported:
        list_supported_devices_cli()
    elif args.list_hid:
        list_all_hid_devices_cli()
    elif args.test:
        test_connect_cli()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
