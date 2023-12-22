import copy
import sys
from typing import Callable, List

from easyhid import Enumeration

from pyspacemouse.checks import check_config, DeprecatedFunctionException, DeviceNotFoundException, \
    DeviceNotOpenException, InstallationException
from pyspacemouse.configuration import device_specs
from pyspacemouse.devices import Config, DofCallback, ButtonCallback, DeviceSpec

# current version number
__version__ = "1.1.0"


def close():
    """Close the active device, if it exists"""
    raise DeprecatedFunctionException("Deprecated function. Use non global close() instead")


def read():
    """Return the current state of the active navigation controller."""
    raise DeprecatedFunctionException("Deprecated function. Use non global read() instead")


def list_devices():
    """Return a list of the supported devices connected

    Returns:
        A list of string names of the devices supported which were found. Empty if no supported devices found
    """
    devices = []
    try:
        hid = Enumeration()
    except AttributeError as e:
        raise InstallationException("HID API is probably not installed. See README.md for details.") from e

    all_hids = hid.find()

    if all_hids:
        for device in all_hids:
            devices.extend(
                device_name
                for device_name, spec in device_specs.items()
                if (
                        device.vendor_id == spec.hid_id[0]
                        and device.product_id == spec.hid_id[1]
                )
            )
    return devices


def get_supported_devices():
    """Return a list of the supported devices

    Returns:
        A list of string names of the devices supported
    """
    return list(device_specs.keys())


def open_config(config: Config, set_nonblocking_loop: bool = True, device=None, device_number=0) -> DeviceSpec:
    """
    Open a 3D space navigator device. Same as open() but input one config file -> class Config

    Returns:
        Device object if the device was opened successfully
        None if the device could not be opened
    """

    return open(config.callback, config.dof_callback, config.dof_callback_arr, config.button_callback,
                config.button_callback_arr, set_nonblocking_loop, device, device_number)


def openCfg(config: Config, set_nonblocking_loop: bool = True, device=None, device_number=0) -> DeviceSpec:
    """
    Open a 3D space navigator device. Same as open() but input one config file -> class Config

    Returns:
        Device object if the device was opened successfully
        None if the device could not be opened
    """
    sys.stderr.write("openCfg() is deprecated. Use open_config() instead\n")
    return open_config(config, set_nonblocking_loop, device, device_number)


