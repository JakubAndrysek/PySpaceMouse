import pyspacemouse
import time

# success = pyspacemouse.open()

with pyspacemouse.open() as device:
    print(device)
    while 1:
        state = device.read()
        print(state.x, state.y, state.z)
        time.sleep(0.01)