"""Utility functions for PySpaceMouse.

This module contains helper functions for debugging and common operations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .types import SpaceMouseState


def print_state(state: SpaceMouseState) -> None:
    """Print all axis values to stdout.

    Args:
        state: Current SpaceMouse state
    """
    if state:
        parts = [
            f"{axis:>4s} {getattr(state, axis):+.2f}"
            for axis in ("x", "y", "z", "roll", "pitch", "yaw", "t")
        ]
        print(" ".join(parts))


def print_buttons(state: SpaceMouseState, buttons: List[int]) -> None:
    """Print all button states to stdout.

    Args:
        state: Current SpaceMouse state
        buttons: List of button states
    """
    formatted = " ".join(f"{b:2d}," for b in buttons)
    print(f"[{formatted}]")


def silent_callback(state: SpaceMouseState) -> None:
    """Do-nothing callback for suppressing output.

    Args:
        state: Current SpaceMouse state (ignored)
    """
    pass
