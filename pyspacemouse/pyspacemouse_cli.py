import argparse
import time

from pyspacemouse import list_devices, list_available_devices, open as open_mouse, read as read_mouse, \
    close as close_mouse, list_all_hid_devices
from pkg_resources import get_distribution


def print_version_cli():
    distribution = get_distribution("pyspacemouse")
    print(f"pyspacemouse version {distribution.version}")


def list_spacemouse_cli():
    devices = list_devices()
    if devices:
        print("Connected SpaceMouse devices:")
        for device in devices:
            print(f"- {device}")
    else:
        print("Error: No connected SpaceMouse devices found.")

def list_all_hid_devices_cli():
    devices = list_all_hid_devices()
    if devices:
        print("All HID devices:")
        for (product_string, manufacturer_string, vendor_id, product_id) in devices:
            if product_string == "":
                product_string = "Unknown"
            if manufacturer_string == "":
                manufacturer_string = "Unknown"
            print(f"- {product_string} by {manufacturer_string} [VID: {hex(vendor_id)}, PID: {hex(product_id)}]")
    else:
        print("Error: No HID devices found.")

def list_supported_devices_cli():
    available_devices = list_available_devices()
    if available_devices:
        print("Available SpaceMouse devices:")
        for (device_name, vid_id, pid_id) in available_devices:
            print(f"- {device_name} [VID: {hex(vid_id)}, PID: {hex(pid_id)}]")
    else:
        print("Error: No available SpaceMouse devices found.")

def test_connect_cli():
    try:
        success = open_mouse()
    except Exception as e:
        print(f"Failed to open SpaceMouse: {e}")
        return

    if not success:
        print("Failed to open SpaceMouse")
        return

    print("SpaceMouse opened successfully, reading x, y, z values...")
    time.sleep(1)

    try:
        while True:
            state = read_mouse()
            print(state.x, state.y, state.z)
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting...")
    finally:
        close_mouse()

def main():
    parser = argparse.ArgumentParser(description="PySpaceMouse CLI",
                                     epilog="For more information, visit https://spacemouse.kubaandrysek.cz/")
    parser.add_argument(
        "--version", action="store_true", help="Version of pyspacemouse"
    )
    parser.add_argument(
        "--list-spacemouse", action="store_true", help="List connected SpaceMouse devices"
    )
    parser.add_argument(
        "--list-supported-devices", action="store_true", help="List supported SpaceMouse devices"
    )
    parser.add_argument(
        "--list-all-hid-devices", action="store_true", help="List all connected HID devices"
    )
    parser.add_argument(
        "--test-connect", action="store_true", help="Test connect to the first available device"
    )
    args = parser.parse_args()

    if args.version:
        print_version_cli()
    elif args.list_spacemouse:
        list_spacemouse_cli()
    elif args.list_supported_devices:
        list_supported_devices_cli()
    elif args.list_all_hid_devices:
        list_all_hid_devices_cli()
    elif args.test_connect:
        test_connect_cli()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
