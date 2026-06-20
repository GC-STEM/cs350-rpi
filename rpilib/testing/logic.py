"""Provide pure Python testing helpers for rpilib examples.

This module is part of the rpilib library. It provides small helper functions
for testing program logic that does not require physical Raspberry Pi hardware.

These helpers are useful for Level 1 tests. A Level 1 test checks ordinary
Python values, such as strings, numbers, lists, and Boolean results. This lets
students test logic before adding GPIO pins, sensors, displays, or serial
connections.

Example:
    from rpilib.testing.logic import assert_equal

    assert_equal(actual=2 + 2, expected=4, description="basic addition")

Future improvements:
    - Add helpers for comparing floating-point sensor values with tolerance.
    - Add simple test report formatting for multiple checks.
"""

from typing import Final


# ---------------------------------------------------------------------------
# Test result defaults
# ---------------------------------------------------------------------------
# These strings keep test output consistent across small classroom examples.
PASS_LABEL: Final[str] = "PASS"
FAIL_LABEL: Final[str] = "FAIL"


def format_result(passed: bool, description: str) -> str:
    """Format one test result as a readable message.

    Args:
        passed: True if the test passed; otherwise, False.
        description: Short description of what the test checked.

    Returns:
        A formatted test-result string.
    """
    test_passed: bool = passed
    test_description: str = description
    label: str = FAIL_LABEL
    result_message: str = ""

    if test_passed:
        label = PASS_LABEL

    result_message = f"[{label}] {test_description}"

    return result_message


def assert_equal(actual: object, expected: object, description: str) -> bool:
    """Check whether two values are equal and print the result.

    This helper is intentionally simple. It returns True or False instead of
    using a full testing framework so students can see the comparison directly.

    Args:
        actual: Value produced by the code being tested.
        expected: Value the test expects.
        description: Short description of what the test checked.

    Returns:
        True if actual equals expected; otherwise, False.
    """
    actual_value: object = actual
    expected_value: object = expected
    test_description: str = description
    passed: bool = actual_value == expected_value

    print(format_result(passed, test_description))

    if not passed:
        print(f"  Expected: {expected_value}")
        print(f"  Actual:   {actual_value}")

    return passed


def assert_true(condition: bool, description: str) -> bool:
    """Check whether a condition is True and print the result.

    Args:
        condition: Boolean expression to check.
        description: Short description of what the test checked.

    Returns:
        True if condition is True; otherwise, False.
    """
    test_condition: bool = condition
    test_description: str = description
    passed: bool = test_condition is True

    print(format_result(passed, test_description))

    return passed


def assert_false(condition: bool, description: str) -> bool:
    """Check whether a condition is False and print the result.

    Args:
        condition: Boolean expression to check.
        description: Short description of what the test checked.

    Returns:
        True if condition is False; otherwise, False.
    """
    test_condition: bool = condition
    test_description: str = description
    passed: bool = test_condition is False

    print(format_result(passed, test_description))

    return passed


def count_passed(results: list[bool]) -> int:
    """Count how many test results passed.

    Args:
        results: List of Boolean test results.

    Returns:
        Number of True values in the results list.
    """
    test_results: list[bool] = results
    passed_count: int = 0

    for result in test_results:
        if result:
            passed_count = passed_count + 1

    return passed_count


def print_summary(results: list[bool]) -> None:
    """Print a short summary for a list of test results.

    Args:
        results: List of Boolean test results.
    """
    test_results: list[bool] = results
    passed_count: int = 0
    total_count: int = 0

    total_count = len(test_results)
    passed_count = count_passed(test_results)

    print(f"Test summary: {passed_count}/{total_count} passed")


def main() -> None:
    """Run a short demonstration when this module is executed directly.

    The main function is not used when this module is imported into another
    program. It gives students and instructors a quick way to see the testing
    helpers in action.
    """
    results: list[bool] = []

    results.append(assert_equal(actual=2 + 2, expected=4, description="2 + 2 equals 4"))
    results.append(assert_true(condition=True, description="True condition passes"))
    results.append(assert_false(condition=False, description="False condition passes"))

    print_summary(results)


if __name__ == "__main__":
    main()


# AI acknowledgement:
# Generative AI assistance was used to help draft, revise, or review this
# module. The author reviewed and tested the code and is responsible for the
# final version.
