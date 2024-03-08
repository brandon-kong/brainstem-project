"""
util/print.py

This module is responsible for providing functions that can be used to display
output to the user.
"""

# Imports
import os
from typing import Optional

# Constants
from util.constants import TERMINAL_COLORS as COLORS


def primary(message: str) -> str:
    """
    Displays a primary message to the user.

    :param message:
    :return:
    """

    return COLORS.MAGENTA + str(message) + COLORS.RESET


def error(message: str) -> str:
    """
    Displays an error message to the user.

    :param message:
    :return:
    """

    return COLORS.RED + str(message) + COLORS.RESET


def success(message: str) -> str:
    """
    Displays a success message to the user.

    :param message:
    :return:
    """

    return COLORS.GREEN + str(message) + COLORS.RESET


def info(message: str) -> str:
    """
    Displays an info message to the user.

    :param message:
    :return:
    """

    return COLORS.CYAN + str(message) + COLORS.RESET


def warning(message: str) -> str:
    """
    Displays a warning message to the user.

    :param message:
    :return:
    """

    return COLORS.YELLOW + str(message) + COLORS.RESET


def bold(message: str) -> str:
    """
    Makes the message bold.

    :param message:
    :return:
    """

    return COLORS.BOLD + str(message) + COLORS.RESET


def underline(message: str) -> str:
    """
    Underlines the message.

    :param message:
    :return:
    """

    return COLORS.UNDERLINE + str(message) + COLORS.RESET

def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def horizontal_line():
    """
    Prints a horizontal line.
    """
    print("=" * 80)
