import pyspacemouse
import time
import pyautogui

pyautogui.PAUSE = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.MINIMUM_DURATION = 0

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
        pyspacemouse.DofCallback("x", lambda axis: print("x:",axis), 0.05),
        # pyspacemouse.DofCallback("pitch", lambda axis: pyautogui.scroll((axis*2)**3), 0.08),
        pyspacemouse.DofCallback("pitch", lambda axis: pyautogui.scroll((axis*5)), 0.09),
        # pyspacemouse.ButtonCallback([1], call2),
    ]
    dev = pyspacemouse.open(dof_callback_arr=arr_success)
    while True:
        state = dev.read()
        time.sleep(0.0001)


def success_dof_callback_cfg():
    test("Move X axis")
    arr_success = [
        pyspacemouse.DofCallback("x", lambda axis: print("x:",axis), 0.05),
        # pyspacemouse.DofCallback("pitch", lambda axis: pyautogui.scroll((axis*2)**3), 0.08),
        pyspacemouse.DofCallback("pitch", lambda axis: pyautogui.scroll((axis*5)), 0.09),
        # pyspacemouse.ButtonCallback([1], call2),
    ]

    cfg = pyspacemouse.Config(dof_callback_arr=arr_success)

    dev = pyspacemouse.openCfg(cfg)
    while True:
        state = dev.read()
        time.sleep(0.0001)


def success_dof_callback_set():
    test("Move X axis")
    arr_success = [
        pyspacemouse.DofCallback("x", lambda axis: print("x:",axis), 0.05),
        # pyspacemouse.DofCallback("pitch", lambda axis: pyautogui.scroll((axis*2)**3), 0.08),
        pyspacemouse.DofCallback("pitch", lambda axis: pyautogui.scroll((axis*5)), 0.09),
        # pyspacemouse.ButtonCallback([1], call2),
    ]

    cfg = pyspacemouse.Config(dof_callback_arr=arr_success)

    dev = pyspacemouse.open()
    dev.config_set(cfg)
    # dev.config_remove()
    while True:
        state = dev.read()
        time.sleep(0.0001)


def success_dof_callback_set_p():
    test("Move X axis")
    arr_success = [
        pyspacemouse.DofCallback("x", lambda state, axis: print("x:",axis), 0.05),
        # pyspacemouse.DofCallback("pitch", lambda state, axis: pyautogui.scroll((axis*2)**3), 0.08),
        pyspacemouse.DofCallback("pitch", lambda state, axis: pyautogui.scroll((axis*5)), 0.09),
        # pyspacemouse.ButtonCallback([1], call2),
    ]

    cfg = pyspacemouse.Config(dof_callback_arr=arr_success)

    pyspacemouse.open()
    pyspacemouse.config_set(cfg)
    # pyspacemouse.config_remove()
    while True:
        state = pyspacemouse.read()
        time.sleep(0.0001)

def mouse(state, axis):
    val = axis*4
    if axis > 0.0:
        # pyautogui.hotkey("up")
        for x in range(0, int(val)):
            pyautogui.press("up")
    elif axis < -0.0:
        for y in range(0, int(-val)):
            pyautogui.press("down")

def mouse_side(state, axis):
    val = axis*2
    print(val)
    if axis > 0.0:
        # pyautogui.hotkey("up")
        for x in range(1, int(val**3)):
            pyautogui.press("right")
    elif axis < -0.0:
        for y in range(1, int(-val**3)):
            pyautogui.press("left")

def success_dof_callback_set_mouse():
    test("Move X axis")
    arr_success = [
        # pyspacemouse.DofCallback("x", lambda state, axis: print("x:",axis), 0.05),
        # pyspacemouse.DofCallback("pitch", lambda state, axis: pyautogui.scroll((axis*2)**3), 0.08),
        pyspacemouse.DofCallback("pitch", mouse, 0.2),
        pyspacemouse.DofCallback("roll", mouse_side, 0.1),
        # pyspacemouse.DofCallback("yaw", mouse_side, 0.1),
        # pyspacemouse.ButtonCallback([1], call2),
    ]

    cfg = pyspacemouse.Config(dof_callback_arr=arr_success)

    pyspacemouse.open()
    pyspacemouse.config_set(cfg)
    # pyspacemouse.config_remove()
    while True:
        state = pyspacemouse.read()
        time.sleep(0.0001)

if __name__ == '__main__':
    print("Start testing")
    # success()
    # err_arr_arr_string() #y
    # err_arr_num_string()
    # err_obj_arr_string() #y
    # err_obj_num_string()
    # success_dof_callback()


    # success_dof_callback_set()
    # success_dof_callback_set_p()
    success_dof_callback_set_mouse()