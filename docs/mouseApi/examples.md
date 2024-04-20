# Examples


## Basic usage
[basicExample.py](https://github.com/JakubAndrysek/PySpaceMouse/blob/master/examples/basicExample.py)
````py
import pyspacemouse
import time

success = pyspacemouse.open()
if success:
    while 1:
        state = pyspacemouse.read()
        print(state.x, state.y, state.z)
        time.sleep(0.01)
````


## Usage with callback
[callbackExample.py](https://github.com/JakubAndrysek/PySpaceMouse/blob/master/examples/callbackExample.py)
````py
import pyspacemouse
import time


def button_0(state, buttons, pressed_buttons):
    print("Button:", pressed_buttons)


def button_0_1(state, buttons, pressed_buttons):
    print("Buttons:", pressed_buttons)


def someButton(state, buttons):
    print("Some button")


def callback():
    button_arr = [pyspacemouse.ButtonCallback(0, button_0),
                  pyspacemouse.ButtonCallback([1], lambda state, buttons, pressed_buttons: print("Button: 1")),
                  pyspacemouse.ButtonCallback([0, 1], button_0_1), ]

    success = pyspacemouse.open(dof_callback=pyspacemouse.print_state, button_callback=someButton,
                                button_callback_arr=button_arr)
    if success:
        while True:
            pyspacemouse.read()
            time.sleep(0.01)


if __name__ == '__main__':
    callback()
````


### Callback: print_state

Print all axis states

    x +0.00    y +0.00    z +0.00 roll +0.00 pitch +0.00  yaw +0.00    t +0.0

### Callback: print_buttons

Print all buttons states

    [ 0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, ]