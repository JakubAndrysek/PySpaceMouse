# import pyspacemouse
# import time
#
# success = pyspacemouse.open()
# if success:
#     while 1:
#         state = pyspacemouse.read()
#         print(state.x, state.y, state.z)
#         time.sleep(0.01)


# import pyspacemouse
# import time
#
#
# def button_0(state, buttons, pressed_buttons):
#     print("Button:", pressed_buttons)
#
#
# def button_0_1(state, buttons, pressed_buttons):
#     print("Buttons:", pressed_buttons)
#
#
# def someButton(state, buttons):
#     print("Some button")
#
#
# def callback():
#     button_arr = [
#         pyspacemouse.ButtonCallback(0, button_0),
#         pyspacemouse.ButtonCallback([1], lambda state, buttons, pressed_buttons: print("Button: 1")),
#         pyspacemouse.ButtonCallback([0, 1], button_0_1),
#     ]
#
#     success = pyspacemouse.open(dof_callback=pyspacemouse.print_state, button_callback=someButton,
#                                 button_callback_arr=button_arr)
#     if success:
#         while True:
#             pyspacemouse.read()
#             time.sleep(0.01)
#
#
# if __name__ == '__main__':
#     callback()


import pyspacemouse
import time

success = pyspacemouse.open(dof_callback=pyspacemouse.print_state, button_callback=pyspacemouse.print_buttons)
if success:
    while 1:
        state = pyspacemouse.read()
        time.sleep(0.01)

# import pyspacemouse
# import time
#
# cfg = pyspacemouse.Config(
#     dof_callback_arr=[
#         pyspacemouse.DofCallback("x", lambda state, buttons: print("Button: 0")),
#         pyspacemouse.DofCallback("y", lambda state, buttons: print("Button: 1")),
#     ],
#     button_callback_arr=[
#         pyspacemouse.ButtonCallback(1, lambda axis: print(f"DoF y: {axis}")),
#         pyspacemouse.ButtonCallback([5, 2, 1], lambda axis: print(f"DoF y: {axis}")),
#         pyspacemouse.ButtonCallback([5, 4], lambda axis, s: print(f"DoF y: {axis}")),
#     ]
# )
#
# dev = pyspacemouse.device_specs["SpaceMouse Pro"]
# dev.check_config_sep(cfg)
