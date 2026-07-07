from __future__ import annotations

from pyspacemouse.config_helpers import apply_axis_convention
from pyspacemouse.types import AXIS_NAMES, AxisConvention, AxisSpec, DeviceInfo


def _hid_spec() -> DeviceInfo:
    mappings = {
        axis: AxisSpec(channel=index, byte1=index * 2, byte2=index * 2 + 1, scale=index + 1)
        for index, axis in enumerate(AXIS_NAMES, start=1)
    }
    return DeviceInfo(
        name="Test HID device",
        vendor_id=1,
        product_id=2,
        led_id=None,
        axis_scale=350.0,
        mappings=mappings,
        button_specs=(),
        button_names=(),
        convention=AxisConvention.HID,
    )


def test_each_axis_convention_round_trips_through_hid() -> None:
    hid_spec = _hid_spec()

    for convention in AxisConvention:
        converted = apply_axis_convention(hid_spec, convention)
        round_tripped = apply_axis_convention(converted, AxisConvention.HID)

        assert round_tripped.convention == AxisConvention.HID
        assert round_tripped.mappings == hid_spec.mappings


def test_axis_conventions_round_trip_between_non_hid_frames() -> None:
    hid_z_up_spec = apply_axis_convention(_hid_spec(), AxisConvention.HID_Z_UP)

    ros_spec = apply_axis_convention(hid_z_up_spec, AxisConvention.ROS)
    round_tripped = apply_axis_convention(ros_spec, AxisConvention.HID_Z_UP)

    assert round_tripped.convention == AxisConvention.HID_Z_UP
    assert round_tripped.mappings == hid_z_up_spec.mappings
