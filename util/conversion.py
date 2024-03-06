"""
util/conversion.py

This module is responsible for providing functions that can be used to
convert units and data types.
"""


def byte_to_mb(byte: int) -> float:
    """
    Converts bytes to megabytes.

    :param byte:
    :return:
    """

    return byte / 1024 / 1024
