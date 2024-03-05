"""
util/cache.py

This module is responsible for providing a cache data
structure that can be used to store and retrieve data
"""

# Imports
from typing import Any, Optional

# Constants
from util.constants import CACHE_SIZE
from util.input import Print

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
    clear_except(keys: list[str])
        Clears the cache except for the specified keys.
    remove(key: str)
        Removes the key from the cache.
    items()
        Gets the items in the cache.
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
    
    def get_all(self) -> dict[str, Any]:
        """
        Gets all the values from the cache.

        :return: A dictionary of all the key-value pairs in the cache.
        """

        return self.cache

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

    def clear_except(self, keys: list[str]):
        """
        Clears the cache except for the specified keys.

        :param keys:
        :return:
        """

        for key in list(self.cache.keys()):
            if key not in keys:
                self.cache.pop(key)

    def remove(self, key: str):
        """
        Removes the key from the cache.

        :param key:
        :return:
        """

        if self.has(key):
            self.cache.pop(key)

    def items(self):
        """
        Gets the items in the cache.

        :return: The items in the cache.
        """

        return self.cache.items()

    def print_tree(self):
        """
        Print the cache in a tree-like structure. It
        is slash-separated. For example, if the cache
        has a key "a/b/c" with value "value", it will
        be printed as:

        a
        |
        |--- b
        |    |
        |    |--- c: value

        :return:
        """

        self.print_tree_recursive(self.cache)

    def print_tree_recursive(self, data: dict[str, Any], level: int = 0):
        """
        Print the cache in a tree-like structure recursively.
        They are slash-separated. For example, if the cache
        has a key "a/b/c" with value "value", it will
        be printed as:

         a
        |
        |--- b
        |    |
        |    |--- c: value

        :param data:
        :param level:
        :return:
        """

        for key, value in data.items():
            if isinstance(value, dict):
                print(Print.cyan("\t" * level + key))
                self.print_tree_recursive(value, level + 1)
            else:
                # see if key is splittable
                if "/" in key:
                    new_key = key.split("/")[0]

                    # print the key
                    print(Print.cyan("\t" * level + new_key))

                    # recurse through the rest of the key
                    self.print_tree_recursive({"/".join(key.split("/")[1:]): value}, level + 1)




    def count(self):
        """
        Gets the number of items in the cache.

        :return: The number of items in the cache.
        """

        return len(self.cache)

    def __len__(self):
        return self.count()

    # Aliases
    add = set
    exists = has