def open(
        callback: Callable[[object], None] = None,
        dof_callback: Callable[[object], None] = None,
        dof_callback_arr: List[DofCallback] = None,
        button_callback: Callable[[object, list], None] = None,
        button_callback_arr: List[ButtonCallback] = None,
        set_nonblocking_loop=True,
        device: str = None,
        path: str = None,
        device_number: int = 0) -> DeviceSpec:
    """
    Open a 3D space navigator device. Makes this device the current active device, which enables the module-level read() and close()
    calls. For multiple devices, use the read() and close() calls on the returned object instead, and don't use the module-level calls.

    Parameters:
        callback: If callback is provided, it is called only on DoF state changes with a copy of the current state tuple.
        dof_callback: If dof_callback is provided, it is called only on DOF state changes with the argument (state).
        dof_callback_arr: If dof_callback_arr is provided, it is called only on DOF state changes with the argument (state, axis).
        button_callback: If button_callback is provided, it is called only on button state changes with the argument (state, buttons).
        button_callback_arr: If button_callbacks_arr is provided, it is called only on specific button state true with the argument (state, buttons, pressed_buttons).
        set_nonblocking_loop: Disable waiting for input from SpaceMouse. It is required for using callbacks
        device: name of device to open. Must be one of the values in supported_devices. If None, chooses the first supported device found.
        path: path of the device to open. If path is specified it will try to open at that path regardless of what is connected to it
        device_number: use the first (device_number=0) device you find. (for universal wireless receiver)
    Returns:
        Device object if the device was opened successfully
        None if the device could not be opened
    """

    # if no device name specified, look for any matching device and choose the first
    if device is None:
        all_devices = list_devices()
        if len(all_devices) > 0:
            device = all_devices[0]
        else:
            raise DeviceNotFoundException("No device connected/supported!")

    found_devices = []
    hid = Enumeration()
    all_hids = hid.find()
    if not all_hids:
        raise DeviceNotFoundException("No HID devices detected")

    for devices in all_hids:
        if path:
            devices.path = path
        spec = device_specs[device]
        if devices.vendor_id == spec.hid_id[0] and devices.product_id == spec.hid_id[1]:
            found_devices.append({"Spec": spec, "HIDDevice": devices})
            print(f"{device} found")

    if not found_devices:
        raise DeviceNotFoundException("No supported devices found")
    if len(found_devices) <= device_number:
        device_number = 0

    if len(found_devices) > device_number:
        # Check that the input configuration has the correct components
        # Raise an exception if it encounters incorrect component.
        check_config(callback, dof_callback, dof_callback_arr, button_callback, button_callback_arr)
        # create a copy of the device specification
        spec = found_devices[device_number]["Spec"]
        devices = found_devices[device_number]["HIDDevice"]
        new_device = copy.deepcopy(spec)
        new_device.device = devices

        # set the callbacks
        new_device.callback = callback
        new_device.dof_callback = dof_callback
        new_device.dof_callback_arr = dof_callback_arr
        new_device.button_callback = button_callback
        new_device.button_callback_arr = button_callback_arr
        # open the device
        new_device.open()
        # set nonblocking/blocking mode
        new_device.set_nonblocking_loop = set_nonblocking_loop
        devices.set_nonblocking(set_nonblocking_loop)
        return new_device

    raise DeviceNotOpenException("Device not open")


def config_set(config: Config):
    """Set new configuration of mouse from Config class"""
    raise DeprecatedFunctionException("Deprecated function. Use non global config_set() instead")


def config_set_sep(callback=None, dof_callback=None, dof_callback_arr=None, button_callback=None,
                   button_callback_arr=None):
    """Set new configuration of mouse and check that the configuration has correct parts"""
    raise DeprecatedFunctionException("Deprecated function. Use non global config_set_sep() instead")


def config_remove():
    """Remove old configuration"""
    raise DeprecatedFunctionException("Deprecated function. Use non global config_remove() instead")


def print_state(state):
    """Simple default DoF callback
    Print all axis to output
    """
    if state:
        print(
            " ".join(
                [
                    "%4s %+.2f" % (k, getattr(state, k))
                    for k in ["x", "y", "z", "roll", "pitch", "yaw", "t"]
                ]
            )
        )


def silent_callback(state):
    """Silent callback
    Does nothing
    """
    pass


def print_buttons(state, buttons):
    """Simple default button callback
    Print all buttons to output
    """
    # simple default button callback
    print(
        (
                (
                        "["
                        + " ".join(["%2d, " % buttons[k] for k in range(len(buttons))])
                )
                + "]"
        )
    )


# def toggle_led(state, buttons):
#     print("".join(["buttons=", str(buttons)]))
#     # Switch on the led on left push, off on right push
#     if buttons[0] == 1:
#         set_led(1)
#     if buttons[1] == 1:
#         set_led(0)
#
#
# def set_led(state):
#     if _active_device:
#         _active_device.set_led(state)


if __name__ == "__main__":

    def butt_0(state, buttons, pressed_buttons):
        print("Button 0")


    def butt_2_3(state, buttons, pressed_buttons):
        print("Button 2 and 3")


    button_callbacks_arr = [
        ButtonCallback([0], butt_0),
        ButtonCallback([1], lambda state, buttons, pressed_buttons: print("Button 1")),
        ButtonCallback([2, 3], butt_2_3),
    ]

    dev = open(dof_callback=print_state, button_callback=print_buttons, button_callback_arr=button_callbacks_arr)

    while True:
        state = dev.read()
