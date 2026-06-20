"""Provide reusable UART serial communication helpers for rpilib.

This module is part of the rpilib library. It provides helper functions for
opening a UART serial connection and sending or receiving text lines.

UART is a serial communication method. In these course projects, UART lets a
Raspberry Pi send text data to another device, such as a computer, USB-to-TTL
adapter, or another Raspberry Pi.

The functions in this module use pyserial. A serial connection sends bytes, so
these helpers encode outgoing strings into bytes and decode incoming bytes back
into strings.

Example:
    from rpilib.comms.uart import open_uart, write_line, read_line, close_uart

    serial_connection = open_uart(port="/dev/ttyS0")
    write_line(serial_connection, "on")
    response = read_line(serial_connection)
    close_uart(serial_connection)

Future improvements:
    - Add support for structured messages, such as CSV or JSON.
    - Add retry logic for unreliable serial connections.
"""

from typing import Final

import serial
from serial import Serial

from rpilib.config import (
    DEFAULT_BAUD_RATE,
    DEFAULT_TEXT_ENCODING,
    DEFAULT_UART_PORT,
    DEFAULT_UART_TIMEOUT_SECONDS,
)


# ---------------------------------------------------------------------------
# UART defaults
# ---------------------------------------------------------------------------
# These defaults come from rpilib.config so serial settings are stored in one
# place. Student programs can still pass different values when needed.
DEFAULT_PORT: Final[str] = DEFAULT_UART_PORT
DEFAULT_TIMEOUT_SECONDS: Final[float] = DEFAULT_UART_TIMEOUT_SECONDS
DEFAULT_ENCODING: Final[str] = DEFAULT_TEXT_ENCODING

# These settings match the common 8N1 serial configuration:
# 8 data bits, no parity bit, and 1 stop bit.
DEFAULT_PARITY: Final[str] = serial.PARITY_NONE
DEFAULT_STOP_BITS: Final[int] = serial.STOPBITS_ONE
DEFAULT_BYTE_SIZE: Final[int] = serial.EIGHTBITS

# A newline marks the end of one text line in many serial programs.
DEFAULT_LINE_ENDING: Final[str] = "\n"


def open_uart(
    port: str = DEFAULT_PORT,
    baud_rate: int = DEFAULT_BAUD_RATE,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
) -> Serial:
    """Open and return a UART serial connection.

    Args:
        port: Serial device path, such as "/dev/ttyS0" or "/dev/ttyUSB0".
        baud_rate: Communication speed in bits per second.
        timeout_seconds: Number of seconds to wait during read operations.

    Returns:
        A pyserial Serial object connected to the requested port.

    Raises:
        ValueError: If baud_rate or timeout_seconds is invalid.
        serial.SerialException: If the serial port cannot be opened.
    """
    uart_port: str = port
    uart_baud_rate: int = baud_rate
    uart_timeout_seconds: float = timeout_seconds
    uart_connection: Serial

    if uart_baud_rate < 1:
        raise ValueError("UART baud rate must be one or greater.")

    if uart_timeout_seconds < 0:
        raise ValueError("UART timeout must be zero or greater.")

    # pyserial handles the lower-level serial setup. This library uses common
    # 8N1 settings because they match the course examples and many UART devices.
    uart_connection = serial.Serial(
        port=uart_port,
        baudrate=uart_baud_rate,
        parity=DEFAULT_PARITY,
        stopbits=DEFAULT_STOP_BITS,
        bytesize=DEFAULT_BYTE_SIZE,
        timeout=uart_timeout_seconds,
    )

    return uart_connection


def write_text(
    uart_connection: Serial,
    message: str,
    encoding: str = DEFAULT_ENCODING,
) -> int:
    """Write text to a UART serial connection.

    This function sends the message exactly as provided. It does not add a
    newline. Use write_line() when the receiving program expects line-based
    input.

    Args:
        uart_connection: Open pyserial Serial object.
        message: Text to send.
        encoding: Text encoding used to convert the string into bytes.

    Returns:
        Number of bytes written to the serial connection.
    """
    connection: Serial = uart_connection
    outgoing_message: str = message
    text_encoding: str = encoding
    outgoing_bytes: bytes = b""
    bytes_written: int = 0

    # Serial connections send bytes, not Python strings. Encoding changes the
    # string into bytes before writing it to the UART connection.
    outgoing_bytes = outgoing_message.encode(text_encoding)
    bytes_written = connection.write(outgoing_bytes)

    return bytes_written


