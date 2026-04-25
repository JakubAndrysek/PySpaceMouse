"""Multi-device example: Connect to multiple SpaceMouse devices.

This example shows how to open two SpaceMouse devices simultaneously,
useful for dual-hand control or controlling multiple robots.
"""

import pyspacemouse


def main():
    # First, discover connected devices
    connected = pyspacemouse.get_connected_paths_and_names()
    print(f"Found {len(connected)} spacemouse device(s): {list(connected.values())}")

    if len(connected) < 2:
        print("This example requires 2 SpaceMouse devices connected.")
        print("Tip: Use a 3Dconnexion Universal Receiver with device_index parameter")
        return

    # Arbitrarily take the first two devices found
    path0 = list(connected.keys())[0]
    path1 = list(connected.keys())[1]

    # Open two devices by path
    with pyspacemouse.open_by_path(path0) as left_hand:
        with pyspacemouse.open_by_path(path1) as right_hand:
            print(f"Left hand:  {left_hand.name}")
            print(f"Right hand: {right_hand.name}")
            print()
            print("Move both devices (Ctrl+C to exit)")

            while True:
                left = left_hand.read()
                right = right_hand.read()

                if left.nonzero() or right.nonzero():
                    print(
                        f"Left: x={left.x:+.2f} y={left.y:+.2f} z={left.z:+.2f}  |  "
                        f"Right: x={right.x:+.2f} y={right.y:+.2f} z={right.z:+.2f}"
                    )


if __name__ == "__main__":
    main()
