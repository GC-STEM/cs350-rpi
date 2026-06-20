"""Provide reusable I2C communication helpers for rpilib.

This module is part of the rpilib library. It provides helper functions for
creating and checking an I2C bus connection on a Raspberry Pi.

I2C is a communication bus that allows a Raspberry Pi to communicate with
compatible devices, such as sensors and displays, using a small number of
wires. Many I2C devices share the same SDA and SCL pins, but each device should
have its own address.

The functions in this module use board.I2C() from Adafruit Blinka. Blinka
provides CircuitPython-style hardware support for regular Python programs
running on Raspberry Pi OS.

Example:
    from rpilib.comms.i2c import create_i2c_bus, scan_i2c_addresses

    i2c_bus = create_i2c_bus()
    addresses = scan_i2c_addresses(i2c_bus)

    print(addresses)

Future improvements:
    - Add helper functions for displaying I2C addresses in hexadecimal format.
    - Add optional retry logic for devices that are slow to respond.
"""

from typing import Final

import board
from busio import I2C


# ---------------------------------------------------------------------------
# I2C defaults
# ---------------------------------------------------------------------------
# I2C device addresses are often shown in hexadecimal. For example, 0x38 is a
# common address for some AHT20 temperature and humidity sensors.
HEX_PREFIX: Final[str] = "0x"

# I2C addresses are usually displayed with two hexadecimal digits.
HEX_ADDRESS_WIDTH: Final[int] = 2


def create_i2c_bus() -> I2C:
    """Create and return the default Raspberry Pi I2C bus.

    The default Raspberry Pi I2C bus uses the board's standard SDA and SCL pins.
    SDA carries data, and SCL carries the clock signal that keeps devices in
    sync.

    Returns:
        An I2C bus object that can communicate with I2C devices.
    """
    i2c_bus: I2C

    # board.I2C() uses the board's default I2C pins. On a Raspberry Pi, this
    # usually means the standard SDA and SCL pins on the 40-pin header.
    i2c_bus = board.I2C()

    return i2c_bus


def try_lock_i2c_bus(i2c_bus: I2C) -> bool:
    """Try to lock the I2C bus for one operation.

    Some I2C operations require a lock so only one part of the program uses the
    bus at a time. This helps prevent mixed or interrupted communication.

    Args:
        i2c_bus: I2C bus object to lock.

    Returns:
        True if the bus was locked; otherwise, False.
    """
    bus: I2C = i2c_bus
    locked: bool = bus.try_lock()

    return locked


def unlock_i2c_bus(i2c_bus: I2C) -> None:
    """Unlock the I2C bus.

    Args:
        i2c_bus: I2C bus object to unlock.
    """
    bus: I2C = i2c_bus

    bus.unlock()


def scan_i2c_addresses(i2c_bus: I2C) -> list[int]:
    """Scan the I2C bus and return detected device addresses.

    Args:
        i2c_bus: I2C bus object to scan.

    Returns:
        List of detected I2C device addresses as integers.
    """
    bus: I2C = i2c_bus
    addresses: list[int] = []

    # The bus must be locked before scanning. The finally block makes sure the
    # bus is unlocked even if the scan fails.
    while not try_lock_i2c_bus(bus):
        pass

    try:
        addresses = bus.scan()
    finally:
        unlock_i2c_bus(bus)

    return addresses


def format_i2c_address(address: int) -> str:
    """Format one I2C address as a hexadecimal string.

    Hexadecimal is base 16. It is commonly used for hardware addresses because
    it is shorter and easier to read than long binary values.

    Args:
        address: I2C device address as an integer.

    Returns:
        I2C address formatted as a string, such as "0x38".

    Raises:
        ValueError: If address is less than zero.
    """
    i2c_address: int = address
    formatted_address: str = ""

    if i2c_address < 0:
        raise ValueError("I2C address must be zero or greater.")

    formatted_address = f"{HEX_PREFIX}{i2c_address:0{HEX_ADDRESS_WIDTH}x}"

    return formatted_address


def format_i2c_addresses(addresses: list[int]) -> list[str]:
    """Format several I2C addresses as hexadecimal strings.

    Args:
        addresses: List of I2C device addresses as integers.

    Returns:
        List of formatted I2C address strings.
    """
    i2c_addresses: list[int] = addresses
    formatted_addresses: list[str] = []

    for address in i2c_addresses:
        formatted_addresses.append(format_i2c_address(address))

    return formatted_addresses


def main() -> None:
    """Run a short I2C scan when this module is executed directly.

    The main function is not used when this module is imported into another
    program. It gives students and instructors a quick way to test whether I2C
    devices are detected by the Raspberry Pi.

    This demo may return an empty list if no I2C devices are connected or if
    the Raspberry Pi I2C interface is not enabled.
    """
    i2c_bus: I2C
    addresses: list[int] = []
    formatted_addresses: list[str] = []
    message: str = "Scanning I2C bus..."

    print(message)

    i2c_bus = create_i2c_bus()
    addresses = scan_i2c_addresses(i2c_bus)
    formatted_addresses = format_i2c_addresses(addresses)

    print(f"I2C devices found: {formatted_addresses}")


if __name__ == "__main__":
    main()


# AI acknowledgement:
# Generative AI assistance was used to help draft, revise, or review this
# module. The author reviewed and tested the code and is responsible for the
# final version.
