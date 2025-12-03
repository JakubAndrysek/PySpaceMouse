from .pyspacemouse import *

# Version handling for dynamic versioning with hatch-vcs
try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    # Python < 3.8 fallback
    from importlib_metadata import PackageNotFoundError, version  # type: ignore

try:
    __version__ = version("pyspacemouse")
except PackageNotFoundError:
    # Package is not installed
    __version__ = "0.0.0.dev0"
