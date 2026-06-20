"""Provide reusable button helpers for Raspberry Pi GPIO pins.

This module is part of the rpilib library. It provides helper functions for
creating and using buttons connected to Raspberry Pi GPIO pins.

The functions in this file use gpiozero.Button. The gpiozero library handles
much of the GPIO setup and cleanup for us while still letting students work
directly with GPIO pin numbers and button events.

A button event is an action that happens when the button changes state. For
example, a program can call one function when the button is pressed and another
function when the button is released.

Example:
    from rpilib.gpio.buttons import create_button, is_pressed

    button = create_button(pin=24)

    if is_pressed(button):
        print("Button is pressed.")

Future improvements:
    - Add support for long-press and double-press button patterns.
    - Add support for grouping several buttons into one controller object.
"""

from collections.abc import Callable
from typing import Final

from gpiozero import Button

from rpilib.config import DEFAULT_GREEN_BUTTON_PIN


# ---------------------------------------------------------------------------
# Button defaults
# ---------------------------------------------------------------------------
# The default button pin comes from rpilib.config so the common course wiring
# value is stored in one place. Student programs can still pass a different pin
# when their circuit uses different wiring.
DEFAULT_BUTTON_PIN: Final[int] = DEFAULT_GREEN_BUTTON_PIN

# Bounce time helps prevent one physical button press from being read as many
# presses. Mechanical buttons can briefly "bounce" between on and off as the
# contacts settle.
DEFAULT_BOUNCE_SECONDS: Final[float] = 0.05

# Hold time is how long the button must stay pressed before gpiozero treats it
# as a held button.
DEFAULT_HOLD_SECONDS: Final[float] = 1.0

# This alias describes the type of a simple callback function. A callback is a
# function that another object calls later when an event happens.
ButtonCallback = Callable[[], None]


def create_button(
    pin: int = DEFAULT_BUTTON_PIN,
    bounce_seconds: float = DEFAULT_BOUNCE_SECONDS,
    hold_seconds: float = DEFAULT_HOLD_SECONDS,
    pull_up: bool = True,
) -> Button:
    """Create and return a Button object for one GPIO pin.

    Args:
        pin: Broadcom GPIO pin number connected to the button.
        bounce_seconds: Number of seconds used to filter switch bounce.
        hold_seconds: Number of seconds the button must be pressed before it is
            considered held.
        pull_up: If True, use the Raspberry Pi internal pull-up resistor.

    Returns:
        A gpiozero Button object that can detect button input and events.

    Raises:
        ValueError: If bounce_seconds or hold_seconds is less than zero.
    """
    button_pin: int = pin
    button_bounce_seconds: float = bounce_seconds
    button_hold_seconds: float = hold_seconds
    button_pull_up: bool = pull_up
    button: Button

    if button_bounce_seconds < 0:
        raise ValueError("Button bounce time must be zero or greater.")

    if button_hold_seconds < 0:
        raise ValueError("Button hold time must be zero or greater.")

    # GPIO pin numbers in this library use Broadcom GPIO numbering. This is the
    # same numbering style used by gpiozero when an integer pin number is given.
    button = Button(
        button_pin,
        pull_up=button_pull_up,
        bounce_time=button_bounce_seconds,
        hold_time=button_hold_seconds,
    )

    return button


def is_pressed(button: Button) -> bool:
    """Check whether a button is currently pressed.

    Args:
        button: The gpiozero Button object to check.

    Returns:
        True if the button is currently pressed; otherwise, False.
    """
    target_button: Button = button
    pressed: bool = target_button.is_pressed

    return pressed