def write_line(
    uart_connection: Serial,
    message: str,
    line_ending: str = DEFAULT_LINE_ENDING,
    encoding: str = DEFAULT_ENCODING,
) -> int:
    """Write one line of text to a UART serial connection.

    A line ending is added to the message so the receiving program can use
    readline() to read one complete command or status update.

    Args:
        uart_connection: Open pyserial Serial object.
        message: Text to send before the line ending.
        line_ending: Text added to mark the end of the line.
        encoding: Text encoding used to convert the string into bytes.

    Returns:
        Number of bytes written to the serial connection.
    """
    connection: Serial = uart_connection
    outgoing_message: str = message
    outgoing_line_ending: str = line_ending
    text_encoding: str = encoding
    line_message: str = ""

    line_message = outgoing_message + outgoing_line_ending

    return write_text(connection, line_message, text_encoding)


def read_bytes(uart_connection: Serial, byte_count: int = 1) -> bytes:
    """Read a specific number of bytes from a UART serial connection.

    Args:
        uart_connection: Open pyserial Serial object.
        byte_count: Maximum number of bytes to read.

    Returns:
        Bytes read from the serial connection. This may be empty if the timeout
        ends before data arrives.

    Raises:
        ValueError: If byte_count is less than one.
    """
    connection: Serial = uart_connection
    bytes_to_read: int = byte_count
    incoming_bytes: bytes = b""

    if bytes_to_read < 1:
        raise ValueError("UART byte count must be one or greater.")

    incoming_bytes = connection.read(bytes_to_read)

    return incoming_bytes


def read_line(
    uart_connection: Serial,
    encoding: str = DEFAULT_ENCODING,
    strip_line_ending: bool = True,
) -> str:
    """Read one line of text from a UART serial connection.

    The serial connection waits until it receives a line ending or reaches its
    timeout. If no data arrives before the timeout, this function returns an
    empty string.

    Args:
        uart_connection: Open pyserial Serial object.
        encoding: Text encoding used to convert incoming bytes into a string.
        strip_line_ending: If True, remove whitespace such as "\\n" from the
            beginning and end of the returned string.

    Returns:
        Text line read from the serial connection.
    """
    connection: Serial = uart_connection
    text_encoding: str = encoding
    should_strip_line_ending: bool = strip_line_ending
    incoming_bytes: bytes = b""
    incoming_text: str = ""

    # readline() returns bytes. Decoding changes those bytes into a Python
    # string so the program can use normal text operations.
    incoming_bytes = connection.readline()
    incoming_text = incoming_bytes.decode(text_encoding)

    if should_strip_line_ending:
        incoming_text = incoming_text.strip()

    return incoming_text


def data_waiting(uart_connection: Serial) -> int:
    """Check how many bytes are waiting to be read.

    Args:
        uart_connection: Open pyserial Serial object.

    Returns:
        Number of bytes currently waiting in the serial input buffer.
    """
    connection: Serial = uart_connection
    waiting_bytes: int = connection.in_waiting

    return waiting_bytes


def flush_uart(uart_connection: Serial) -> None:
    """Flush pending UART output.

    Flushing asks pyserial to finish sending buffered output. This can help when
    a program writes data and then immediately exits.

    Args:
        uart_connection: Open pyserial Serial object.
    """
    connection: Serial = uart_connection

    connection.flush()


def close_uart(uart_connection: Serial) -> None:
    """Close a UART serial connection.

    Args:
        uart_connection: Open pyserial Serial object.
    """
    connection: Serial = uart_connection

    # Closing the connection releases the serial port so another program can use
    # it later.
    connection.close()


def main() -> None:
    """Run a short UART demonstration when executed directly.

    The main function is not used when this module is imported into another
    program. It gives students and instructors a quick way to verify that the
    module can open a serial connection.

    This demo may fail if no serial device is connected to the default port.
    """
    demo_connection: Serial
    message: str = f"Testing UART connection on {DEFAULT_PORT}"

    print(message)

    try:
        demo_connection = open_uart()
        write_line(demo_connection, "rpilib UART test")
        flush_uart(demo_connection)
        close_uart(demo_connection)
        print("UART test complete.")
    except serial.SerialException as error:
        print(f"UART test failed: {error}")


if __name__ == "__main__":
    main()


# AI acknowledgement:
# Generative AI assistance was used to help draft, revise, or review this
# module. The author reviewed and tested the code and is responsible for the
# final version.
