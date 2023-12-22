from collections import namedtuple
from typing import Callable, Union, List

# axis mappings are specified as:
# [channel, byte1, byte2, scale]; scale is usually just -1 or 1 and multiplies the result by this value
# (but per-axis scaling can also be achieved by setting this value)
# byte1 and byte2 are indices into the HID array indicating the two bytes to read to form the value for this axis
# For the SpaceNavigator, these are consecutive bytes following the channel number.
AxisSpec = namedtuple("AxisSpec", ["channel", "byte1", "byte2", "scale"])

# button states are specified as:
# [channel, data byte, bit of byte, index to write to]
# If a message is received on the specified channel, the value of the data byte is set in the button bit array
ButtonSpec = namedtuple("ButtonSpec", ["channel", "byte", "bit"])

# tuple for 6DOF results
SpaceNavigator = namedtuple(
    "SpaceNavigator", ["t", "x", "y", "z", "roll", "pitch", "yaw", "buttons"]
)


class ButtonState(list):
    def __int__(self):
        return sum((b << i) for (i, b) in enumerate(reversed(self)))


class ButtonCallback:
    """Register new button callback"""

    def __init__(
            self, buttons: Union[int, List[int]], callback: Callable[[int, int], None]
    ):
        self.buttons = buttons
        self.callback = callback


class DofCallback:
    """Register new DoF callback"""

    def __init__(
            self,
            axis: str,
            callback: Callable[[int], None],
            sleep: float = 0.0,
            callback_minus: Callable[[int], None] = None,
            filter: float = 0.0
    ):
        self.axis = axis
        self.callback = callback
        self.sleep = sleep
        self.callback_minus = callback_minus
        self.filter = filter
