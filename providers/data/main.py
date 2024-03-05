"""
data/main.py

This module is responsible for initiating the 
data pipeline for the
application.

Data is kept in a cache and organized like a file system.
Ex: data/parent/[4k]_DenCor_No_NaN: <4.3K x 1465> DataFrame

"""

# Imports
from typing import Dict
from time import sleep

from util.cache import Cache
from util.input import Print
from util.data import get_csv_file

# Constants
from util.constants import DATA_SETS

# Config
from config.main import Config


class Data:
    config: Config = None
    data_cache: Cache = Cache()

    def __init__(self, config=None):
        self.config = config
        self.init()

    def init(self):
        print(Print.bold(Print.yellow("\nInitializing the data pipeline...")))

        # Load commonly used data into the cache
        self.load_data_recursive(DATA_SETS, self.data_cache)

        print(Print.bold(Print.green(f"Data pipeline initialized with {Print.underline(str(len(self.data_cache)))} data sets.")))

    def run(self):
        print(Print.bold(Print.green("Running the data pipeline...")))

        # Run the data pipeline
        self.print_data()

        sleep(1)
        print(Print.bold(Print.green("Data pipeline finished.")))

    def get_all_loaded_data(self):
        return self.data_cache.get_all()

    def load_data_recursive(self, data_dict: Dict[str, any], cache, keys=None):
        if keys is None:
            keys = []
        for key, value in data_dict.items():
            if isinstance(value, dict):
                self.load_data_recursive(value, cache, keys + [key])
            else:
                cache.set('/'.join(keys + [key]), get_csv_file(value))

    def print_data(self):
        """
        Print the data in the cache in a tree-like structure.

        :return:
        """

        print(Print.bold(Print.green("\nData Cache:")))

        self.data_cache.print_tree()
