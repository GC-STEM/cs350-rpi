"""Provide reusable helpers for [module purpose].

This module is part of the rpilib library. It contains [briefly describe
what this module provides] for Raspberry Pi projects.

The functions and classes in this file are designed to be small, readable,
and reusable. Students should be able to import this module into their own
programs without changing the module source code.

Example:
    from rpilib.[package_name].[module_name] import [function_or_class_name]

    [function_or_class_name](parameter=value)

Future improvements:
    - Add [possible real-world improvement].
    - Add [another possible extension if useful].
"""

# Standard library imports
# Example: from time import sleep
from typing import Final


# Third-party imports
# Example: from gpiozero import LED


# Local rpilib imports
# Example: from rpilib.config import DEFAULT_LED_PIN


# Module-level constants
# Constants use UPPER_SNAKE_CASE because their values should not change
# while the program is running.
#
# Final tells readers and type-checking tools that this value should be
# treated as a constant.
DEFAULT_VALUE: Final[str] = "replace_me"


class ExampleClass:
    """Represent [what this class models or controls].

    This class provides a reusable interface for [hardware device,
    communication method, or helper behavior].

    Attributes:
        example_attribute: Briefly explain what this attribute stores.
    """

    def __init__(self, example_parameter: str = DEFAULT_VALUE) -> None:
        """Initialize an ExampleClass object.

        Args:
            example_parameter: Briefly explain what this parameter controls.
        """
        # Store parameter values as object attributes so other methods can
        # use them later.
        self.example_attribute: str = example_parameter

    def example_method(self) -> str:
        """Perform one clear action.

        Returns:
            A brief description of what this method returns.
        """
        result: str = self.example_attribute
        return result


def example_function(example_parameter: str = DEFAULT_VALUE) -> str:
    """Perform one reusable task.

    Args:
        example_parameter: Briefly explain what this parameter controls.

    Returns:
        A brief description of the returned value.
    """
    result: str = example_parameter
    return result


def main() -> None:
    """Run a small demonstration when this module is executed directly.

    The main function is not used when this module is imported into another
    program. It gives students and instructors a quick way to test the module.
    """
    message: str = "Running module demonstration..."
    result: str = ""

    print(message)

    result = example_function()
    print(f"Example result: {result}")


if __name__ == "__main__":
    main()


# AI acknowledgement:
# Generative AI assistance was used to help draft, revise, or review this
# module. The author reviewed and tested the code and is responsible for the
# final version.
