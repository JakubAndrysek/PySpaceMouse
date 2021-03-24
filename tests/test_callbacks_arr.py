import pyspacemouse
import time

def test(info):
    print(f"Test: {info}")


def call1(state, buttons):
    print("Success-1")


def call2(state, buttons):
    print("Success-2")


def success():
    test("Press button 0 or 1")
    arr_success = [
        pyspacemouse.ButtonCallback([0], call1),
        pyspacemouse.ButtonCallback([1], call2),
    ]
    dev = pyspacemouse.open(button_callback_arr=arr_success)
    while True:
        state = dev.read()


def err_arr_arr_string():
    test("Press button 0 or 1")
    arr_success = [
        pyspacemouse.ButtonCallback(["1", "1.1"], call1),
        pyspacemouse.ButtonCallback(["2"], call2),
    ]
    dev = pyspacemouse.open(button_callback_arr=arr_success)
    while True:
        state = dev.read()


def err_arr_num_string():
    test("Press button 0 or 1")
    arr_success = [
        pyspacemouse.ButtonCallback("1", call1),
        pyspacemouse.ButtonCallback("2", call2),
    ]
    dev = pyspacemouse.open(button_callback_arr=arr_success)
    while True:
        state = dev.read()


def err_obj_arr_string():
    test("Press button 0 or 1")
    arr_success = pyspacemouse.ButtonCallback(["1"], call1)

    dev = pyspacemouse.open(button_callback_arr=arr_success)
    while True:
        state = dev.read()


def err_obj_num_string():
    test("Press button 0 or 1")
    arr_success = pyspacemouse.ButtonCallback("1", call1)

    dev = pyspacemouse.open(button_callback_arr=arr_success)
    while True:
        state = dev.read()

def success_dof_callback():
    test("Move X axis")
    arr_success = [
        pyspacemouse.DofCallback("x", lambda axis: print("x:",axis)),
        pyspacemouse.DofCallback("pitch", lambda axis: print("pitch:", axis)),
        # pyspacemouse.ButtonCallback([1], call2),
    ]
    dev = pyspacemouse.open(dof_callback_arr=arr_success)
    while True:
        state = dev.read()
        time.sleep(0.0001)


if __name__ == '__main__':
    print("Start testing")
    # success()
    # err_arr_arr_string() #y
    # err_arr_num_string()
    # err_obj_arr_string() #y
    # err_obj_num_string()
    success_dof_callback()