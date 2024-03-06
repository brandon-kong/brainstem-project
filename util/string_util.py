"""
util/string_util.py

This module is responsible for providing functions that can be used to
manipulate strings.
"""

# Imports
from typing import Tuple
from difflib import SequenceMatcher


def get_most_alike_from_list(string: str, strings: list[str]) -> str:
    """
    Returns the string from the list that is most alike to the input string.

    :param string:
    :param strings:
    :return:
    """

    return max(strings, key=lambda s: SequenceMatcher(None, string, s).ratio() if SequenceMatcher(None, string, s).ratio() > 0.5 else 0)

