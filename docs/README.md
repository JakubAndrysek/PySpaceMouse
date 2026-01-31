# PySpaceMouse

🎮 Multiplatform Python library for 3Dconnexion SpaceMouse devices using raw HID.

3Dconnexion Space Mouse in Python using raw HID.
Note: you **don't** need to install or use any of the drivers or 3Dconnexion software to use this package.
It interfaces with the controller directly with `hidapi` and python wrapper library `easyhid`.

<p align="center">
<a href="https://hit.kubaandrysek.cz/?url=https%3A%2F%2Fgithub.com%2FJakubAndrysek%2Fpyspacemouse&chart=true"><img src="https://hit.kubaandrysek.cz/?url=https%3A%2F%2Fgithub.com%2FJakubAndrysek%2Fpyspacemouse"/></a>
</p>

<p align="center">
<img src="https://img.shields.io/github/license/JakubAndrysek/pyspacemouse?style=flat-square">
<img src="https://img.shields.io/github/stars/JakubAndrysek/pyspacemouse?style=flat-square">
<img src="https://img.shields.io/github/forks/JakubAndrysek/pyspacemouse?style=flat-square">
<img src="https://img.shields.io/github/issues/JakubAndrysek/pyspacemouse?style=flat-square">
<a href="https://www.pepy.tech/projects/pyspacemouse" target="_blank"><img src="https://static.pepy.tech/badge/pyspacemouse"></a>
</p>

