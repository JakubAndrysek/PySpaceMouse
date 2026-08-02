"""Multi-device example: Connect to multiple SpaceMouse devices.

This example shows how to open two SpaceMouse devices simultaneously,
useful for dual-hand control or controlling multiple robots.
"""

import time

import pyspacemouse
from pyspacemouse import AxisConvention


def main():
    # First, discover connected devices
    connected = pyspacemouse.get_connected_devices_by_path()
    print(f"Found {len(connected)} spacemouse device(s): {list(connected.values())}")

    if len(connected) < 2:
        print("This example requires 2 SpaceMouse devices connected.")
        print("Tip: Use a 3Dconnexion Universal Receiver with device_index parameter")
        return

    # Arbitrarily take the first two devices found
    path0 = list(connected.keys())[0]
    path1 = list(connected.keys())[1]

    # Open two devices by path
    with pyspacemouse.open_by_path(path0, axis_convention=AxisConvention.HID_Z_UP) as left_hand:
        with pyspacemouse.open_by_path(
            path1, axis_convention=AxisConvention.HID_Z_UP
        ) as right_hand:
            print(f"Left hand:  {left_hand.name}")
            print(f"Right hand: {right_hand.name}")
            print()
            print("Move both devices (Ctrl+C to exit)")

            while True:
                left = left_hand.read_latest()
                right = right_hand.read_latest()

                if left.has_motion() or right.has_motion():
                    print(
                        f"Left: x={left.x:+.2f} y={left.y:+.2f} z={left.z:+.2f}  |  "
                        f"Right: x={right.x:+.2f} y={right.y:+.2f} z={right.z:+.2f}"
                    )

                time.sleep(0.1)


if __name__ == "__main__":
    main()