def wait_for_press(button: Button, timeout_seconds: float | None = None) -> bool:
    """Wait until a button is pressed or the optional timeout ends.

    This function pauses the program while it waits. That is called blocking.
    Blocking is simple and useful in small programs, but event callbacks are
    often better for programs that need to do several things at once.

    Args:
        button: The gpiozero Button object to wait on.
        timeout_seconds: Maximum number of seconds to wait. Use None to wait
            forever.

    Returns:
        True if the button was pressed before the timeout; otherwise, False.

    Raises:
        ValueError: If timeout_seconds is less than zero.
    """
    target_button: Button = button
    wait_timeout_seconds: float | None = timeout_seconds
    was_pressed: bool | None

    if wait_timeout_seconds is not None and wait_timeout_seconds < 0:
        raise ValueError("Button timeout must be zero or greater.")

    was_pressed = target_button.wait_for_press(timeout=wait_timeout_seconds)

    # gpiozero returns True when the button is pressed. It may return None if
    # the timeout ends first, so bool() converts that result into False.
    return bool(was_pressed)


def wait_for_release(button: Button, timeout_seconds: float | None = None) -> bool:
    """Wait until a button is released or the optional timeout ends.

    Args:
        button: The gpiozero Button object to wait on.
        timeout_seconds: Maximum number of seconds to wait. Use None to wait
            forever.

    Returns:
        True if the button was released before the timeout; otherwise, False.

    Raises:
        ValueError: If timeout_seconds is less than zero.
    """
    target_button: Button = button
    wait_timeout_seconds: float | None = timeout_seconds
    was_released: bool | None

    if wait_timeout_seconds is not None and wait_timeout_seconds < 0:
        raise ValueError("Button timeout must be zero or greater.")

    was_released = target_button.wait_for_release(timeout=wait_timeout_seconds)

    return bool(was_released)


def set_press_callback(button: Button, callback: ButtonCallback) -> None:
    """Run a callback function when a button is pressed.

    Args:
        button: The gpiozero Button object to configure.
        callback: Function to call when the button is pressed.
    """
    target_button: Button = button
    press_callback: ButtonCallback = callback

    target_button.when_pressed = press_callback


def set_release_callback(button: Button, callback: ButtonCallback) -> None:
    """Run a callback function when a button is released.

    Args:
        button: The gpiozero Button object to configure.
        callback: Function to call when the button is released.
    """
    target_button: Button = button
    release_callback: ButtonCallback = callback

    target_button.when_released = release_callback


def set_hold_callback(button: Button, callback: ButtonCallback) -> None:
    """Run a callback function when a button is held.

    The hold time is set when the button is created.

    Args:
        button: The gpiozero Button object to configure.
        callback: Function to call when the button is held.
    """
    target_button: Button = button
    hold_callback: ButtonCallback = callback

    target_button.when_held = hold_callback


def clear_callbacks(button: Button) -> None:
    """Remove all callback functions from a button.

    This is useful when a program needs to stop responding to old button events
    before assigning new behavior.

    Args:
        button: The gpiozero Button object to update.
    """
    target_button: Button = button

    target_button.when_pressed = None
    target_button.when_released = None
    target_button.when_held = None


def close_button(button: Button) -> None:
    """Release the GPIO resources used by a button.

    gpiozero usually handles cleanup when a program exits. This helper is still
    useful when a program creates and removes hardware objects while it is
    running.

    Args:
        button: The gpiozero Button object to close.
    """
    target_button: Button = button

    # Closing a gpiozero device releases the pin so another object or program
    # can use it later.
    target_button.close()


def main() -> None:
    """Run a short button demonstration when executed directly.

    The main function is not used when this module is imported into another
    program. It gives students and instructors a quick way to test the module
    on a Raspberry Pi with a button connected to the default pin.
    """
    demo_button: Button
    message: str = f"Testing button on GPIO {DEFAULT_BUTTON_PIN}"
    was_pressed: bool = False

    print(message)
    print("Press the button within 10 seconds.")

    demo_button = create_button()
    was_pressed = wait_for_press(demo_button, timeout_seconds=10.0)

    if was_pressed:
        print("Button press detected.")
    else:
        print("No button press detected.")

    close_button(demo_button)
    print("Button test complete.")


if __name__ == "__main__":
    main()


# AI acknowledgement:
# Generative AI assistance was used to help draft, revise, or review this
# module. The author reviewed and tested the code and is responsible for the
# final version.
