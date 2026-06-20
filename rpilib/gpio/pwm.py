"""Provide reusable PWM LED helpers for Raspberry Pi GPIO pins.

This module is part of the rpilib library. It provides helper functions for
controlling LEDs with pulse-width modulation, or PWM.

PWM lets a program change LED brightness by turning a GPIO output on and off
very quickly. The LED appears dimmer or brighter depending on the duty cycle.
A duty cycle is the percentage of time the signal is on during one PWM cycle.

The functions in this file use gpiozero.PWMLED. The gpiozero library handles
much of the GPIO setup and cleanup for us while still letting students work
directly with GPIO pin numbers.

Example:
    from rpilib.gpio.pwm import create_pwm_led, pulse, set_brightness

    red_led = create_pwm_led(pin=18)
    set_brightness(red_led, brightness=0.5)
    pulse(red_led)

Future improvements:
    - Add support for LED fade patterns with custom timing.
    - Add support for RGB LEDs controlled by three PWM pins.
"""

from typing import Final

from gpiozero import PWMLED

from rpilib.config import DEFAULT_PWM_FREQUENCY_HZ, DEFAULT_RED_LED_PIN


# ---------------------------------------------------------------------------
# PWM LED defaults
# ---------------------------------------------------------------------------
# The default pin and frequency come from rpilib.config so shared course wiring
# and hardware values are stored in one place.
DEFAULT_PWM_LED_PIN: Final[int] = DEFAULT_RED_LED_PIN
DEFAULT_FREQUENCY_HZ: Final[int] = DEFAULT_PWM_FREQUENCY_HZ

# gpiozero.PWMLED brightness values use the range 0.0 through 1.0.
# 0.0 means fully off. 1.0 means fully on.
MIN_BRIGHTNESS: Final[float] = 0.0
MAX_BRIGHTNESS: Final[float] = 1.0

# Pulse timing values are measured in seconds.
DEFAULT_FADE_IN_SECONDS: Final[float] = 1.0
DEFAULT_FADE_OUT_SECONDS: Final[float] = 1.0


def create_pwm_led(
    pin: int = DEFAULT_PWM_LED_PIN,
    frequency_hz: int = DEFAULT_FREQUENCY_HZ,
) -> PWMLED:
    """Create and return a PWMLED object for one GPIO pin.

    Args:
        pin: Broadcom GPIO pin number connected to the LED.
        frequency_hz: PWM frequency in hertz. Hertz means cycles per second.

    Returns:
        A gpiozero PWMLED object that can change brightness or pulse.

    Raises:
        ValueError: If frequency_hz is less than one.
    """
    led_pin: int = pin
    pwm_frequency_hz: int = frequency_hz
    pwm_led: PWMLED

    if pwm_frequency_hz < 1:
        raise ValueError("PWM frequency must be one hertz or greater.")

    # GPIO pin numbers in this library use Broadcom GPIO numbering. This is the
    # same numbering style used by gpiozero when an integer pin number is given.
    pwm_led = PWMLED(led_pin, frequency=pwm_frequency_hz)

    return pwm_led


def set_brightness(led: PWMLED, brightness: float) -> None:
    """Set the brightness of a PWM LED.

    Args:
        led: The gpiozero PWMLED object to update.
        brightness: LED brightness from 0.0 through 1.0.

    Raises:
        ValueError: If brightness is outside the valid range.
    """
    target_led: PWMLED = led
    brightness_level: float = brightness

    if brightness_level < MIN_BRIGHTNESS or brightness_level > MAX_BRIGHTNESS:
        raise ValueError("Brightness must be between 0.0 and 1.0.")

    target_led.value = brightness_level


def turn_on(led: PWMLED) -> None:
    """Turn on a PWM LED at full brightness.

    Args:
        led: The gpiozero PWMLED object to turn on.
    """
    target_led: PWMLED = led

    target_led.on()


def turn_off(led: PWMLED) -> None:
    """Turn off a PWM LED.

    Args:
        led: The gpiozero PWMLED object to turn off.
    """
    target_led: PWMLED = led

    target_led.off()


def pulse(
    led: PWMLED,
    fade_in_seconds: float = DEFAULT_FADE_IN_SECONDS,
    fade_out_seconds: float = DEFAULT_FADE_OUT_SECONDS,
    repetitions: int | None = None,
    background: bool = True,
) -> None:
    """Fade a PWM LED in and out.

    Args:
        led: The gpiozero PWMLED object to pulse.
        fade_in_seconds: Number of seconds used to fade from off to on.
        fade_out_seconds: Number of seconds used to fade from on to off.
        repetitions: Number of times to repeat the pulse pattern. Use None to
            pulse continuously.
        background: If True, pulsing happens in the background while the
            program continues. If False, the program waits until pulsing ends.

    Raises:
        ValueError: If fade timing or repetitions are invalid.
    """
    target_led: PWMLED = led
    pulse_fade_in_seconds: float = fade_in_seconds
    pulse_fade_out_seconds: float = fade_out_seconds
    pulse_repetitions: int | None = repetitions
    run_in_background: bool = background

    if pulse_fade_in_seconds < 0:
        raise ValueError("Fade-in time must be zero or greater.")

    if pulse_fade_out_seconds < 0:
        raise ValueError("Fade-out time must be zero or greater.")

    if pulse_repetitions is not None and pulse_repetitions < 1:
        raise ValueError("Pulse repetitions must be one or greater.")

    target_led.pulse(
        fade_in_time=pulse_fade_in_seconds,
        fade_out_time=pulse_fade_out_seconds,
        n=pulse_repetitions,
        background=run_in_background,
    )


def close_pwm_led(led: PWMLED) -> None:
    """Release the GPIO resources used by a PWM LED.

    gpiozero usually handles cleanup when a program exits. This helper is still
    useful when a program creates and removes hardware objects while it is
    running.

    Args:
        led: The gpiozero PWMLED object to close.
    """
    target_led: PWMLED = led

    # Closing a gpiozero device releases the pin so another object or program
    # can use it later.
    target_led.close()


def main() -> None:
    """Run a short PWM LED demonstration when executed directly.

    The main function is not used when this module is imported into another
    program. It gives students and instructors a quick way to test the module
    on a Raspberry Pi with an LED connected to the default pin.
    """
    demo_led: PWMLED
    message: str = f"Testing PWM LED on GPIO {DEFAULT_PWM_LED_PIN}"

    print(message)

    demo_led = create_pwm_led()
    pulse(
        demo_led,
        fade_in_seconds=0.5,
        fade_out_seconds=0.5,
        repetitions=3,
        background=False,
    )
    turn_off(demo_led)
    close_pwm_led(demo_led)

    print("PWM LED test complete.")


if __name__ == "__main__":
    main()


# AI acknowledgement:
# Generative AI assistance was used to help draft, revise, or review this
# module. The author reviewed and tested the code and is responsible for the
# final version.
