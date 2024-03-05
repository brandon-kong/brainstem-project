"""
input.py

This module is responsible for providing functions that can be used to interact
with the user. This includes getting input from the user and displaying output to
the user.

"""

# Imports

from .constants import TERMINAL_COLORS as COLORS
from typing import Optional, List


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

    for i, choice in enumerate(choices):
        print(Print.cyan(f"\t{i + 1}. {choice}"))

    try:
        # handle 0-based index
        print()
        choice = input(message)

        if int(choice) <= 0:
            raise ValueError

        val = choices[int(choice) - 1]
        return int(choice)
    
    except (ValueError, IndexError):
        print(Print.bold(Print.red("\nInvalid choice. Please try again.\n")))

        return list_input(message, choices)
    
    

def text_input(message: str) -> str:
    """
    Gets a text input from the user and returns it.

    :param message:
    :return:
    """

    return input(message)


class Print:
    def bold(message: str):
        return f"{COLORS.BOLD}{message}{COLORS.ENDC}"

    def underline(message: str):
        return f"{COLORS.UNDERLINE}{message}{COLORS.ENDC}"

    def black(message: str):
        return f"{COLORS.BLACK}{message}{COLORS.ENDC}"

    def red(message: str):
        return f"{COLORS.RED}{message}{COLORS.ENDC}"

    def green(message: str):
        return f"{COLORS.GREEN}{message}{COLORS.ENDC}"

    def yellow(message: str):
        return f"{COLORS.YELLOW}{message}{COLORS.ENDC}"

    def blue(message: str):
        return f"{COLORS.BLUE}{message}{COLORS.ENDC}"

    def magenta(message: str):
        return f"{COLORS.MAGENTA}{message}{COLORS.ENDC}"

    def cyan(message: str):
        return f"{COLORS.CYAN}{message}{COLORS.ENDC}"

    def white(message: str):
        return f"{COLORS.WHITE}{message}{COLORS.ENDC}"
