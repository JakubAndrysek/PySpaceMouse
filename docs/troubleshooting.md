# Troubleshooting

If you encounter any issues, you can find help in the following section.

## Axis Conventions

The library applies some axis inversions to make values more intuitive:

- **Z axis**: Inverted so positive = up (HID spec defines down as positive)
- **Y axis**: Inverted for common conventions
- **Rotations**: pitch/roll inverted from HID spec

If your application needs a common coordinate convention, pass it when opening the device:

```python
import pyspacemouse
from pyspacemouse import AxisConvention

with pyspacemouse.open(axis_convention=AxisConvention.ROS) as device:
    state = device.read()
```

For custom conventions, use `modify_device_info()` to remap or invert axes:

```python
import pyspacemouse

specs = pyspacemouse.get_device_specs()
base = specs["SpaceNavigator"]

custom = pyspacemouse.modify_device_info(
    base,
    remap_axes={"x": "y", "y": ("x", -1), "yaw": ("yaw", -1)},
)

with pyspacemouse.open(device_spec=custom) as device:
    state = device.read()
```

See [Custom Device Configuration](https://spacemouse.kubaandrysek.cz/mouseApi#custom-device-configuration) for full details.


## Common issues

### ModuleNotFoundError: No module named 'hid'

- The [`hidapi`](https://pypi.org/project/hidapi/) package is missing. It is installed
  automatically with `pyspacemouse`, so this usually means you are in a different
  environment than you think. Install it with `pip install hidapi`.

### ImportError: The `hid` module ... is not cython-hidapi

- The [`hid`](https://pypi.org/project/hid/) package (pyhidapi) is installed and is
  shadowing the module `hidapi` provides. Both distributions install a top-level module
  called `hid`, so only one of them can be imported at a time.
- Remove the other one and reinstall:

  ```bash
  pip uninstall hid
  pip install --force-reinstall hidapi
  ```


<hr>

## Checking your device is visible

The hidapi C library ships inside the `hidapi` wheel, so there is nothing to install or
verify. When something is wrong it is almost always the device or its permissions.

The CLI goes through the same backend the library does, so trust it over external tools:

```bash
pyspacemouse --list-hid         # every HID device the system exposes
pyspacemouse --list-connected   # the ones recognised as SpaceMice
pyspacemouse --test             # open the first one and print live axis values
```

??? note "My output"
    ```bash
    $ pyspacemouse --list-connected
    Connected SpaceMouse devices:
      - SpaceMouseCompact (/dev/hidraw5)
    ```

Work down from the top:

- **Nothing in `--list-hid`** - the OS isn't seeing the device at all. Check the cable, try
  another port, and on a wireless model check the receiver.
- **In `--list-hid` but not `--list-connected`** - the device is visible but its VID/PID
  isn't in the device table. Compare against `pyspacemouse --list-supported`, then open an
  issue with the IDs or supply your own `device_spec`.
- **In `--list-connected` but `--test` won't open** - permissions; see the Linux section
  below. If you have 3DxWare installed, try quitting it first.
- **Opens, but the axes do nothing** - the device is being read but its report layout
  doesn't match the spec. See [Adding a new device](./CONTRIBUTING.md#adding-a-new-device).

<hr>

## Linux

### Failed to open device / Permission denied

If you encounter an error like `Failed to open device` or `Permission denied` when trying to use your SpaceMouse on Linux, this is typically a permissions issue. Normal users don't have permission to access HID devices by default.

**Error example:**
```bash
Traceback (most recent call last):
  File "/home/user/.local/lib/python3.12/site-packages/pyspacemouse/device.py", line 185, in open
    device.open_path(self._hid_info["path"])
  File "hidraw.pyx", line 158, in hidraw.device.open_path
OSError: open failed

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/user/.local/lib/python3.12/site-packages/pyspacemouse/device.py", line 187, in open
    raise RuntimeError("Failed to open device") from e
RuntimeError: Failed to open device
```

**Solution:**

1. **Find your device's Vendor ID and Product ID:**
   ```bash
   lsusb
   ```
   Look for your SpaceMouse device. Example output:
   ```
   Bus 001 Device 013: ID 256f:c652 3Dconnexion Universal Receiver
   ```
   Here, `256f` is the Vendor ID and `c652` is the Product ID.

2. **Create udev rules to grant permissions:**
   ```bash
   cd /etc/udev/rules.d
   sudo touch 99-spacemouse.rules
   sudo nano 99-spacemouse.rules
   ```

3. **Add the following rules** (replace `046d` and `c62b` with your Vendor ID and Product ID):
   ```bash
   SUBSYSTEM=="hidraw", ATTRS{idVendor}=="046d", ATTRS{idProduct}=="c62b", MODE="0664", GROUP="input", TAG+="uaccess"
   SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", ATTR{idVendor}=="046d", ATTR{idProduct}=="c62b", MODE="0664", GROUP="input", TAG+="uaccess"
   ```

   Common SpaceMouse IDs:
   - SpaceMouse Compact: `256f:c635`
   - SpaceMouse Wireless: `256f:c62e`
   - 3Dconnexion Universal Receiver: `256f:c652`
   - SpaceNavigator: `046d:c626`

4. **Reload udev rules:**
   ```bash
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

5. **Add your user to the input group:**
   ```bash
   sudo usermod -a -G input $USER
   ```

6. **Disconnect and reconnect your SpaceMouse**, then log out and log back in to Ubuntu (or restart your computer).

After these steps, your SpaceMouse should work correctly without permission errors.

<hr>
