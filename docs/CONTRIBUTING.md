# Development guide

## Adding new features
1. Create a new branch from `master` with a descriptive name.
2. Implement your feature.
3. Create a pull request to `master` and assign a reviewer.
4. The reviewer will review your code and merge it into `master`.

## Adding a new device

This section describes how to add support for a new SpaceMouse or similar 6-DOF device.

### 1. Find Device IDs

First, identify your device's **Vendor ID (VID)** and **Product ID (PID)**.

**Linux/macOS:**
```bash
lsusb
# Example output: Bus 001 Device 013: ID 256f:c652 3Dconnexion Universal Receiver
# VID = 256f, PID = c652
```

**Using [hidapitester](https://github.com/todbot/hidapitester):**
```bash
./hidapitester --list
# Example: 046D/C626: 3Dconnexion - SpaceNavigator
```

### 2. Analyze HID Data

Use `hidapitester` to read raw data from your device:

```bash
./hidapitester --vidpid <VID/PID> --open --read-input
```

Move the SpaceMouse knob in each direction and identify which bytes change:

- **Channel 1**: Usually translation data (X, Y, Z)
- **Channel 2**: Usually rotation data (pitch, roll, yaw)
- **Channel 3**: Button data

Each axis is typically a signed 16-bit value (2 bytes, little-endian).

### 3. Add Device to `devices.toml`

Edit `pyspacemouse/devices.toml` and add your device:

```toml
[YourDeviceName]
hid_id = [0xVID, 0xPID]          # Vendor ID and Product ID in hex
led_id = [0x04, 0x01]            # Optional: [report_id, on_value] for LED control
axis_scale = 350.0               # Scaling factor (adjust based on device sensitivity)

# Axis mappings: [channel, byte1, byte2, scale]
# - channel: HID report number (1, 2, or 3)
# - byte1, byte2: Byte positions for the 16-bit value
# - scale: 1 for normal, -1 for inverted axis
mappings.x     = [1, 1, 2, 1]
mappings.y     = [1, 3, 4, -1]
mappings.z     = [1, 5, 6, -1]
mappings.pitch = [2, 1, 2, -1]
mappings.roll  = [2, 3, 4, -1]
mappings.yaw   = [2, 5, 6, 1]

# Button mappings: [channel, byte, bit]
[YourDeviceName.buttons]
LEFT = [3, 1, 0]                 # Channel 3, byte 1, bit 0
RIGHT = [3, 1, 1]                # Channel 3, byte 1, bit 1
```

**Mapping format explained:**

| Field | Description |
|-------|-------------|
| `channel` | HID report ID (first byte of each HID message) |
| `byte1`, `byte2` | Byte positions within the report (1-indexed) |
| `scale` | Sign modifier: `1` = normal, `-1` = inverted |
| `bit` | For buttons: which bit in the byte (0-7) |

### 4. Test Your Configuration

```python
import pyspacemouse

# Check if device is recognized
devices = pyspacemouse.get_connected_devices()
print(devices)  # Should show your device name

# Test reading
with pyspacemouse.open() as device:
    while True:
        state = device.read()
        print(f"X:{state.x:.2f} Y:{state.y:.2f} Z:{state.z:.2f}")
        print(f"Roll:{state.roll:.2f} Pitch:{state.pitch:.2f} Yaw:{state.yaw:.2f}")
        print(f"Buttons: {state.buttons}")
```

### 5. Fine-tune Axis Directions

If an axis moves in the wrong direction, change its `scale` from `1` to `-1` or vice versa in `devices.toml`.

### 6. Submit a Pull Request

Once your device works correctly:

1. Create a branch: `git checkout -b add-device-<name>`
2. Add your device entry to `devices.toml`
3. Test thoroughly with the examples in `examples/`
4. Submit a PR with your device name and any notes about testing

### Using Custom Configuration (Without Modifying Library)

If you don't want to modify the library, use `create_device_info()`:

```python
import pyspacemouse

device_spec = pyspacemouse.create_device_info({
    "name": "MyCustomDevice",
    "hid_id": [0x256F, 0xC652],
    "axis_scale": 350.0,
    "mappings": {
        "x": [1, 1, 2, 1],
        "y": [1, 3, 4, -1],
        "z": [1, 5, 6, -1],
        "pitch": [2, 1, 2, -1],
        "roll": [2, 3, 4, -1],
        "yaw": [2, 5, 6, 1],
    },
    "buttons": {
        "LEFT": [3, 1, 0],
        "RIGHT": [3, 1, 1],
    },
})

with pyspacemouse.open(device_spec=device_spec) as device:
    state = device.read()
```

See [Custom Device Configuration](https://spacemouse.kubaandrysek.cz/mouseApi/#custom-device-configuration) for more details.

## How to write documentation
To install the required dependencies, run `pip install pyspacemouse[docs]`.

Edit `README.md` only in the root folder. The documentation is automatically generated from `README.md` and `docs/` folder.
To update documentation from root to `/docs` use macro `make fixRelativeLinkDocs` which will replace all relative links from `/` to `/docs` folder.

### Building the documentation
The documentation is built using [mkdocs](https://www.mkdocs.org/). To test the documentation locally, run `make docs-serve` and open [http://localhost:8000](http://localhost:8000) in your browser.

### Deploying the documentation
The documentation is deployed automatically using GitHub Actions. Just push to the `master` branch and the documentation will be updated automatically.
