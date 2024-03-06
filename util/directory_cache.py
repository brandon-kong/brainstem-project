"""
util/directory_cache.py

This module is responsible for providing a cache data
structure that can be used to store and retrieve data
where the key is a path and values are dictionaries or
other data structures.

"""

# Imports
from typing import Any, Optional, TypeVar, Generic

from util.cache import Cache
from util.input import Print

# Constants
from util.constants import CACHE_SIZE

T = TypeVar("T")


class DirectoryCache(Cache[T | dict[str, T]]):
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

    cache: dict[str, T] = {}
    size: int = CACHE_SIZE
    all_directories: list[str] = []  # To improve performance, we can store all the directories in a list

    def __init__(self, size: Optional[int] = None):
        super().__init__(size)
        if size:
            self.size = size

    def get(self, key: str) -> T:
        """
        Gets the value from the cache based on the key.

        :param key:
        :return:
        """

        keys = key.split("/")

        data = self.cache

        for k in keys:
            if k in data:
                data = data[k]
            else:
                return None

        return data

    def set(self, key: str, value: T):
        """
        Sets the value in the cache based on the key.

        If there is a slash in the key, it will be split
        and the value will be set in a nested dictionary.

        :param key:
        :param value:
        :return:
        """

        keys = key.split("/")
        data = self.cache

        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]

        data[keys[-1]] = value

        if len(self.cache) >= self.size:
            self.cache.popitem()

        self.compute_all_directories()

    def has(self, key: str) -> bool:
        """
        Checks if the cache has the key.
        
        :param key:
        :return: True if the cache has the key, False otherwise.
        """

        keys = key.split("/")
        data = self.cache

        for k in keys:
            if k in data:
                data = data[k]
            else:
                return False

        return True

    def remove(self, key: str):
        """
        Removes the key from the cache.

        :param key:
        :return:
        """

        keys = key.split("/")
        data = self.cache

        for k in keys[:-1]:
            if k in data:
                data = data[k]
            else:
                return

        data.pop(keys[-1])

        self.compute_all_directories()

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

    def print_tree_recursive(self, data: dict[str, T], level: int = 0):
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

        if not data or not isinstance(data, dict):
            return

        for key, value in data.items():
            print(" " * level * 4 + key)

            if isinstance(value, dict):
                self.print_tree_recursive(value, level + 1)

    def get_leafs(self) -> list[str]:
        """
        Get the leaf nodes of the cache.

        :return: The leaf nodes of the cache.
        """

        return self.get_leafs_recursive(self.cache)

    def get_leafs_recursive(self, data: dict[str, T], path: str = "") -> list[str]:
        """
        Get the leaf nodes of the cache recursively.

        :param data:
        :param path:
        :return: The leaf nodes of the cache.
        """

        leafs = []

        for key, value in data.items():
            if isinstance(value, dict):
                leafs.extend(self.get_leafs_recursive(value, f"{path}/{key}"))
            else:
                leafs.append(f"{path}/{key}")

        return leafs

    def count(self):
        return len(self.get_leafs())

    def is_leaf(self, key: str) -> bool:
        """
        Check if the key is a leaf node.

        :param key:
        :return: True if the key is a leaf node, False otherwise.
        """

        return key in self.get_leafs()

    def get_all_directories(self) -> list[str]:
        """
        Get all the directories in the cache.

        :return: All the directories in the cache.
        """

        return self.all_directories

    def compute_all_directories(self):
        """
        Get all the directories in the cache.

        :return: All the directories in the cache.
        """

        self.all_directories = self.get_all_directories_recursive(self.cache)

    def get_all_directories_recursive(self, data: dict[str, T], path: str = "") -> list[str]:
        """
        Get all the directories in the cache recursively.

        :param data:
        :param path:
        :return: All the directories in the cache.
        """

        directories = []

        for key, value in data.items():
            # Include all files and directories
            new_path = f"{path}/" if path else path
            if new_path.startswith("/"):
                new_path = new_path[1:]

            new_dir = f"{new_path}{key}"

            if not isinstance(value, dict):
                directories.append(new_dir)
            else:
                directories.extend(self.get_all_directories_recursive(value, new_dir))

        return directories

    def __len__(self):
        return self.count()
