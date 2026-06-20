"""Provide shared timing values and timing helpers for rpilib.

This module is part of the rpilib library. It stores common timing values
used by Raspberry Pi projects, such as loop delays, sensor read intervals,
display refresh intervals, and Morse code timing.

The helper functions in this module make timing code easier to read. They
also give students one consistent place to learn how time-based delays are
handled in Python.

Example:
    from rpilib.timing import pause, MORSE_DOT_SECONDS

    pause(MORSE_DOT_SECONDS)

Future improvements:
    - Add non-blocking timing helpers for programs that should avoid sleep().
    - Add timer classes for more advanced event-driven programs.
"""

from time import monotonic, sleep
from typing import Final


# ---------------------------------------------------------------------------
# General timing defaults
# ---------------------------------------------------------------------------
# A timing value is stored in seconds unless the constant name says otherwise.
# For example, 0.5 means one-half second, and 1.0 means one full second.

DEFAULT_LOOP_SLEEP_SECONDS: Final[float] = 1.0
DEFAULT_DISPLAY_REFRESH_SECONDS: Final[float] = 1.0
DEFAULT_SENSOR_READ_SECONDS: Final[float] = 5.0
DEFAULT_SERIAL_UPDATE_SECONDS: Final[float] = 30.0


# ---------------------------------------------------------------------------
# Morse code timing defaults
# ---------------------------------------------------------------------------
# These constants support LED-based Morse code examples. The names describe
# the purpose of each pause so the calling program is easier to understand.

MORSE_DOT_SECONDS: Final[float] = 0.5
MORSE_DASH_SECONDS: Final[float] = 1.5
MORSE_SYMBOL_PAUSE_SECONDS: Final[float] = 0.25
MORSE_LETTER_PAUSE_SECONDS: Final[float] = 0.75
MORSE_WORD_PAUSE_SECONDS: Final[float] = 3.0


# ---------------------------------------------------------------------------
# Validation constants
# ---------------------------------------------------------------------------
# These values help us catch timing mistakes before they cause confusing
# hardware behavior. A negative sleep value does not make sense.
MIN_SECONDS: Final[float] = 0.0


def pause(seconds: float) -> None:
    """Pause the program for a specific number of seconds.

    This function wraps time.sleep() so rpilib modules and student programs
    can use one consistent helper for simple delays.

    Args:
        seconds: Number of seconds to pause. This value must be zero or greater.

    Raises:
        ValueError: If seconds is less than zero.
    """
    delay_seconds: float = seconds

    if delay_seconds < MIN_SECONDS:
        raise ValueError("Pause duration must be zero or greater.")

    sleep(delay_seconds)


def pause_milliseconds(milliseconds: int) -> None:
    """Pause the program for a specific number of milliseconds.

    A millisecond is one-thousandth of a second. For example, 500 milliseconds
    is the same as 0.5 seconds.

    Args:
        milliseconds: Number of milliseconds to pause. This value must be zero
            or greater.

    Raises:
        ValueError: If milliseconds is less than zero.
    """
    delay_milliseconds: int = milliseconds
    delay_seconds: float = 0.0

    if delay_milliseconds < MIN_SECONDS:
        raise ValueError("Pause duration must be zero or greater.")

    delay_seconds = delay_milliseconds / 1000
    pause(delay_seconds)


def seconds_elapsed(start_time: float) -> float:
    """Calculate how many seconds have passed since a starting time.

    Use monotonic() to create the starting time. A monotonic clock is useful
    for measuring elapsed time because it only moves forward.

    Args:
        start_time: Starting time returned by monotonic().

    Returns:
        Number of seconds that have passed since start_time.
    """
    current_time: float = monotonic()
    elapsed_seconds: float = current_time - start_time

    return elapsed_seconds


def interval_has_elapsed(start_time: float, interval_seconds: float) -> bool:
    """Check whether a time interval has passed.

    This helper is useful when a program needs to perform an action every few
    seconds without hiding the decision logic from the student.

    Args:
        start_time: Starting time returned by monotonic().
        interval_seconds: Number of seconds that must pass before returning
            True.

    Returns:
        True if the interval has passed; otherwise, False.

    Raises:
        ValueError: If interval_seconds is less than zero.
    """
    required_interval_seconds: float = interval_seconds
    elapsed_seconds: float = 0.0
    has_elapsed: bool = False

    if required_interval_seconds < MIN_SECONDS:
        raise ValueError("Interval duration must be zero or greater.")

    elapsed_seconds = seconds_elapsed(start_time)
    has_elapsed = elapsed_seconds >= required_interval_seconds

    return has_elapsed


def current_time_marker() -> float:
    """Return the current monotonic time marker.

    This function gives programs a readable way to record a starting time
    before checking elapsed time later.

    Returns:
        Current monotonic time as a float.
    """
    time_marker: float = monotonic()

    return time_marker


def main() -> None:
    """Display a short timing summary when run directly.

    The main function is not used when this module is imported into another
    program. It gives students and instructors a quick way to verify that the
    module can run without syntax errors.
    """
    summary_message: str = "rpilib timing defaults"
    loop_message: str = f"Default loop delay: {DEFAULT_LOOP_SLEEP_SECONDS} second(s)"
    display_message: str = (
        f"Default display refresh: {DEFAULT_DISPLAY_REFRESH_SECONDS} second(s)"
    )
    morse_message: str = (
        f"Morse dot: {MORSE_DOT_SECONDS} second(s), "
        f"Morse dash: {MORSE_DASH_SECONDS} second(s)"
    )

    print(summary_message)
    print(loop_message)
    print(display_message)
    print(morse_message)


if __name__ == "__main__":
    main()


# AI acknowledgement:
# Generative AI assistance was used to help draft, revise, or review this
# module. The author reviewed and tested the code and is responsible for the
# final version.
