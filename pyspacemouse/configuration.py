from pyspacemouse.abstraction import AxisSpec, ButtonSpec
from pyspacemouse.devices import DeviceSpec

device_specs = {
    "SpaceExplorer": DeviceSpec(
        name="SpaceExplorer",
        # vendor ID and product ID
        hid_id=[0x46D, 0xc627],
        # LED HID usage code pair
        led_id=[0x8, 0x4B],
        mappings={
            "x": AxisSpec(channel=1, byte1=1, byte2=2, scale=1),
            "y": AxisSpec(channel=1, byte1=3, byte2=4, scale=-1),
            "z": AxisSpec(channel=1, byte1=5, byte2=6, scale=-1),
            "pitch": AxisSpec(channel=2, byte1=1, byte2=2, scale=-1),
            "roll": AxisSpec(channel=2, byte1=3, byte2=4, scale=-1),
            "yaw": AxisSpec(channel=2, byte1=5, byte2=6, scale=1),
        },
        button_mapping=[
            ButtonSpec(channel=3, byte=2, bit=0),  # SHIFT
            ButtonSpec(channel=3, byte=1, bit=6),  # ESC
            ButtonSpec(channel=3, byte=2, bit=1),  # CTRL
            ButtonSpec(channel=3, byte=1, bit=7),  # ALT
            ButtonSpec(channel=3, byte=1, bit=0),  # 1
            ButtonSpec(channel=3, byte=1, bit=1),  # 2
            ButtonSpec(channel=3, byte=2, bit=3),  # PANEL
            ButtonSpec(channel=3, byte=2, bit=2),  # FIT
            ButtonSpec(channel=3, byte=2, bit=5),  # -
            ButtonSpec(channel=3, byte=2, bit=4),  # +
            ButtonSpec(channel=3, byte=1, bit=2),  # T
            ButtonSpec(channel=3, byte=1, bit=3),  # L
            ButtonSpec(channel=3, byte=1, bit=5),  # F
            ButtonSpec(channel=3, byte=2, bit=6),  # 2D
            ButtonSpec(channel=3, byte=1, bit=4),  # R
        ],
        axis_scale=350.0,
    ),
    "SpaceNavigator": DeviceSpec(
        name="SpaceNavigator",
        # vendor ID and product ID
        hid_id=[0x46D, 0xC626],
        # LED HID usage code pair
        led_id=[0x8, 0x4B],
        mappings={
            "x": AxisSpec(channel=1, byte1=1, byte2=2, scale=1),
            "y": AxisSpec(channel=1, byte1=3, byte2=4, scale=-1),
            "z": AxisSpec(channel=1, byte1=5, byte2=6, scale=-1),
            "pitch": AxisSpec(channel=2, byte1=1, byte2=2, scale=-1),
            "roll": AxisSpec(channel=2, byte1=3, byte2=4, scale=-1),
            "yaw": AxisSpec(channel=2, byte1=5, byte2=6, scale=1),
        },
        button_mapping=[
            ButtonSpec(channel=3, byte=1, bit=0),  # LEFT
            ButtonSpec(channel=3, byte=1, bit=1),  # RIGHT
        ],
        axis_scale=350.0,
    ),
    "SpaceMouse USB": DeviceSpec(
        name="SpaceMouseUSB",
        # vendor ID and product ID
        hid_id=[0x256f, 0xc641],
        # LED HID usage code pair
        led_id=None,
        mappings={
            "x": AxisSpec(channel=1, byte1=1, byte2=2, scale=1),
            "y": AxisSpec(channel=1, byte1=3, byte2=4, scale=-1),
            "z": AxisSpec(channel=1, byte1=5, byte2=6, scale=-1),
            "pitch": AxisSpec(channel=2, byte1=1, byte2=2, scale=-1),
            "roll": AxisSpec(channel=2, byte1=3, byte2=4, scale=-1),
            "yaw": AxisSpec(channel=2, byte1=5, byte2=6, scale=1),
        },
        button_mapping=[
            ButtonSpec(channel=None, byte=None, bit=None),  # No buttons
        ],
        axis_scale=350.0,
    ),
    "SpaceMouse Compact": DeviceSpec(
        name="SpaceMouse Compact",
        # vendor ID and product ID
        hid_id=[0x256F, 0xC635],
        # LED HID usage code pair
        led_id=[0x8, 0x4B],
        mappings={
            "x": AxisSpec(channel=1, byte1=1, byte2=2, scale=1),
            "y": AxisSpec(channel=1, byte1=3, byte2=4, scale=-1),
            "z": AxisSpec(channel=1, byte1=5, byte2=6, scale=-1),
            "pitch": AxisSpec(channel=2, byte1=1, byte2=2, scale=-1),
            "roll": AxisSpec(channel=2, byte1=3, byte2=4, scale=-1),
            "yaw": AxisSpec(channel=2, byte1=5, byte2=6, scale=1),
        },
        button_mapping=[
            ButtonSpec(channel=3, byte=1, bit=0),  # LEFT
            ButtonSpec(channel=3, byte=1, bit=1),  # RIGHT
        ],
        axis_scale=350.0,
    ),
    "SpaceMouse Pro Wireless": DeviceSpec(
        name="SpaceMouse Pro Wireless",
        # vendor ID and product ID
        hid_id=[0x256F, 0xC632],
        # LED HID usage code pair
        led_id=[0x8, 0x4B],
        mappings={
            "x": AxisSpec(channel=1, byte1=1, byte2=2, scale=1),
            "y": AxisSpec(channel=1, byte1=3, byte2=4, scale=-1),
            "z": AxisSpec(channel=1, byte1=5, byte2=6, scale=-1),
            "pitch": AxisSpec(channel=1, byte1=7, byte2=8, scale=-1),
            "roll": AxisSpec(channel=1, byte1=9, byte2=10, scale=-1),
            "yaw": AxisSpec(channel=1, byte1=11, byte2=12, scale=1),
        },
        button_mapping=[
            ButtonSpec(channel=3, byte=1, bit=0),  # MENU
            ButtonSpec(channel=3, byte=3, bit=7),  # ALT
            ButtonSpec(channel=3, byte=4, bit=1),  # CTRL
            ButtonSpec(channel=3, byte=4, bit=0),  # SHIFT
            ButtonSpec(channel=3, byte=3, bit=6),  # ESC
            ButtonSpec(channel=3, byte=2, bit=4),  # 1
            ButtonSpec(channel=3, byte=2, bit=5),  # 2
            ButtonSpec(channel=3, byte=2, bit=6),  # 3
            ButtonSpec(channel=3, byte=2, bit=7),  # 4
            ButtonSpec(channel=3, byte=2, bit=0),  # ROLL CLOCKWISE
            ButtonSpec(channel=3, byte=1, bit=2),  # TOP
            ButtonSpec(channel=3, byte=4, bit=2),  # ROTATION
            ButtonSpec(channel=3, byte=1, bit=5),  # FRONT
            ButtonSpec(channel=3, byte=1, bit=4),  # REAR
            ButtonSpec(channel=3, byte=1, bit=1),  # FIT
        ],
        axis_scale=350.0,
    ),
    "SpaceMouse Pro": DeviceSpec(
        name="SpaceMouse Pro",
        # vendor ID and product ID
        hid_id=[0x46D, 0xC62b],
        led_id=[0x8, 0x4B],
        mappings={
            "x": AxisSpec(channel=1, byte1=1, byte2=2, scale=1),
            "y": AxisSpec(channel=1, byte1=3, byte2=4, scale=-1),
            "z": AxisSpec(channel=1, byte1=5, byte2=6, scale=-1),
            "pitch": AxisSpec(channel=2, byte1=1, byte2=2, scale=-1),
            "roll": AxisSpec(channel=2, byte1=3, byte2=4, scale=-1),
            "yaw": AxisSpec(channel=2, byte1=5, byte2=6, scale=1),
        },
        button_mapping=[
            ButtonSpec(channel=3, byte=1, bit=0),  # MENU
            ButtonSpec(channel=3, byte=3, bit=7),  # ALT
            ButtonSpec(channel=3, byte=4, bit=1),  # CTRL
            ButtonSpec(channel=3, byte=4, bit=0),  # SHIFT
            ButtonSpec(channel=3, byte=3, bit=6),  # ESC
            ButtonSpec(channel=3, byte=2, bit=4),  # 1
            ButtonSpec(channel=3, byte=2, bit=5),  # 2
            ButtonSpec(channel=3, byte=2, bit=6),  # 3
            ButtonSpec(channel=3, byte=2, bit=7),  # 4
            ButtonSpec(channel=3, byte=2, bit=0),  # ROLL CLOCKWISE
            ButtonSpec(channel=3, byte=1, bit=2),  # TOP
            ButtonSpec(channel=3, byte=4, bit=2),  # ROTATION
            ButtonSpec(channel=3, byte=1, bit=5),  # FRONT
            ButtonSpec(channel=3, byte=1, bit=4),  # REAR
            ButtonSpec(channel=3, byte=1, bit=1),  # FIT
        ],
        axis_scale=350.0,
    ),
    "SpaceMouse Wireless": DeviceSpec(
        name="SpaceMouse Wireless",
        # vendor ID and product ID
        hid_id=[0x256F, 0xC62E],
        # LED HID usage code pair
        led_id=[0x8, 0x4B],
        mappings={
            "x": AxisSpec(channel=1, byte1=1, byte2=2, scale=1),
            "y": AxisSpec(channel=1, byte1=3, byte2=4, scale=-1),
            "z": AxisSpec(channel=1, byte1=5, byte2=6, scale=-1),
            "pitch": AxisSpec(channel=1, byte1=7, byte2=8, scale=-1),
            "roll": AxisSpec(channel=1, byte1=9, byte2=10, scale=-1),
            "yaw": AxisSpec(channel=1, byte1=11, byte2=12, scale=1),
        },
        button_mapping=[
            ButtonSpec(channel=3, byte=1, bit=0),  # LEFT
            ButtonSpec(channel=3, byte=1, bit=1),  # RIGHT
        ],  # FIT
        axis_scale=350.0,
    ),
    "3Dconnexion Universal Receiver": DeviceSpec(
        name="3Dconnexion Universal Receiver",
        # vendor ID and product ID
        hid_id=[0x256F, 0xC652],
        # LED HID usage code pair
        led_id=[0x8, 0x4B],
        mappings={
            "x": AxisSpec(channel=1, byte1=1, byte2=2, scale=1),
            "y": AxisSpec(channel=1, byte1=3, byte2=4, scale=-1),
            "z": AxisSpec(channel=1, byte1=5, byte2=6, scale=-1),
            "pitch": AxisSpec(channel=1, byte1=7, byte2=8, scale=-1),
            "roll": AxisSpec(channel=1, byte1=9, byte2=10, scale=-1),
            "yaw": AxisSpec(channel=1, byte1=11, byte2=12, scale=1),
        },
        button_mapping=[
            ButtonSpec(channel=3, byte=1, bit=0),  # MENU
            ButtonSpec(channel=3, byte=3, bit=7),  # ALT
            ButtonSpec(channel=3, byte=4, bit=1),  # CTRL
            ButtonSpec(channel=3, byte=4, bit=0),  # SHIFT
            ButtonSpec(channel=3, byte=3, bit=6),  # ESC
            ButtonSpec(channel=3, byte=2, bit=4),  # 1
            ButtonSpec(channel=3, byte=2, bit=5),  # 2
            ButtonSpec(channel=3, byte=2, bit=6),  # 3
            ButtonSpec(channel=3, byte=2, bit=7),  # 4
            ButtonSpec(channel=3, byte=2, bit=0),  # ROLL CLOCKWISE
            ButtonSpec(channel=3, byte=1, bit=2),  # TOP
            ButtonSpec(channel=3, byte=4, bit=2),  # ROTATION
            ButtonSpec(channel=3, byte=1, bit=5),  # FRONT
            ButtonSpec(channel=3, byte=1, bit=4),  # REAR
            ButtonSpec(channel=3, byte=1, bit=1),  # FIT
        ],
        axis_scale=350.0,
    ),
    "SpacePilot": DeviceSpec(
        name="SpacePilot",
        # vendor ID and product ID
        hid_id=[0x46D, 0xC625],
        # LED HID usage code pair
        led_id=None,
        mappings={
            "x": AxisSpec(channel=1, byte1=1, byte2=2, scale=1),
            "y": AxisSpec(channel=1, byte1=3, byte2=4, scale=-1),
            "z": AxisSpec(channel=1, byte1=5, byte2=6, scale=-1),
            "pitch": AxisSpec(channel=2, byte1=1, byte2=2, scale=-1),
            "roll": AxisSpec(channel=2, byte1=3, byte2=4, scale=-1),
            "yaw": AxisSpec(channel=2, byte1=5, byte2=6, scale=1),
        },
        button_mapping=[
            ButtonSpec(channel=3, byte=1, bit=0), # 1
            ButtonSpec(channel=3, byte=1, bit=1), # 2
            ButtonSpec(channel=3, byte=1, bit=2), # 3
            ButtonSpec(channel=3, byte=1, bit=3), # 4
            ButtonSpec(channel=3, byte=1, bit=4), # 5
            ButtonSpec(channel=3, byte=1, bit=5), # 6
            ButtonSpec(channel=3, byte=1, bit=6), # T
            ButtonSpec(channel=3, byte=1, bit=7), # L
            ButtonSpec(channel=3, byte=2, bit=0), # R
            ButtonSpec(channel=3, byte=2, bit=1), # F
            ButtonSpec(channel=3, byte=2, bit=2), # Esc
            ButtonSpec(channel=3, byte=2, bit=3), # Alt
            ButtonSpec(channel=3, byte=2, bit=4), # Shift
            ButtonSpec(channel=3, byte=2, bit=5), # Ctrl
            ButtonSpec(channel=3, byte=2, bit=6), # Fit
            ButtonSpec(channel=3, byte=2, bit=7), # Panel
            ButtonSpec(channel=3, byte=3, bit=0), # Zoom -
            ButtonSpec(channel=3, byte=3, bit=1), # Zoom +
            ButtonSpec(channel=3, byte=3, bit=2), # Dom
            ButtonSpec(channel=3, byte=3, bit=3), # 3D Lock
            ButtonSpec(channel=3, byte=3, bit=4), # Config
        ],
        axis_scale=350.0,
    ),
    "SpacePilot Pro": DeviceSpec(
        name="SpacePilot Pro",
        # vendor ID and product ID
        hid_id=[0x46D, 0xC629],
        # LED HID usage code pair
        led_id=[0x8, 0x4B],
        mappings={
            "x": AxisSpec(channel=1, byte1=1, byte2=2, scale=1),
            "y": AxisSpec(channel=1, byte1=3, byte2=4, scale=-1),
            "z": AxisSpec(channel=1, byte1=5, byte2=6, scale=-1),
            "pitch": AxisSpec(channel=2, byte1=1, byte2=2, scale=-1),
            "roll": AxisSpec(channel=2, byte1=3, byte2=4, scale=-1),
            "yaw": AxisSpec(channel=2, byte1=5, byte2=6, scale=1),
        },
        button_mapping=[
            ButtonSpec(channel=3, byte=4, bit=0),  # SHIFT
            ButtonSpec(channel=3, byte=3, bit=6),  # ESC
            ButtonSpec(channel=3, byte=4, bit=1),  # CTRL
            ButtonSpec(channel=3, byte=3, bit=7),  # ALT
            ButtonSpec(channel=3, byte=3, bit=1),  # 1
            ButtonSpec(channel=3, byte=3, bit=2),  # 2
            ButtonSpec(channel=3, byte=2, bit=6),  # 3
            ButtonSpec(channel=3, byte=2, bit=7),  # 4
            ButtonSpec(channel=3, byte=3, bit=0),  # 5
            ButtonSpec(channel=3, byte=1, bit=0),  # MENU
            ButtonSpec(channel=3, byte=4, bit=6),  # -
            ButtonSpec(channel=3, byte=4, bit=5),  # +
            ButtonSpec(channel=3, byte=4, bit=4),  # DOMINANT
            ButtonSpec(channel=3, byte=4, bit=3),  # PAN/ZOOM
            ButtonSpec(channel=3, byte=4, bit=2),  # ROTATION
            ButtonSpec(channel=3, byte=2, bit=0),  # ROLL CLOCKWISE
            ButtonSpec(channel=3, byte=1, bit=2),  # TOP
            ButtonSpec(channel=3, byte=1, bit=5),  # FRONT
            ButtonSpec(channel=3, byte=1, bit=4),  # REAR
            ButtonSpec(channel=3, byte=2, bit=2),  # ISO
            ButtonSpec(channel=3, byte=1, bit=1),  # FIT
        ],
        axis_scale=350.0,
    ),
}