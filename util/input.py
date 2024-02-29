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

    print(COLORS.CYAN)

    print(message)
    for i, choice in enumerate(choices):
        print(f"{i + 1}. {choice}")

    print(COLORS.ENDC)

    choice = input("Enter the number of your choice: ")

    print()
    
    try:
        # handle 0-based index

        if int(choice) == 0:
            raise ValueError

        return int(choice)
    
    except (ValueError, IndexError):
        print("Invalid choice. Please try again.")
        print(COLORS.ENDC)

        return list_input(message, choices)
    
    

def text_input(message: str) -> str:
    """
    Gets a text input from the user and returns it.

    :param message:
    :return:
    """

    return input(message)