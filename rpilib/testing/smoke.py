"""Provide hardware smoke-test helpers for rpilib.

This module is part of the rpilib library. It provides short tests that run on
a real Raspberry Pi with real course hardware connected.

These helpers are useful for Level 3 tests. A Level 3 test does not prove that
the full project is correct. It only checks that one hardware feature appears
to work, such as blinking an LED or detecting a button press.

Example:
    from rpilib.testing.smoke import smoke_test_led

    smoke_test_led(pin=18)

Future improvements:
    - Add smoke tests for LCD displays, UART connections, and I2C sensors.
    - Add a simple command-line menu so students can choose which test to run.
"""

from typing import Final

from gpiozero import Button, LED, PWMLED

from rpilib.config import (
    DEFAULT_BLUE_LED_PIN,
    DEFAULT_GREEN_BUTTON_PIN,
    DEFAULT_RED_LED_PIN,
)
from rpilib.gpio.buttons import close_button, create_button, wait_for_press
from rpilib.gpio.leds import blink, close_led, create_led, turn_off
from rpilib.gpio.pwm import close_pwm_led, create_pwm_led, pulse


# ---------------------------------------------------------------------------
# Smoke-test defaults
# ---------------------------------------------------------------------------
# Smoke tests should be short. They should confirm basic hardware behavior
# without becoming a full assignment solution.
DEFAULT_BLINK_REPETITIONS: Final[int] = 3
DEFAULT_BUTTON_TIMEOUT_SECONDS: Final[float] = 10.0
DEFAULT_TEST_DELAY_SECONDS: Final[float] = 0.5


def smoke_test_led(pin: int = DEFAULT_RED_LED_PIN) -> None:
    """Blink a real LED connected to one GPIO pin.

    Args:
        pin: Broadcom GPIO pin number connected to the LED.
    """
    led_pin: int = pin
    led: LED

    print(f"Blinking LED on GPIO {led_pin}...")

    led = create_led(pin=led_pin)
    blink(
        led=led,
        on_seconds=DEFAULT_TEST_DELAY_SECONDS,
        off_seconds=DEFAULT_TEST_DELAY_SECONDS,
        repetitions=DEFAULT_BLINK_REPETITIONS,
        background=False,
    )
    turn_off(led)
    close_led(led)

    print("LED smoke test complete.")


def smoke_test_pwm_led(pin: int = DEFAULT_BLUE_LED_PIN) -> None:
    """Pulse a real PWM LED connected to one GPIO pin.

    Args:
        pin: Broadcom GPIO pin number connected to the PWM LED.
    """
    led_pin: int = pin
    led: PWMLED

    print(f"Pulsing PWM LED on GPIO {led_pin}...")

    led = create_pwm_led(pin=led_pin)
    pulse(
        led=led,
        fade_in_seconds=DEFAULT_TEST_DELAY_SECONDS,
        fade_out_seconds=DEFAULT_TEST_DELAY_SECONDS,
        repetitions=DEFAULT_BLINK_REPETITIONS,
        background=False,
    )
    close_pwm_led(led)

    print("PWM LED smoke test complete.")


def smoke_test_button(
    pin: int = DEFAULT_GREEN_BUTTON_PIN,
    timeout_seconds: float = DEFAULT_BUTTON_TIMEOUT_SECONDS,
) -> bool:
    """Wait for a real button press on one GPIO pin.

    Args:
        pin: Broadcom GPIO pin number connected to the button.
        timeout_seconds: Maximum number of seconds to wait for the button.

    Returns:
        True if the button was pressed before the timeout; otherwise, False.
    """
    button_pin: int = pin
    wait_timeout_seconds: float = timeout_seconds
    button: Button
    was_pressed: bool = False

    print(f"Waiting for button press on GPIO {button_pin}...")
    print(f"Press the button within {wait_timeout_seconds} seconds.")

    button = create_button(pin=button_pin)
    was_pressed = wait_for_press(button, timeout_seconds=wait_timeout_seconds)
    close_button(button)

    if was_pressed:
        print("Button smoke test passed.")
    else:
        print("Button smoke test did not detect a press.")

    return was_pressed


def main() -> None:
    """Run a short hardware smoke-test menu.

    The main function is not used when this module is imported into another
    program. It gives students and instructors a quick way to test real GPIO
    hardware from the command line.
    """
    choice: str = ""

    print("rpilib hardware smoke tests")
    print("1. Test red LED")
    print("2. Test blue PWM LED")
    print("3. Test green button")

    choice = input("Choose a test: ").strip()

    if choice == "1":
        smoke_test_led()
    elif choice == "2":
        smoke_test_pwm_led()
    elif choice == "3":
        smoke_test_button()
    else:
        print("No valid smoke test selected.")


if __name__ == "__main__":
    main()


# AI acknowledgement:
# Generative AI assistance was used to help draft, revise, or review this
# module. The author reviewed and tested the code and is responsible for the
# final version.
