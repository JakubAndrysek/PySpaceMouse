import timeit
from typing import Callable, Union, List

from easyhid import HIDException

from pyspacemouse.abstraction import DofCallback, SpaceNavigator, ButtonState, ButtonCallback
# from pyspacemouse.checks import check_config



# clock for timing
high_acc_clock = timeit.default_timer


class Config:
    """Create new config file with correct structure and check that the configuration has correct parts"""

    def __init__(
            self,
            callback: Callable[[object], None] = None,
            dof_callback: Callable[[object], None] = None,
            dof_callback_arr: List[DofCallback] = None,
            button_callback: Callable[[object, list], None] = None,
            button_callback_arr: List[ButtonCallback] = None,

    ):
        self.callback = callback
        self.dof_callback = dof_callback
        self.dof_callback_arr = dof_callback_arr
        self.button_callback = button_callback
        self.button_callback_arr = button_callback_arr


class DeviceSpec(object):
    """Holds the specification of a single 3Dconnexion device"""

    def __init__(
            self, name, hid_id, led_id, mappings, button_mapping, axis_scale=350.0
    ):
        self.version_number = None
        self.serial_number = None
        self.vendor_name: Union[None, str] = None
        self.product_name: Union[None, str] = None
        self.name = name
        self.hid_id = hid_id
        self.led_id = led_id
        self.__mappings = mappings
        self.button_mapping = button_mapping
        self.axis_scale = axis_scale
        self.__bytes_to_read = self.__get_num_bytes_to_read()

        # self.led_usage = hid.get_full_usage_id(led_id[0], led_id[1])
        # initialise to a vector of 0s for each state
        self.dict_state: dict[str, Union[int, float, ButtonState]] = {
            "t": -1,
            "x": 0,
            "y": 0,
            "z": 0,
            "roll": 0,
            "pitch": 0,
            "yaw": 0,
            "buttons": ButtonState([0] * len(self.button_mapping)),
        }
        # initialise to a vector for button_callback_arr timer
        self.dict_state_last = {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0,
            "roll": 0.0,
            "pitch": 0.0,
            "yaw": 0.0,
        }
        self.tuple_state = SpaceNavigator(**self.dict_state)

        # start in disconnected state
        self.device = None
        self.callback = None
        self.dof_callback = None
        self.dof_callback_arr = None
        self.button_callback = None
        self.button_callback_arr: Union[None, List[ButtonCallback]] = None
        self.set_nonblocking_loop = True


    def __enter__(self):
        """Open the device"""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the device"""
        self.close()


    def __get_num_bytes_to_read(self):
        byte_indices = []
        for value in self.__mappings.values():
            byte_indices.extend([value.byte1, value.byte2])

        return max(byte_indices) + 1

    def describe_connection(self):
        """Return string representation of the device, including
        the connection state"""
        if self.device is None:
            return f"{self.name} [disconnected]"
        else:
            return f"{self.name} connected to {self.vendor_name} {self.product_name} version: {self.version_number} [serial: {self.serial_number}]"

    @property
    def mappings(self):
        return self.__mappings

    @mappings.setter
    def mappings(self, val):
        self.__mappings = val
        self.__bytes_to_read = self.__get_num_bytes_to_read()

    @property
    def connected(self):
        """True if the device has been connected"""
        return self.device is not None

    @property
    def state(self):
        """Return the current value of read()

        Returns: state: {t,x,y,z,pitch,yaw,roll,button} namedtuple
                None if the device is not open.
        """
        return self.read()

    def open(self):
        """Open a connection to the device, if possible"""
        if self.device:
            try:
                self.device.open()
            except HIDException as e:
                raise Exception("Failed to open device") from e

        # copy in product details
        self.product_name = self.device.product_string
        self.vendor_name = self.device.manufacturer_string
        self.version_number = self.device.release_number
        # doesn't seem to work on 3dconnexion devices...
        # serial number will be a byte string, we convert to a hex id
        self.serial_number = "".join(
            ["%02X" % ord(char) for char in self.device.serial_number]
        )

    # def set_led(self, state):
    #     """Set the LED state to state (True or False)"""
    #     if self.connected:
    #         reports = self.device.find_output_reports()
    #         for report in reports:
    #             if self.led_usage in report:
    #                 report[self.led_usage] = state
    #                 report.send()

    def close(self):
        """Close the connection, if it is open"""
        if self.connected:
            self.device.close()
            self.device = None

    def read(self):
        """Read data from SpaceMouse and return the current state of this navigation controller.

        Returns:
            state: {t,x,y,z,pitch,yaw,roll,button} namedtuple
            None if the device is not open.
        """
        if not self.connected:
            return None
        # read bytes from SpaceMouse
        ret = self.device.read(self.__bytes_to_read)
        # test for nonblocking read
        if (ret):
            self.process(ret)
        return self.tuple_state

    def process(self, data):
        """
        Update the state based on the incoming data

        This function updates the state of the DeviceSpec object, giving values for each
        axis [x,y,z,roll,pitch,yaw] in range [-1.0, 1.0]
        The state tuple is only set when all 6 DoF have been read correctly.

        The timestamp (in fractional seconds since the start of the program)  is written as element "t"

        If callback is provided, it is called only on DoF state changes with a copy of the current state tuple.
        If dof_callback is provided, it is called only on DOF state changes with the argument (state).
        If dof_callback_arr is provided, it is called only on DOF state changes with the argument (state, axis).
        If button_callback is provided, it is called only on button state changes with the argument (state, buttons).
        If button_callbacks_arr is provided, it is called only on specific button state true with the argument (state, buttons, pressed_buttons).

        Parameters:
            data    The data for this HID event, as returned by the HID callback

        """
        button_changed = False
        dof_changed = False

        for name, (chan, b1, b2, flip) in self.__mappings.items():
            if data[0] == chan:
                dof_changed = True
                # check if b1 or b2 is over the length of the data
                if b1 < len(data) and b2 < len(data):
                    self.dict_state[name] = (
                            flip * self.__to_int16(data[b1], data[b2]) / float(self.axis_scale)
                    )

        for button_index, (chan, byte, bit) in enumerate(self.button_mapping):
            if data[0] == chan:
                button_changed = True
                # update the button vector
                mask = 1 << bit
                self.dict_state["buttons"][button_index] = (
                    1 if (data[byte] & mask) != 0 else 0
                )

        self.dict_state["t"] = high_acc_clock()

        # must receive both parts of the 6DOF state before we return the state dictionary
        if len(self.dict_state) == 8:
            self.tuple_state = SpaceNavigator(**self.dict_state)

        # call any attached callbacks
        if self.callback:
            self.callback(self.tuple_state)

        # only call the DOF callback if the DOF state actually changed
        if self.dof_callback and dof_changed:
            self.dof_callback(self.tuple_state)

        # only call the DoF callback_arr if the specific DoF state actually changed
        if self.dof_callback_arr and dof_changed:
            # foreach all callbacks (ButtonCallback)
            for block_dof_callback in self.dof_callback_arr:
                now = high_acc_clock()
                axis_name = block_dof_callback.axis
                if now >= self.dict_state_last[axis_name] + block_dof_callback.sleep:
                    axis_val = self.dict_state[axis_name]
                    # is minus callback defined
                    if block_dof_callback.callback_minus:
                        # is axis value greater than filter
                        if axis_val > block_dof_callback.filter:
                            block_dof_callback.callback(self.tuple_state, axis_val)
                        elif axis_val < -block_dof_callback.filter:
                            block_dof_callback.callback_minus(self.tuple_state, axis_val)
                    elif axis_val > block_dof_callback.filter or axis_val < -block_dof_callback.filter:
                        block_dof_callback.cafllback(self.tuple_state, axis_val)
                    self.dict_state_last[axis_name] = now

        # only call the button callback if the button state actually changed
        if self.button_callback and button_changed:
            self.button_callback(self.tuple_state, self.tuple_state.buttons)

        # only call the button callback_arr if the specific button state actually changed
        if self.button_callback_arr and button_changed:
            # foreach all callbacks (ButtonCallback)
            for block_button_callback in self.button_callback_arr:
                run = True
                # are buttons list
                if type(block_button_callback.buttons) is list:
                    for button_id in block_button_callback.buttons:
                        if not self.tuple_state.buttons[button_id]:
                            run = False

                # is one button
                elif isinstance(block_button_callback.buttons, int):
                    if not self.tuple_state.buttons[block_button_callback.buttons]:
                        run = False
                # call callback
                if run:
                    block_button_callback.callback(self.tuple_state, self.tuple_state.buttons,
                                                   block_button_callback.buttons)

    # def config_set(self, config: Config):
    #     """Set new configuration of mouse from Config class"""
    #
    #     self.callback = config.callback
    #     self.dof_callback = config.dof_callback
    #     self.dof_callback_arr = config.dof_callback_arr
    #     self.button_callback = config.button_callback
    #     self.button_callback_arr = config.button_callback_arr

    def config_set_sep(self, callback=None, dof_callback=None, dof_callback_arr=None, button_callback=None,
                       button_callback_arr=None):
        """Set new configuration of mouse and check that the configuration has correct parts"""

        check_config(callback, dof_callback, dof_callback_arr, button_callback, button_callback_arr)

        self.callback = callback
        self.dof_callback = dof_callback
        self.dof_callback_arr = dof_callback_arr
        self.button_callback = button_callback
        self.button_callback_arr = button_callback_arr

    # def config_remove(self):
    #     """Remove old configuration"""
    #
    #     self.callback = None
    #     self.dof_callback = None
    #     self.dof_callback_arr = None
    #     self.button_callback = None
    #     self.button_callback_arr = None

    # convert two 8 bit bytes to a signed 16-bit integer
    def __to_int16(self, y1, y2):
        x = (y1) | (y2 << 8)
        if x >= 32768:
            x = -(65536 - x)
        return x

# the IDs for the supported devices
# Each ID maps a device name to a DeviceSpec object

# [For the SpaceNavigator]
# The HID data is in the format
# [id, a, b, c, d, e, f]
# each pair (a,b), (c,d), (e,f) is a 16 bit signed value representing the absolute device state [from -350 to 350]

# if id==1, then the mapping is
# (a,b) = y translation
# (c,d) = x translation
# (e,f) = z translation

# if id==2 then the mapping is
# (a,b) = x tilting (roll)
# (c,d) = y tilting (pitch)
# (d,e) = z tilting (yaw)

# if id==3 then the mapping is
# a = button. Bit 1 = button 1, bit 2 = button 2

# Each movement of the device always causes two HID events, one
# with id 1 and one with id 2, to be generated, one after the other.
