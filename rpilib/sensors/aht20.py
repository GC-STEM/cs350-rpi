"""Provide reusable helpers for the AHT20 temperature and humidity sensor.

This module is part of the rpilib library. It contains a small wrapper class
for reading temperature and relative humidity from an AHT20/AHTx0 sensor in
Raspberry Pi projects.

The functions and classes in this file are designed to be small, readable,
and reusable. Students should be able to import this module into their own
programs without changing the module source code.

Example:
    from rpilib.sensors.aht20 import AHT20Sensor

    sensor = AHT20Sensor()
    temperature_f = sensor.get_temperature_f()
    humidity = sensor.get_humidity()

    print(f"Temperature: {temperature_f:.1f} F")
    print(f"Humidity: {humidity:.1f}%")

Future improvements:
    - Add support for other temperature and humidity sensor models.
    - Add calibration offsets for projects that need adjusted sensor readings.
"""

# Standard library imports
from typing import Final


# Third-party imports
import adafruit_ahtx0
from adafruit_ahtx0 import AHTx0
from busio import I2C


# Local rpilib imports
from rpilib.comms.i2c import create_i2c_bus
from rpilib.config import DEFAULT_TEMPERATURE_UNIT


# ---------------------------------------------------------------------------
# Sensor defaults
# ---------------------------------------------------------------------------
# Temperature units are stored as short strings because that is how students
# commonly see them in output: C for Celsius and F for Fahrenheit.
CELSIUS_UNIT: Final[str] = "C"
FAHRENHEIT_UNIT: Final[str] = "F"

# Relative humidity is reported as a percentage.
MIN_RELATIVE_HUMIDITY: Final[float] = 0.0
MAX_RELATIVE_HUMIDITY: Final[float] = 100.0


class AHT20Sensor:
    """Represent an AHT20/AHTx0 temperature and humidity sensor.

    This class provides a reusable interface for reading temperature and
    relative humidity from the sensor.

    Attributes:
        i2c_bus: The I2C bus used to communicate with the sensor.
        sensor: The Adafruit AHTx0 sensor object.
    """

    def __init__(self, i2c_bus: I2C | None = None) -> None:
        """Initialize an AHT20Sensor object.

        Args:
            i2c_bus: Optional I2C bus object. If no bus is provided, this class
                creates the default Raspberry Pi I2C bus.
        """
        self.i2c_bus: I2C
        self.sensor: AHTx0

        # Allow the caller to pass an existing I2C bus. This is useful when one
        # program needs to share the same I2C bus with several devices.
        if i2c_bus is None:
            self.i2c_bus = create_i2c_bus()
        else:
            self.i2c_bus = i2c_bus

        self.sensor = adafruit_ahtx0.AHTx0(self.i2c_bus)

    def get_temperature_c(self) -> float:
        """Read the current temperature in degrees Celsius.

        Returns:
            Current temperature in degrees Celsius.
        """
        temperature_c: float = self.sensor.temperature

        return temperature_c

    def get_temperature_f(self) -> float:
        """Read the current temperature in degrees Fahrenheit.

        Returns:
            Current temperature in degrees Fahrenheit.
        """
        temperature_c: float = 0.0
        temperature_f: float = 0.0

        temperature_c = self.get_temperature_c()
        temperature_f = celsius_to_fahrenheit(temperature_c)

        return temperature_f

    def get_temperature(self, unit: str = DEFAULT_TEMPERATURE_UNIT) -> float:
        """Read the current temperature in the requested unit.

        Args:
            unit: Temperature unit to use. Use "C" for Celsius or "F" for
                Fahrenheit.

        Returns:
            Current temperature in the requested unit.

        Raises:
            ValueError: If unit is not "C" or "F".
        """
        requested_unit: str = unit.upper()
        temperature: float = 0.0

        if requested_unit == CELSIUS_UNIT:
            temperature = self.get_temperature_c()
        elif requested_unit == FAHRENHEIT_UNIT:
            temperature = self.get_temperature_f()
        else:
            raise ValueError('Temperature unit must be "C" or "F".')

        return temperature

    def get_humidity(self) -> float:
        """Read the current relative humidity.

        Relative humidity is the amount of water vapor in the air compared
        with the maximum amount the air can hold at that temperature.

        Returns:
            Current relative humidity as a percentage.
        """
        humidity: float = self.sensor.relative_humidity

        return humidity

    def get_reading(self, unit: str = DEFAULT_TEMPERATURE_UNIT) -> dict[str, float]:
        """Read temperature and humidity together.

        Args:
            unit: Temperature unit to use. Use "C" for Celsius or "F" for
                Fahrenheit.

        Returns:
            Dictionary containing temperature and humidity values.
        """
        requested_unit: str = unit.upper()
        reading: dict[str, float] = {}

        reading = {
            "temperature": self.get_temperature(requested_unit),
            "humidity": self.get_humidity(),
        }

        return reading


def celsius_to_fahrenheit(temperature_c: float) -> float:
    """Convert a Celsius temperature to Fahrenheit.

    Args:
        temperature_c: Temperature in degrees Celsius.

    Returns:
        Equivalent temperature in degrees Fahrenheit.
    """
    celsius_value: float = temperature_c
    fahrenheit_value: float = 0.0

    fahrenheit_value = (celsius_value * 9 / 5) + 32

    return fahrenheit_value


def fahrenheit_to_celsius(temperature_f: float) -> float:
    """Convert a Fahrenheit temperature to Celsius.

    Args:
        temperature_f: Temperature in degrees Fahrenheit.

    Returns:
        Equivalent temperature in degrees Celsius.
    """
    fahrenheit_value: float = temperature_f
    celsius_value: float = 0.0

    celsius_value = (fahrenheit_value - 32) * 5 / 9

    return celsius_value


def humidity_is_valid(humidity: float) -> bool:
    """Check whether a relative humidity value is in the expected range.

    Args:
        humidity: Relative humidity percentage to check.

    Returns:
        True if humidity is between 0 and 100; otherwise, False.
    """
    humidity_value: float = humidity
    valid: bool = False

    valid = MIN_RELATIVE_HUMIDITY <= humidity_value <= MAX_RELATIVE_HUMIDITY

    return valid


def main() -> None:
    """Run a small demonstration when this module is executed directly.

    The main function is not used when this module is imported into another
    program. It gives students and instructors a quick way to test the sensor
    on a Raspberry Pi with an AHT20/AHTx0 sensor connected.
    """
    sensor: AHT20Sensor
    temperature_f: float = 0.0
    humidity: float = 0.0
    message: str = "Testing AHT20/AHTx0 temperature and humidity sensor..."

    print(message)

    sensor = AHT20Sensor()
    temperature_f = sensor.get_temperature_f()
    humidity = sensor.get_humidity()

    print(f"Temperature: {temperature_f:.1f} F")
    print(f"Humidity: {humidity:.1f}%")

    if humidity_is_valid(humidity):
        print("Humidity reading is in the expected range.")
    else:
        print("Humidity reading is outside the expected range.")


if __name__ == "__main__":
    main()


# AI acknowledgement:
# Generative AI assistance was used to help draft, revise, or review this
# module. The author reviewed and tested the code and is responsible for the
# final version.
