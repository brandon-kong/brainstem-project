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

class Print():
    
    def print_bold_magenta(message: str):
        print(f"{COLORS.BOLD_MAGENTA}{message}{COLORS.ENDC}")

    def print_bold_green(message: str):
        print(f"{COLORS.BOLD_GREEN}{message}{COLORS.ENDC}")

    def print_bold_red(message: str):
        print(f"{COLORS.BOLD_RED}{message}{COLORS.ENDC}")

    def print_bold_cyan(message: str):
        print(f"{COLORS.BOLD_CYAN}{message}{COLORS.ENDC}")

    def print_bold_yellow(message: str):
        print(f"{COLORS.BOLD_YELLOW}{message}{COLORS.ENDC}")

    def print_bold_blue(message: str):
        print(f"{COLORS.BOLD_BLUE}{message}{COLORS.ENDC}")

    def print_bold_white(message: str):
        print(f"{COLORS.BOLD_WHITE}{message}{COLORS.ENDC}")

    def print_bold_black(message: str):
        print(f"{COLORS.BOLD_BLACK}{message}{COLORS.ENDC}")

    def print_bold(message: str):
        print(f"{COLORS.BOLD}{message}{COLORS.ENDC}")

    def print_underline(message: str):
        print(f"{COLORS.UNDERLINE}{message}{COLORS.ENDC}")

    def print_black(message: str):
        print(f"{COLORS.BLACK}{message}{COLORS.ENDC}")

    def print_red(message: str):
        print(f"{COLORS.RED}{message}{COLORS.ENDC}")

    def print_green(message: str):
        print(f"{COLORS.GREEN}{message}{COLORS.ENDC}")

    def print_yellow(message: str):
        print(f"{COLORS.YELLOW}{message}{COLORS.ENDC}")

    def print_blue(message: str):
        print(f"{COLORS.BLUE}{message}{COLORS.ENDC}")

    def print_magenta(message: str):
        print(f"{COLORS.MAGENTA}{message}{COLORS.ENDC}")

    def print_cyan(message: str):
        print(f"{COLORS.CYAN}{message}{COLORS.ENDC}")

    def print_white(message: str):
        print(f"{COLORS.WHITE}{message}{COLORS.ENDC}")
