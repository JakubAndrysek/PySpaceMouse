# PySpaceMouse

🎮 Multiplatform Python library for 3Dconnexion SpaceMouse devices using raw HID.

3Dconnexion Space Mouse in Python using raw HID.
Note: you **don't** need to install or use any of the drivers or 3Dconnexion software to use this package.
It interfaces with the controller directly with `hidapi` and python wrapper library `easyhid`.

<p align="center">
<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FJakubAndrysek%2Fpyspacemouse&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=true"/></a>
<img src="https://img.shields.io/github/license/JakubAndrysek/pyspacemouse?style=flat-square">
<img src="https://img.shields.io/github/stars/JakubAndrysek/pyspacemouse?style=flat-square">
<img src="https://img.shields.io/github/forks/JakubAndrysek/pyspacemouse?style=flat-square">
<img src="https://img.shields.io/github/issues/JakubAndrysek/pyspacemouse?style=flat-square">
<a href="https://www.pepy.tech/projects/pyspacemouse" target="_blank"><img src="https://static.pepy.tech/badge/pyspacemouse"></a>
</p>

[PySpaceMouse](https://github.com/JakubAndrysek/pyspacemouse) is forked from: [johnhw/pyspacenavigator](https://github.com/johnhw/pyspacenavigator)

Implements a simple interface for 6 DoF 3Dconnexion [Space Mouse](https://3dconnexion.com/uk/spacemouse/) device as
well as similar devices.

![](https://github.com/JakubAndrysek/pyspacemouse/raw/master/media/spacemouse-robot.jpg)
Control [Robo Arm](https://roboruka.robotickytabor.cz/) with a Space Mouse.

## Supported 3Dconnexion devices

* SpaceNavigator
* SpaceMouse Pro
* SpaceMouse Pro Wireless
* SpaceMouse Wireless
* 3Dconnexion Universal Receiver
* SpaceMouse Compact
* SpacePilot
* SpacePilot Pro
* SpaceMouse Enterprise
* [Add more devices](https://github.com/johnhw/pyspacenavigator/issues/1)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [pyspacemouse](https://pypi.org/project/pyspacemouse/). If you are using a Mac with an ARM processor, you'll need a patched version of `easyhid`.

```bash
# Install package
pip install pyspacemouse

# Only needed for ARM MacOs
pip install git+https://github.com/bglopez/python-easyhid.git
```

## Dependencies (required)

The library uses `hidapi` as low-level interface to the device and `easyhid` as a Python abstraction for easier use.

- ### [hidapi](https://github.com/libusb/hidapi) is `C` library for direct communication with HID devices
    - #### Linux
        - [libhidapi-dev]() to access HID data
        - `sudo apt-get install libhidapi-dev` (Debian/Ubuntu)
        - Compile and install [hidapi](https://github.com/libusb/hidapi/#build-from-source).  (other Linux
          distributions)

        - add rules for permissions
            ```bash
            sudo echo 'KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0664", GROUP="plugdev"' > /etc/udev/rules.d/99-hidraw-permissions.rules
            sudo usermod -aG plugdev $USER
            newgrp plugdev
            ```
            <details>
            <summary>Aleternative option - with tee (RPi)</summary>
            <pre>
            echo 'KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0664", GROUP="plugdev"' | sudo tee /etc/udev/rules.d/99-hidraw-permissions.rules
            sudo usermod -aG plugdev $USER
            newgrp plugdev
            </pre>
            </details>

    - ### Windows
        - Install the latest release of hidapi.dll and hidapi.lib from
          the [hidapi releases](https://github.com/libusb/hidapi/releases) page.
        - Set system environment: add absolute path for `x64` or `x86` folder in Path.
        - More info on [Troubleshooting - WIndows](./troubleshooting.md#windows) page.

    - ### Mac OS X (M1)
        - Install from [Homebrew](https://formulae.brew.sh/formula/hidapi)
        - `brew install hidapi`
        - Add hidapi to your `DYLD_LIBRARY_PATH` directory.
            ```bash
            export DYLD_LIBRARY_PATH=/opt/homebrew/Cellar/hidapi/0.14.0/lib:$DYLD_LIBRARY_PATH
            ```
        - On MacOS M1 you will need patched version of easyhid. If easyhid is already installed, please uninstall it first.
            ```bash
            pip install git+https://github.com/bglopez/python-easyhid.git
            ```
        - In case of problem with M1 chip, try to run you code with Rosseta 2
            - How to use Rosseta 2 - [Setup Rosetta](https://apple.stackexchange.com/questions/428768/on-apple-m1-with-rosetta-how-to-open-entire-terminal-iterm-in-x86-64-architec)
        - Tested and developed by [consi](https://github.com/JakubAndrysek/PySpaceMouse/issues/10#issuecomment-1768362007) - thanks!
        - More info on [Troubleshooting - Mac OS (M1)](./troubleshooting.md#mac-os-m1) page.

- ### [easyhid](https://github.com/bglopez/python-easyhid) is `hidapi` interface for Python - required on all platforms
    - `pip install git+https://github.com/bglopez/python-easyhid.git`
    - this fork fix problems with `hidapi` on MacOS.
    - on other platforms it possible works with original package `pip install easyhid`

## Basic Usage:

If the 3Dconnexion driver is installed, please ensure to stop `3DconnexionHelper` before running your python scripts.



## Basic example

````py
import pyspacemouse
import time

success = pyspacemouse.open(dof_callback=pyspacemouse.print_state, button_callback=pyspacemouse.print_buttons)
if success:
    while 1:
        state = pyspacemouse.read()
        time.sleep(0.01)
````
More examples can be found in the [/examples](https://github.com/JakubAndrysek/PySpaceMouse/tree/master/examples) directory or in page with [Examples](https://spacemouse.kubaandrysek.cz/mouseApi/examples/).

## Available CLI test commands
```bash
usage: pyspacemouse [-h] [--version] [--list-spacemouse]
                    [--list-supported-devices] [--list-all-hid-devices]
                    [--test-connect]

PySpaceMouse CLI

options:
  -h, --help            show this help message and exit
  --version             Version of pyspacemouse
  --list-spacemouse     List connected SpaceMouse devices
  --list-supported-devices
                        List supported SpaceMouse devices
  --list-all-hid-devices
                        List all connected HID devices
  --test-connect        Test connect to the first available device

For more information, visit https://spacemouse.kubaandrysek.cz
```


## Troubleshooting

Look at the [Troubleshooting](./troubleshooting.md) page for help with common issues.

## References

PySpaceMouse is used in the following projects:

- [PySpaceApp](https://github.com/JakubAndrysek/pyspaceapp) - Control your PC with SpaceMouse (basic hotkeys, mouse control, and more)
- [TeleMoMa](https://github.com/UT-Austin-RobIn/telemoma) - A Modular and Versatile Teleoperation System for Mobile Manipulation
- [SERL](https://github.com/rail-berkeley/serl) - SERL: A Software Suite for Sample-Efficient Robotic Reinforcement Learning
    - ![](https://github.com/rail-berkeley/serl/raw/e59dc0d2721399af2e629d7bcad678fa2ffce9ae/docs/images/tasks-banner.gif)
- [Pancake Robot](https://github.com/pauldw/pancake-robot)- An integration of the Ufactory Lite 6 robot arm with kitchenware to make pancakes.
- [GELLO](https://github.com/wuphilipp/gello_software) - GELLO: A General, Low-Cost, and Intuitive Teleoperation Framework for Robot Manipulators
    - ![image](https://github.com/wuphilipp/gello_software/assets/33494544/229d90b5-c758-4c14-ab37-d4b2ed7ad50b)
- [spacepad](https://github.com/brianpeiris/spacepad) - A simple python script that turns a spacemouse device into a standard gamepad
- [arm_xarm](https://github.com/johnrso/arm_xarm)
