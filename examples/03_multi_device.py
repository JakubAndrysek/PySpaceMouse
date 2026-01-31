"""Multi-device example: Connect to multiple SpaceMouse devices.

This example shows how to open two SpaceMouse devices simultaneously,
useful for dual-hand control or controlling multiple robots.
"""

import time

import pyspacemouse


def main():
    # First, discover connected devices
    devices = pyspacemouse.get_connected_spacemice()
    paths = [path for path, name in devices]
    names = [name for path, name in devices]
    print(f"Found {len(names)} spacemouse device(s): {names}")

    if len(names) < 2:
        print("This example requires 2 SpaceMouse devices connected.")
        print("Tip: Use a 3Dconnexion Universal Receiver with device_index parameter")
        return

    # Open two devices by path
    with pyspacemouse.open_by_path(paths[0]) as left_hand:
        with pyspacemouse.open_by_path(paths[1]) as right_hand:
            print(f"Left hand:  {left_hand.name}")
            print(f"Right hand: {right_hand.name}")
            print()
            print("Move both devices (Ctrl+C to exit)")

            while True:
                left = left_hand.read()
                right = right_hand.read()

                print(
                    f"Left: x={left.x:+.2f} y={left.y:+.2f} z={left.z:+.2f}  |  "
                    f"Right: x={right.x:+.2f} y={right.y:+.2f} z={right.z:+.2f}"
                )
                time.sleep(0.02)


if __name__ == "__main__":
    main()
