"""Provide GPIO Zero mock-pin helpers for rpilib tests.

This module is part of the rpilib library. It provides helper functions for
testing GPIO code without using physical Raspberry Pi hardware.

These helpers are useful for Level 2 tests. A Level 2 test uses simulated GPIO
pins to check whether LED and button logic behaves as expected. This does not
test real wiring, resistors, LEDs, or buttons.

Example:
    from gpiozero import Button, LED
    from rpilib.testing.gpio_mock import configure_mock_gpio, press_button

    configure_mock_gpio()

    led = LED(18)
    button = Button(24)
    press_button(button)

Future improvements:
    - Add helpers for testing multiple buttons as a group.
    - Add simple examples showing how to combine mock GPIO tests with pytest.
"""

from typing import Final

from gpiozero import Button, Device, LED, PWMLED
from gpiozero.pins.mock import MockFactory, MockPin, MockPWMPin


# ---------------------------------------------------------------------------
# Mock GPIO defaults
# ---------------------------------------------------------------------------
# A mock pin factory tells GPIO Zero to simulate GPIO pins instead of talking
# to the physical Raspberry Pi GPIO hardware.
DEFAULT_SUPPORT_PWM: Final[bool] = True


def configure_mock_gpio(support_pwm: bool = DEFAULT_SUPPORT_PWM) -> None:
    """Configure GPIO Zero to use mock pins.

    This function should be called before creating gpiozero LED, PWMLED, or
    Button objects that should use simulated pins.

    Args:
        support_pwm: If True, configure mock pins that support PWM behavior.
    """
    use_pwm: bool = support_pwm

    # MockPWMPin supports PWM-style output used by PWMLED. MockPin is enough
    # for simple on/off LEDs and buttons.
    if use_pwm:
        Device.pin_factory = MockFactory(pin_class=MockPWMPin)
    else:
        Device.pin_factory = MockFactory(pin_class=MockPin)


def reset_pin_factory() -> None:
    """Reset the GPIO Zero pin factory setting.

    After this function runs, GPIO Zero will choose its normal pin factory the
    next time a device is created. Use this after mock tests if the same Python
    session will later create real hardware devices.
    """
    Device.pin_factory = None


def create_mock_led(pin: int) -> LED:
    """Create a simulated on/off LED.

    Args:
        pin: Broadcom GPIO pin number to simulate.

    Returns:
        A gpiozero LED object using a mock pin.
    """
    led_pin: int = pin
    led: LED

    led = LED(led_pin)

    return led


def create_mock_pwm_led(pin: int) -> PWMLED:
    """Create a simulated PWM LED.

    Args:
        pin: Broadcom GPIO pin number to simulate.

    Returns:
        A gpiozero PWMLED object using a mock PWM pin.
    """
    led_pin: int = pin
    led: PWMLED

    led = PWMLED(led_pin)

    return led


def create_mock_button(pin: int, pull_up: bool = True) -> Button:
    """Create a simulated button.

    Args:
        pin: Broadcom GPIO pin number to simulate.
        pull_up: If True, the button is pressed when the pin is driven low.

    Returns:
        A gpiozero Button object using a mock pin.
    """
    button_pin: int = pin
    button_pull_up: bool = pull_up
    button: Button

    button = Button(button_pin, pull_up=button_pull_up)

    return button


def press_button(button: Button) -> None:
    """Simulate pressing a button.

    Args:
        button: The gpiozero Button object to simulate.
    """
    target_button: Button = button
    uses_pull_up: bool = True

    # Most Raspberry Pi button examples use pull-up wiring. With pull_up=True,
    # pressing the button connects the pin to ground, so the pin is driven low.
    uses_pull_up = bool(getattr(target_button, "pull_up", True))

    if uses_pull_up:
        target_button.pin.drive_low()
    else:
        target_button.pin.drive_high()


def release_button(button: Button) -> None:
    """Simulate releasing a button.

    Args:
        button: The gpiozero Button object to simulate.
    """
    target_button: Button = button
    uses_pull_up: bool = True

    uses_pull_up = bool(getattr(target_button, "pull_up", True))

    if uses_pull_up:
        target_button.pin.drive_high()
    else:
        target_button.pin.drive_low()


def led_is_on(led: LED | PWMLED) -> bool:
    """Check whether a simulated LED is on.

    Args:
        led: The gpiozero LED or PWMLED object to check.

    Returns:
        True if the LED value is greater than zero; otherwise, False.
    """
    target_led: LED | PWMLED = led
    is_on: bool = target_led.value > 0

    return is_on


def main() -> None:
    """Run a short mock GPIO demonstration when executed directly.

    The main function is not used when this module is imported into another
    program. It gives students and instructors a quick way to verify that mock
    GPIO setup is working.
    """
    led: LED
    button: Button

    print("Configuring mock GPIO pins...")
    configure_mock_gpio()

    led = create_mock_led(pin=18)
    button = create_mock_button(pin=24)

    led.on()
    print(f"LED on after led.on(): {led_is_on(led)}")

    press_button(button)
    print(f"Button pressed after press_button(): {button.is_pressed}")

    release_button(button)
    print(f"Button pressed after release_button(): {button.is_pressed}")

    led.close()
    button.close()
    reset_pin_factory()

    print("Mock GPIO test complete.")


if __name__ == "__main__":
    main()


# AI acknowledgement:
# Generative AI assistance was used to help draft, revise, or review this
# module. The author reviewed and tested the code and is responsible for the
# final version.
