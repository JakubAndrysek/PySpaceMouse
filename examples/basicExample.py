import pyspacemouse
import time

if success := pyspacemouse.open():
    while 1:
        state = pyspacemouse.read()
        print(state.x, state.y, state.z)
        time.sleep(0.01)