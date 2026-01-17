"""Callback types and configuration for PySpaceMouse.

This module contains callback definitions and configuration classes
for handling SpaceMouse events.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, List, Optional, Sequence, Union

if TYPE_CHECKING:
    from .types import SpaceMouseState

# Type aliases for callback signatures
StateCallback = Callable[["SpaceMouseState"], None]
ButtonChangeCallback = Callable[["SpaceMouseState", List[int]], None]
ButtonPressCallback = Callable[["SpaceMouseState", List[int], Union[int, List[int]]], None]
DofValueCallback = Callable[["SpaceMouseState", float], None]


@dataclass(slots=True)
class ButtonCallback:
    """Callback triggered when specific button(s) are pressed.

    Attributes:
        buttons: Single button index or list of button indices to watch
        callback: Function called with (state, buttons, pressed_buttons)
    """

    buttons: Union[int, List[int]]
    callback: ButtonPressCallback

    def __post_init__(self) -> None:
        """Validate the callback configuration."""
        if not callable(self.callback):
            raise TypeError("callback must be callable")
        if isinstance(self.buttons, list):
            if not all(isinstance(b, int) for b in self.buttons):
                raise TypeError("buttons must be int or list of int")
        elif not isinstance(self.buttons, int):
            raise TypeError("buttons must be int or list of int")


@dataclass(slots=True)
class DofCallback:
    """Callback triggered when a specific axis changes.

    Attributes:
        axis: Name of axis to monitor ('x', 'y', 'z', 'roll', 'pitch', 'yaw')
        callback: Function called with (state, axis_value) for positive values
        sleep: Minimum time between callback invocations
        callback_minus: Optional function for negative axis values
        filter: Minimum absolute value to trigger callback (deadzone)
    """

    axis: str
    callback: DofValueCallback
    sleep: float = 0.0
    callback_minus: Optional[DofValueCallback] = None
    filter: float = 0.0

    def __post_init__(self) -> None:
        """Validate the callback configuration."""
        valid_axes = ("x", "y", "z", "roll", "pitch", "yaw")
        if self.axis not in valid_axes:
            raise ValueError(f"axis must be one of {valid_axes}, got '{self.axis}'")
        if not callable(self.callback):
            raise TypeError("callback must be callable")
        if self.callback_minus is not None and not callable(self.callback_minus):
            raise TypeError("callback_minus must be callable or None")


@dataclass(slots=True)
class Config:
    """Configuration container for all callback types.

    Attributes:
        callback: Called on every state change
        dof_callback: Called on DoF (axis) state changes
        dof_callbacks: List of axis-specific callbacks
        button_callback: Called on any button state change
        button_callbacks: List of button-specific callbacks
    """

    callback: Optional[StateCallback] = None
    dof_callback: Optional[StateCallback] = None
    dof_callbacks: Optional[Sequence[DofCallback]] = None
    button_callback: Optional[ButtonChangeCallback] = None
    button_callbacks: Optional[Sequence[ButtonCallback]] = None

    def __post_init__(self) -> None:
        """Validate the configuration."""
        if self.dof_callbacks:
            for i, dc in enumerate(self.dof_callbacks):
                if not isinstance(dc, DofCallback):
                    raise TypeError(f"dof_callbacks[{i}] must be DofCallback instance")
        if self.button_callbacks:
            for i, bc in enumerate(self.button_callbacks):
                if not isinstance(bc, ButtonCallback):
                    raise TypeError(f"button_callbacks[{i}] must be ButtonCallback instance")

    # Legacy property names for backward compatibility
    @property
    def dof_callback_arr(self) -> Optional[Sequence[DofCallback]]:
        """Legacy alias for dof_callbacks."""
        return self.dof_callbacks

    @property
    def button_callback_arr(self) -> Optional[Sequence[ButtonCallback]]:
        """Legacy alias for button_callbacks."""
        return self.button_callbacks
