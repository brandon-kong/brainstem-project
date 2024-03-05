"""
util/cache.py

This module is responsible for providing a cache data
structure that can be used to store and retrieve data
"""

# Imports
from typing import Any, Optional

# Constants
from util.constants import CACHE_SIZE

class Cache():
    """
    A class that represents a cache data structure.
    
    Attributes
    ----------
    cache : dict[str, Any]
        A dictionary that stores the key-value pairs.
    size : int
        The size of the cache.

    Methods
    -------
    get(key: str) -> Any
        Gets the value from the cache based on the key.
    set(key: str, value: Any)
        Sets the value in the cache based on the key.
    has(key: str) -> bool
        Checks if the cache has the key.
    clear()
        Clears the cache.
    remove(key: str)
        Removes the key from the cache.
    """
    
    cache: dict[str, Any] = {}
    size: int = CACHE_SIZE

    def __init__(self, size: Optional[int] = None):
        if size:
            self.size = size

    def get(self, key: str) -> Any:
        """
        Gets the value from the cache based on the key.

        :param key:
        :return:
        """

        return self.cache.get(key, None)

    def set(self, key: str, value: Any):
        """
        Sets the value in the cache based on the key.

        :param key:
        :param value:
        :return:
        """

        if len(self.cache) >= self.size:
            self.cache.popitem()

        self.cache[key] = value

    def has(self, key: str) -> bool:
        """
        Checks if the cache has the key.
        
        :param key:
        :return: True if the cache has the key, False otherwise.
        """

        return key in self.cache
    
    def clear(self):
        """
        Clears the cache.
        """
        
        self.cache.clear()

    def remove(self, key: str):
        """
        Removes the key from the cache.

        :param key:
        :return:
        """

        if self.has(key):
            self.cache.pop(key)

    # Aliases
    add = set
    exists = has