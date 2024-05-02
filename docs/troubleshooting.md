# Troubleshooting

If you encounter any issues, you can find help in the following section.

## Common issues

### ModuleNotFoundError: No module named 'easyhid'

- Install `easyhid` by `pip install easyhid`.

### AttributeError: function/symbol 'hid_enumerate' not found in library '<None>': python3: undefined symbol: hid_enumerate

- HID library for your computer is not installed.
- Follow the instructions in [requirements](./README.md#dependencies).

<hr>

## Mac OS (M1)

!!! info "External dependencies"
    You don't have to install original 3Dconnexion driver `3DxWare 10`. This library works directly with `hidapi` device interface.

If you are using a Mac with an M1 chip or newer, you may encounter issues when installing the dependencies.
Required dependency is `hidapi` which you can install using Homebrew `brew install hidapi`.

By  default, the `hidapi` library is installed in `/opt/homebrew/Cellar/hidapi/0.14.0/lib` directory, and you need to add it to your `DYLD_LIBRARY_PATH` environment variable.
It is possible to add it to your `.bashrc` or `.zshrc` file, but you can also add it directly in the terminal (only for the current session).

Replace `0.14.0` with the version you have installed on your system (`brew info hidapi`).
```bash
export DYLD_LIBRARY_PATH=/opt/homebrew/Cellar/hidapi/0.14.0/lib:$DYLD_LIBRARY_PATH
```

In case of changes in MacOS M1, architecture name, you have to use patched version of `easyhid` library.
Updated version is not yet available on PyPi, so you have to uninstall the current version and install the patched version from GitHub.
```bash
pip install git+https://github.com/bglopez/python-easyhid.git
```

After this setup everything works correctly directly on MacOS M1.
Tested on:

- MacBook Pro 14 (M1 Pro, 2021)
- ??? (add your device and feedback)

I have probably tested it also in Rosetta 2 mode, but right now it works directly on M1 chip with python from `brew`.

<hr>

## Testing Hidapi

If you are not sure if `hidapi` is installed correctly, you can test it with the console tool [hidapitester](https://github.com/todbot/hidapitester).
This tool provides a simple interface to test the communication with HID devices.
On GitHub, you can find the source code and precompiled binaries for Windows, Linux, and Mac OS.

Just download the binary for your system and run it in the terminal.

List connected devices:
```bash
./hidapitester --list
```
??? note "My output"
    ```bash
    046D/C626: 3Dconnexion - SpaceNavigator
    045E/07A5: Microsoft - Microsoft 2.4GHz Transceiver v9.0
    ...
    ```
Read data from the device (replace `<VID/PID>` with the VID/PID of your device):
```bash
./hidapitester --vidpid <VID/PID> --open --read-input
```

??? note "My output"
    ```bash
    ./hidapitester --vidpid 046D/C626 --open --read-input
    Opening device, vid/pid: 0x046D/0xC626
    Reading 64-byte input report 0, 250 msec timeout...read 7 bytes:
    01 76 00 00 00 FA FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    Closing device
    ```

Read descriptor from the device (replace `<VID/PID>` with the VID/PID of your device):
```bash
./hidapitester --vidpid <VID/PID> --open --get-report-descriptor
```

??? note "My output"
    ```bash
    ./hidapitester --vidpid 046D/C626 --open --get-report-descriptor
    Opening device, vid/pid: 0x046D/0xC626
    Report Descriptor:
    05 01 09 08 A1 01 A1 00 85 01 16 A2 FE 26 5E 01 36 88 FA 46 78 05 55 0C 65 11 09 30 09 31 09 32
    75 10 95 03 81 06 C0 A1 00 85 02 09 33 09 34 09 35 75 10 95 03 81 06 C0 A1 02 85 03 05 01 05 09
    ...
    Closing device
    ```

## Windows

!!! info "Error message - OSError: cannot load library 'hidapi.dll'"
    ```bash
    Traceback (most recent call last):
    File "C:\Users\Student\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\easyhid\easyhid.py", line 53, in <module>
        hidapi = ffi.dlopen('hidapi.dll')
    File "C:\Users\Student\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\cffi\api.py", line 150, in dlopen
        lib, function_cache = _make_ffi_library(self, name, flags)
    File "C:\Users\Student\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\cffi\api.py", line 832, in _make_ffi_library
        backendlib = _load_backend_lib(backend, libname, flags)
    File "C:\Users\Student\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\cffi\api.py", line 827, in _load_backend_lib
        raise OSError(msg)
    OSError: cannot load library 'hidapi.dll': error 0x7e.  Additionally, ctypes.util.find_library() did not manage to locate a library called 'hidapi.dll
    ```

??? info "Other error message - OSError: dlopen(None) cannot work on Windows for Python 3"
    ```bash
    File "C:\Users\Student\Downloads\basicExample.py", line 1, in <module>
        import pyspacemouse
    File "C:\Users\Student\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\pyspacemouse\__init__.py", line 1, in <module>
        from .pyspacemouse import *
    File "C:\Users\Student\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\pyspacemouse\pyspacemouse.py", line 1, in <module>
        from easyhid import Enumeration, HIDException
    File "C:\Users\Student\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\easyhid\__init__.py", line 8, in <module>
        from easyhid.easyhid import *
    File "C:\Users\Student\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\easyhid\easyhid.py", line 55, in <module>
        hidapi = ffi.dlopen(ctypes.util.find_library('hidapi.dll'))
    File "C:\Users\Student\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\cffi\api.py", line 150, in dlopen
        lib, function_cache = _make_ffi_library(self, name, flags)
    File "C:\Users\Student\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\cffi\api.py", line 832, in _make_ffi_library
        backendlib = _load_backend_lib(backend, libname, flags)
    File "C:\Users\Student\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\cffi\api.py", line 821, in _load_backend_lib
        raise OSError("dlopen(None) cannot work on Windows for Python 3 "
    OSError: dlopen(None) cannot work on Windows for Python 3 (see http://bugs.python.org/issue23606)
    ```


If you are using Windows, you may encounter issues with the `hidapi` library.
The library is not included in the system, so you have to install it manually.

Go to [hidapi GitHub](https://github.com/libusb/hidapi/releases/latest) and download the latest version of the library in zip format.
Extract the zip file and copy the x64/x86 folder with `hidapi.dll` to the static location where will be found by the system.

To make it work, you have to add the folder to the system `PATH` variable.

Go to Windows settings and search for `enviroment`.
![image](https://github.com/JakubAndrysek/PySpaceMouse/assets/33494544/ce7ba2b3-8e40-48bb-8348-5a1f932146c3)

Click on the `Environment variables`.
![image](https://github.com/JakubAndrysek/PySpaceMouse/assets/33494544/ce22bae7-a0c8-4f19-9204-7f1a12f28782)

Append the path to the folder with `hidapi.dll` to the `Path` variable.
![image](https://github.com/JakubAndrysek/PySpaceMouse/assets/33494544/0ddefada-b595-49f3-bf0f-d11567cf887f)

After this setup, you have to restart (maybe log out) your computer to apply the changes.
Let's start using this library in your Python code.
