"""Store shared default settings and constants for the rpilib library.

This module is part of the rpilib library. It stores common default values
used by Raspberry Pi course projects, such as GPIO pin numbers, UART serial
settings, LCD dimensions, and timing values.

These values are collected in one place so other modules can import them
instead of hardcoding the same numbers or strings in several files.

Example:
    from rpilib.config import DEFAULT_RED_LED_PIN

    print(DEFAULT_RED_LED_PIN)

Future improvements:
    - Move board-specific settings into separate configuration profiles.
    - Add support for loading settings from a user-provided configuration file.
"""

from typing import Final


# ---------------------------------------------------------------------------
# GPIO pin defaults
# ---------------------------------------------------------------------------
# These pin numbers use Broadcom GPIO numbering, also called BCM numbering.
# BCM numbering refers to the GPIO labels used by the Raspberry Pi processor,
# not the physical pin numbers printed by position on the 40-pin header.
#
# Example:
# GPIO 18 is not the same thing as physical header pin 18.
GPIO_NUMBERING_MODE: Final[str] = "BCM"

# The course circuit commonly uses GPIO 18 for the red LED.
DEFAULT_RED_LED_PIN: Final[int] = 18

# The course circuit commonly uses GPIO 23 for the blue LED.
DEFAULT_BLUE_LED_PIN: Final[int] = 23

# The course circuit commonly uses GPIO 24 for the primary button.
DEFAULT_GREEN_BUTTON_PIN: Final[int] = 24

# The course circuit commonly uses GPIO 25 for the second button.
DEFAULT_RED_BUTTON_PIN: Final[int] = 25

# The course circuit commonly uses GPIO 12 for the third button.
DEFAULT_BLUE_BUTTON_PIN: Final[int] = 12


# ---------------------------------------------------------------------------
# PWM defaults
# ---------------------------------------------------------------------------
# PWM stands for pulse-width modulation. It lets a program simulate different
# brightness levels by turning a GPIO output on and off very quickly.
DEFAULT_PWM_FREQUENCY_HZ: Final[int] = 60

# Duty cycle is the percentage of time the signal is on during one PWM cycle.
# A 0% duty cycle is off. A 100% duty cycle is fully on.
DEFAULT_PWM_START_DUTY_CYCLE: Final[int] = 0

MIN_DUTY_CYCLE: Final[int] = 0
MAX_DUTY_CYCLE: Final[int] = 100


# ---------------------------------------------------------------------------
# UART serial defaults
# ---------------------------------------------------------------------------
# UART is a serial communication method. The Raspberry Pi can use UART to send
# and receive text data through a serial connection.
DEFAULT_UART_PORT: Final[str] = "/dev/ttyS0"

# Some USB-to-TTL serial cables appear as /dev/ttyUSB0 on Raspberry Pi OS.
DEFAULT_USB_UART_PORT: Final[str] = "/dev/ttyUSB0"

# Baud rate controls how fast serial data is transmitted, in bits per second.
DEFAULT_BAUD_RATE: Final[int] = 115200

# Timeout controls how long serial reads wait before giving up.
DEFAULT_UART_TIMEOUT_SECONDS: Final[float] = 1.0

# UTF-8 is the standard text encoding used by most modern Python programs.
DEFAULT_TEXT_ENCODING: Final[str] = "utf-8"


# ---------------------------------------------------------------------------
# LCD defaults
# ---------------------------------------------------------------------------
# The course display is a 16-column by 2-row character LCD.
DEFAULT_LCD_COLUMNS: Final[int] = 16
DEFAULT_LCD_ROWS: Final[int] = 2

# These values match the common course wiring for the LCD data and control pins.
DEFAULT_LCD_RS_PIN: Final[str] = "D17"
DEFAULT_LCD_ENABLE_PIN: Final[str] = "D27"
DEFAULT_LCD_D4_PIN: Final[str] = "D5"
DEFAULT_LCD_D5_PIN: Final[str] = "D6"
DEFAULT_LCD_D6_PIN: Final[str] = "D13"
DEFAULT_LCD_D7_PIN: Final[str] = "D26"


# ---------------------------------------------------------------------------
# Sensor defaults
# ---------------------------------------------------------------------------
# The course temperature and humidity sensor uses the AHT20/AHTx0 family.
DEFAULT_TEMPERATURE_UNIT: Final[str] = "F"

# The default thermostat set point is expressed in degrees Fahrenheit.
DEFAULT_THERMOSTAT_SET_POINT_F: Final[int] = 72


# ---------------------------------------------------------------------------
# Timing defaults
# ---------------------------------------------------------------------------
# These values are used by example programs and helper functions that pause
# between hardware updates.
DEFAULT_LOOP_SLEEP_SECONDS: Final[float] = 1.0
DEFAULT_DISPLAY_REFRESH_SECONDS: Final[float] = 1.0
DEFAULT_SENSOR_READ_SECONDS: Final[float] = 5.0
DEFAULT_SERIAL_UPDATE_SECONDS: Final[float] = 30.0

# Morse code timing values used in the LED messaging assignment.
MORSE_DOT_SECONDS: Final[float] = 0.5
MORSE_DASH_SECONDS: Final[float] = 1.5
MORSE_SYMBOL_PAUSE_SECONDS: Final[float] = 0.25
MORSE_LETTER_PAUSE_SECONDS: Final[float] = 0.75
MORSE_WORD_PAUSE_SECONDS: Final[float] = 3.0


def main() -> None:
    """Display a short configuration summary when run directly.

    The main function is not used when this module is imported into another
    program. It gives students and instructors a quick way to verify that the
    module can run without syntax errors.
    """
    summary_message: str = "rpilib configuration defaults"
    gpio_message: str = (
        f"LED pins: red={DEFAULT_RED_LED_PIN}, blue={DEFAULT_BLUE_LED_PIN}"
    )
    uart_message: str = (
        f"UART: port={DEFAULT_UART_PORT}, baud={DEFAULT_BAUD_RATE}"
    )
    lcd_message: str = (
        f"LCD: {DEFAULT_LCD_COLUMNS} columns x {DEFAULT_LCD_ROWS} rows"
    )

    print(summary_message)
    print(gpio_message)
    print(uart_message)
    print(lcd_message)


if __name__ == "__main__":
    main()


# AI acknowledgement:
# Generative AI assistance was used to help draft, revise, or review this
# module. The author reviewed and tested the code and is responsible for the
# final version.
