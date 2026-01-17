"""Multi-device example: Connect to multiple SpaceMouse devices.

This example shows how to open two SpaceMouse devices simultaneously,
useful for dual-hand control or controlling multiple robots.
"""

import time

import pyspacemouse


def main():
    # First, discover connected devices
    connected = pyspacemouse.get_connected_devices()
    print(f"Found {len(connected)} device(s): {connected}")

    if len(connected) < 2:
        print("This example requires 2 SpaceMouse devices connected.")
        print("Tip: Use a 3Dconnexion Universal Receiver with device_index parameter")
        return

    # Open two devices using device_index
    # device_index=0 is the first device, device_index=1 is the second
    device_name = connected[0]

    with pyspacemouse.open(device=device_name, device_index=0) as left_hand:
        with pyspacemouse.open(device=device_name, device_index=1) as right_hand:
            print(f"Left hand:  {left_hand.name}")
            print(f"Right hand: {right_hand.name}")
            print()
            print("Move both devices (Ctrl+C to exit)")

            while True:
                left = left_hand.read()
                right = right_hand.read()

                print(
                    f"L: x={left.x:+.2f} y={left.y:+.2f} z={left.z:+.2f}  |  "
                    f"R: x={right.x:+.2f} y={right.y:+.2f} z={right.z:+.2f}"
                )
                time.sleep(0.02)


if __name__ == "__main__":
    main()
