from typing import List

from pyspacemouse.devices import ButtonCallback, DofCallback


def check_config(callback=None, dof_callback=None, dof_callback_arr=None, button_callback=None,
                 button_callback_arr=None):
    """Check that the input configuration has the correct components.
    Raise an exception if it encounters incorrect component.
    """
    if dof_callback_arr and check_dof_callback_arr(dof_callback_arr):
        pass
    if button_callback_arr and check_button_callback_arr(button_callback_arr):
        pass


def check_button_callback_arr(button_callback_arr: List[ButtonCallback]) -> List[ButtonCallback]:
    """Check that the button_callback_arr has the correct components.
    Raise an exception if it encounters incorrect component.
    """
    # foreach ButtonCallback
    for num, butt_call in enumerate(button_callback_arr):
        if not isinstance(butt_call, ButtonCallback):
            raise ButtonCallbackException(f"'ButtonCallback[{num}]' is not instance of 'ButtonCallback'")
        if type(butt_call.buttons) is int:
            pass
        elif type(butt_call.buttons) is list:
            for b_num, butt in enumerate(butt_call.buttons):
                if type(butt) is not int:
                    raise ButtonCallbackException(f"'ButtonCallback[{num}]:buttons[{b_num}]' is not type int")
        else:
            raise ButtonCallbackException(f"'ButtonCallback[{num}]:buttons' is not type int or list of int")
        if not callable(butt_call.callback):
            raise ButtonCallbackException(f"'ButtonCallback[{num}]:callback' is not callable")
    return button_callback_arr


def check_dof_callback_arr(dof_callback_arr: List[DofCallback]) -> List[DofCallback]:
    """Check that the dof_callback_arr has the correct components.
    Raise an exception if it encounters incorrect component."""

    # foreach DofCallback
    for num, dof_call in enumerate(dof_callback_arr):
        if not isinstance(dof_call, DofCallback):
            raise DofCallbackException(f"'DofCallback[{num}]' is not instance of 'DofCallback'")

        # has the correct axis name
        if dof_call.axis not in ["x", "y", "z", "roll", "pitch", "yaw"]:
            raise DofCallbackException(
                f"'DofCallback[{num}]:axis' is not string from ['x', 'y', 'z', 'roll', 'pitch', 'yaw']")

        # is callback callable
        if not callable(dof_call.callback):
            raise DofCallbackException(f"'DofCallback[{num}]:callback' is not callable")

        # is sleep type float
        if type(dof_call.sleep) is not float:
            raise DofCallbackException(f"'DofCallback[{num}]:sleep' is not type float")

        # is callback_minus callable
        if not dof_call.callback_minus or not callable(dof_call.callback_minus):
            raise DofCallbackException(f"'DofCallback[{num}]:callback_minus' is not callable")

        # is filter type float
        if not dof_call.filter or type(dof_call.filter) is not float:
            raise DofCallbackException(f"'DofCallback[{num}]:filter' is not type float")
    return dof_callback_arr


# custom exceptions

# Deprecated function
class DeprecatedFunctionException(Exception):
    pass


# connecting problems
class DeviceNotFoundException(Exception):
    pass


class DeviceNotOpenException(Exception):
    pass


class InstallationException(Exception):
    pass


class DofCallbackException(Exception):
    pass


class ButtonCallbackException(Exception):
    pass
