"""Provide reusable LED helpers for Raspberry Pi GPIO pins.

This module is part of the rpilib library. It provides small helper
functions for controlling standard on/off LEDs connected to Raspberry Pi
GPIO pins.

The functions in this file use gpiozero. The gpiozero library is a beginner-
friendly hardware library that handles much of the GPIO setup and cleanup
for us while still letting students work directly with pin numbers.

Example:
    from rpilib.gpio.leds import create_led, turn_on, turn_off

    red_led = create_led(pin=18)
    turn_on(red_led)
    turn_off(red_led)

Future improvements:
    - Add support for active-low LED circuits.
    - Add support for blinking patterns and reusable LED groups.
"""

from typing import Final

from gpiozero import LED

from rpilib.config import DEFAULT_RED_LED_PIN


# ---------------------------------------------------------------------------
# LED defaults
# ---------------------------------------------------------------------------
# The default LED pin comes from rpilib.config so the same course wiring value
# is stored in one place. Student programs can still pass a different pin when
# their circuit uses different wiring.
DEFAULT_LED_PIN: Final[int] = DEFAULT_RED_LED_PIN


def create_led(pin: int = DEFAULT_LED_PIN) -> LED:
    """Create and return an LED object for one GPIO pin.

    Args:
        pin: Broadcom GPIO pin number connected to the LED.

    Returns:
        A gpiozero LED object that can be turned on, turned off, or blinked.
    """
    led_pin: int = pin
    led: LED

    # GPIO pin numbers in this library use Broadcom GPIO numbering. This is the
    # same numbering style used by gpiozero when an integer pin number is given.
    led = LED(led_pin)

    return led


def turn_on(led: LED) -> None:
    """Turn on an LED.

    Args:
        led: The gpiozero LED object to turn on.
    """
    target_led: LED = led

    target_led.on()


def turn_off(led: LED) -> None:
    """Turn off an LED.

    Args:
        led: The gpiozero LED object to turn off.
    """
    target_led: LED = led

    target_led.off()


def toggle(led: LED) -> None:
    """Switch an LED to the opposite state.

    If the LED is off, this function turns it on. If the LED is on, this
    function turns it off.

    Args:
        led: The gpiozero LED object to toggle.
    """
    target_led: LED = led

    target_led.toggle()


def blink(
    led: LED,
    on_seconds: float = 1.0,
    off_seconds: float = 1.0,
    repetitions: int | None = None,
    background: bool = True,
) -> None:
    """Blink an LED using a simple on/off pattern.

    Args:
        led: The gpiozero LED object to blink.
        on_seconds: Number of seconds the LED stays on during each blink.
        off_seconds: Number of seconds the LED stays off during each blink.
        repetitions: Number of times to repeat the blink pattern. Use None to
            blink continuously.
        background: If True, blinking happens in the background while the
            program continues. If False, the program waits until blinking ends.

    Raises:
        ValueError: If on_seconds, off_seconds, or repetitions is invalid.
    """
    target_led: LED = led
    blink_on_seconds: float = on_seconds
    blink_off_seconds: float = off_seconds
    blink_repetitions: int | None = repetitions
    run_in_background: bool = background

    if blink_on_seconds < 0:
        raise ValueError("LED on time must be zero or greater.")

    if blink_off_seconds < 0:
        raise ValueError("LED off time must be zero or greater.")

    if blink_repetitions is not None and blink_repetitions < 1:
        raise ValueError("LED blink repetitions must be one or greater.")

    target_led.blink(
        on_time=blink_on_seconds,
        off_time=blink_off_seconds,
        n=blink_repetitions,
        background=run_in_background,
    )


def close_led(led: LED) -> None:
    """Release the GPIO resources used by an LED.

    gpiozero usually handles cleanup when a program exits. This helper is still
    useful when a program creates and removes hardware objects while it is
    running.

    Args:
        led: The gpiozero LED object to close.
    """
    target_led: LED = led

    # Closing a gpiozero device releases the pin so another object or program
    # can use it later.
    target_led.close()


def main() -> None:
    """Run a short LED demonstration when this module is executed directly.

    The main function is not used when this module is imported into another
    program. It gives students and instructors a quick way to test the module
    on a Raspberry Pi with an LED connected to the default pin.
    """
    demo_led: LED
    message: str = f"Testing LED on GPIO {DEFAULT_LED_PIN}"

    print(message)

    demo_led = create_led()
    blink(demo_led, on_seconds=0.5, off_seconds=0.5, repetitions=3, background=False)
    turn_off(demo_led)
    close_led(demo_led)

    print("LED test complete.")


if __name__ == "__main__":
    main()


# AI acknowledgement:
# Generative AI assistance was used to help draft, revise, or review this
# module. The author reviewed and tested the code and is responsible for the
# final version.