[PySpaceMouse](https://github.com/JakubAndrysek/pyspacemouse) is forked from: [johnhw/pyspacenavigator](https://github.com/johnhw/pyspacenavigator) and modified to be multiplatform.

![](https://github.com/JakubAndrysek/pyspacemouse/raw/master/media/spacemouse-robot.jpg)

## Supported 3Dconnexion devices

* SpaceNavigator
* SpaceMouse Pro / Pro Wireless
* SpaceMouse Wireless
* SpaceMouse Compact
* SpaceMouse Enterprise
* SpacePilot / SpacePilot Pro
* 3Dconnexion Universal Receiver
* ...
* [Add more devices](https://spacemouse.kubaandrysek.cz/CONTRIBUTING/)

## Installation

```bash
pip install pyspacemouse
```

## Quick Start

```python
import pyspacemouse

# Context manager (recommended) - automatically closes device
with pyspacemouse.open() as device:
    while True:
        state = device.read()
        print(state.x, state.y, state.z)
```

## API Reference

From version 2.0.0 the API has been modularized and changed.
Please look at the [API Reference](./mouseApi/index.md) and [Examples](https://github.com/JakubAndrysek/PySpaceMouse/tree/master/examples) for more information.

### Device Discovery

```python
import pyspacemouse

# List connected SpaceMouse devices
pyspacemouse.get_connected_devices()
# Returns: ["SpaceNavigator", "SpaceMouse Pro", ...]

# List all supported device types
pyspacemouse.get_supported_devices()
# Returns: [(name, vendor_id, product_id), ...]

# List ALL HID devices (for debugging)
pyspacemouse.get_all_hid_devices()
# Returns: [(product, manufacturer, vid, pid), ...]
```

### Opening Devices

```python
# Auto-detect and open first device
with pyspacemouse.open() as device:
    state = device.read()

# Open specific device by name
with pyspacemouse.open(device="SpaceNavigator") as device:
    state = device.read()

# Open second device when multiple identical devices are connected
with pyspacemouse.open(device_index=1) as device:
    state = device.read()

# Open by filesystem path (Linux: /dev/hidraw0)
with pyspacemouse.open_by_path("/dev/hidraw0") as device:
    state = device.read()
```

### Reading State

```python
with pyspacemouse.open() as device:
    state = device.read()

    # 6-DOF axes (range: -1.0 to 1.0)
    print(state.x, state.y, state.z)       # Translation
    print(state.roll, state.pitch, state.yaw)  # Rotation

    # Buttons (list of 0/1)
    print(state.buttons)

    # Timestamp
    print(state.t)
```

### Callbacks

```python
# Button callback
def on_button(state, buttons, pressed):
    print(f"Button {pressed} pressed!")

button_callbacks = [
    pyspacemouse.ButtonCallback(0, on_button),  # Button 0
    pyspacemouse.ButtonCallback([0, 1], on_button),  # Both 0 and 1
]

# DOF callback with filtering
dof_callbacks = [
    pyspacemouse.DofCallback(
        axis="x",
        callback=lambda s, v: print(f"X: {v}"),
        callback_minus=lambda s, v: print(f"X negative: {v}"),
        filter=0.1,  # Deadzone
        sleep=0.05,  # Rate limit
    ),
]

with pyspacemouse.open(
    button_callbacks=button_callbacks,
    dof_callbacks=dof_callbacks,
) as device:
    while True:
        device.read()  # Triggers callbacks
```

### Custom Axis Mapping

Customize axis directions for specific coordinate conventions (ROS, OpenGL, etc.):

```python
import pyspacemouse

# Get existing device spec and modify axes
specs = pyspacemouse.get_device_specs()
base = specs["SpaceNavigator"]

# Invert axes for your application
custom = pyspacemouse.modify_device_info(
    base,
    invert_axes=["y", "z", "roll", "yaw"],  # Invert these
)

with pyspacemouse.open(device_spec=custom) as device:
    state = device.read()
```

See [Custom Device Configuration](./mouseApi/index.md#custom-device-configuration) for full API.

## CLI

```bash
pyspacemouse --list-connected    # Show connected devices
pyspacemouse --list-supported    # Show all supported types
pyspacemouse --list-hid          # Show all HID devices
pyspacemouse --test              # Test connection
pyspacemouse --version           # Show version
```

## Examples

See the [examples/](https://github.com/JakubAndrysek/PySpaceMouse/tree/master/examples) directory:

| Example | Description |
|---------|-------------|
| `01_basic.py` | Simple reading with context manager |
| `02_callbacks.py` | Button and DOF callbacks |
| `03_multi_device.py` | Using two devices simultaneously |
| `04_open_by_path.py` | Open specific device by path |
| `05_discovery.py` | List and inspect devices |
| `06_axis_callbacks.py` | Per-axis callbacks with filtering |
| `07_led.py` | LED control |
| `08_buttons.py` | Button names and handling |
| `09_custom_config.py` | Custom axis mappings |

## Dependencies

### hidapi (C library)

- **Linux**: `sudo apt-get install libhidapi-dev`
- **macOS**: `brew install hidapi`
- **Windows**: Download from [hidapi releases](https://github.com/libusb/hidapi/releases)

### Linux permissions

```bash
echo 'KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0664", GROUP="plugdev"' | sudo tee /etc/udev/rules.d/99-hidraw-permissions.rules
sudo usermod -aG plugdev $USER
newgrp plugdev
```

### macOS PATH

```bash
export DYLD_LIBRARY_PATH=/opt/homebrew/Cellar/hidapi/<VERSION>/lib:$DYLD_LIBRARY_PATH
```

## Troubleshooting

See [troubleshooting.md](./troubleshooting.md) for help with common issues.

## Developing / Contributing

This project includes a `Makefile` with commands for creating a virtual environment (using hatch), and publishing to pypi.

You will need `hatch` and `pre-commit` for this.
You can get these by using

```
pipx install hatch==1.15.1 pre-commit
```

If you're not familiar with pipx, it lets you install python tools into isolated environments in `~/.local`.

## Used In

- [TeleMoMa](https://github.com/UT-Austin-RobIn/telemoma) - A Modular and Versatile Teleoperation System for Mobile Manipulation
- [SERL](https://github.com/rail-berkeley/serl) - SERL: A Software Suite for Sample-Efficient Robotic Reinforcement Learning
    - ![](https://github.com/rail-berkeley/serl/raw/e59dc0d2721399af2e629d7bcad678fa2ffce9ae/docs/images/tasks-banner.gif)
- [Pancake Robot](https://github.com/pauldw/pancake-robot)- An integration of the Ufactory Lite 6 robot arm with kitchenware to make pancakes.
- [GELLO](https://github.com/wuphilipp/gello_software) - GELLO: A General, Low-Cost, and Intuitive Teleoperation Framework for Robot Manipulators
    - ![image](https://github.com/wuphilipp/gello_software/assets/33494544/229d90b5-c758-4c14-ab37-d4b2ed7ad50b)
- [spacepad](https://github.com/brianpeiris/spacepad) - A simple python script that turns a spacemouse device into a standard gamepad
- [arm_xarm](https://github.com/johnrso/arm_xarm)
