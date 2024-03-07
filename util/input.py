"""
input.py

This module is responsible for providing functions that can be used to interact
with the user. This includes getting input from the user and displaying output to
the user.

"""

# Imports
from typing import Optional, List, Tuple

# Constants
from util.constants import BACK_KEYWORD

# Utilities
from util.print import (
    primary,
    error,
    success,
    info,
)


def user_input(input_type: str, message: str, choices: Optional[List[str]] = None) -> str | int:
    """
    Gets input from the user and returns it based on the input type.

    :param input_type:
    :param message:
    :param choices:
    :return:
    """

    if input_type == "list":
        return list_input(message, choices)
    else:
        return text_input(message)


def list_input(message: str, choices: list[str]) -> int:
    """
    Gets a list input from the user and returns it.

    :param message:
    :param choices:
    :return:
    """

    print("")

    for i, choice in enumerate(choices):
        print(info(f"\t{i + 1}. {choice}"))

    try:
        # handle 0-based index
        print()
        choice = input(message)

        if int(choice) <= 0:
            raise ValueError

        val = choices[int(choice) - 1]
        return int(choice)

    except (ValueError, IndexError):
        print(error("\nInvalid choice. Please try again.\n"))

        return list_input(message, choices)


def text_input(message: str) -> str:
    """
    Gets a text input from the user and returns it.

    :param message:
    :return:
    """

    return input(message)


# Past this point, I have updated better implementation

def get_yes_no_input(message: str) -> bool:
    """
    Gets a yes/no input from the user and returns it.

    :param message:
    :return:
    """

    yes_alias = ["yes", "y"]
    no_alias = ["no", "n"]

    choice = input(f"{message} (y/n): ").lower()

    while choice not in yes_alias + no_alias:
        print(error("Invalid choice. Please try again."))
        choice = input().lower()

    return choice in yes_alias


def get_text_input(message: str, default=None) -> str:
    """
    Gets input from the user and returns it based on the input type.

    :param message:
    :param choices:
    :return:
    """

    choice = input(message)

    if not choice and default:
        return default

    while not choice:
        print(error("Invalid choice. Please try again."))
        choice = input()

    return choice

def get_int_input(message: str) -> int:
    """
    Gets an integer input from the user and returns it.

    :param message:
    :return:
    """

    print(message)
    choice = input(message)

    while not choice.isdigit():
        print(error("Invalid choice. Please try again."))
        choice = input()

    return int(choice)


def get_float_input(message: str) -> float:
    """
    Gets a float input from the user and returns it.

    :param message:
    :return:
    """

    print(message)
    choice = input()

    while not choice.replace(".", "", 1).isdigit():
        print(error("Invalid choice. Please try again."))
        choice = input()

    return float(choice)


def get_choice_input(
        message: str,
        choices: list[str],
        can_go_back: bool = True
) -> Tuple[int, str, bool]:
    """
    Gets a choice input from the user and returns it.

    :param message:
    :param choices:
    :param can_go_back:
    :return:
    """

    for i, choice in enumerate(choices):
        print(info(f"\t[{i + 1}] {choice}"))

    if can_go_back:
        print(info(f"\t[{BACK_KEYWORD}] Back"))

    print()

    choice = input(message)

    while not choice.isdigit() or int(choice) < 1 or int(choice) > len(choices):
        if choice.lower() == BACK_KEYWORD.lower() and can_go_back:
            return -1, choice, True
        print(error("Invalid choice. Please try again."))
        choice = input()

    # New line for readability
    print()

    return int(choice), choices[int(choice) - 1], choice == BACK_KEYWORD

