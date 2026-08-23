"""hidapi binding selection.

pyspacemouse talks to devices through the `hidapi` package (cython-hidapi),
which compiles the hidapi C library into its wheels. That means there is no
system library to install and no dynamic-linker search path to configure on any
platform.

On Linux the package ships two modules built against different backends:

- ``hidraw`` - the kernel hidraw backend. Devices are reported as ``/dev/hidrawN``
  paths and permissions are granted by the udev rules in the README.
- ``hid`` - the libusb backend. Devices are reported as bus addresses and the
  kernel driver has to be detached first.

We prefer ``hidraw`` there so that device paths stay stable and the documented
udev rules keep working. macOS and Windows wheels only ship ``hid``.
"""

from __future__ import annotations

import sys
from typing import Any, Optional

_INSTALL_HINT = (
    "Install it with `pip install hidapi`. Note that `hidapi` (cython-hidapi) is "
    "a different package from `hid` (pyhidapi) even though both provide a module "
    "named `hid`; if `hid` is installed it will shadow this one and must be "
    "uninstalled. See https://spacemouse.kubaandrysek.cz for details."
)

_module: Optional[Any] = None


def get_hid() -> Any:
    """Return the hidapi binding module, importing it on first use.

    The import is deferred so that the hardware-free parts of pyspacemouse
    (types, config helpers, device specs) stay usable without the binding.

    Raises:
        ImportError: If the `hidapi` package is missing, or if a different
            package is providing the `hid` module name.
    """
    global _module
    if _module is None:
        _module = _import_hid()
    return _module


def _import_hid() -> Any:
    module = None

    if sys.platform.startswith("linux"):
        try:
            import hidraw

            module = hidraw
        except ImportError:
            # Older cython-hidapi releases, and source builds configured with
            # --with-libusb, only provide `hid`.
            module = None

    if module is None:
        try:
            import hid

            module = hid
        except ImportError as e:
            raise ImportError(f"pyspacemouse requires the `hidapi` package. {_INSTALL_HINT}") from e

    # cython-hidapi exposes the `device` class; pyhidapi exposes `Device` and no
    # `device`, so this tells the two apart and gives a message that names the
    # actual problem instead of failing later with an AttributeError.
    if not hasattr(module, "device"):
        raise ImportError(
            f"The `hid` module at {getattr(module, '__file__', '<unknown>')} is not from "
            f"cython-hidapi. {_INSTALL_HINT}"
        )

    return module
