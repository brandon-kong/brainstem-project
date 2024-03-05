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

from util.directory_cache import DirectoryCache
from util.cache import Cache
from util.input import Print, user_input
from util.data import get_csv_file

# Constants
from util.constants import DATA_SETS

# Config
from config.main import Config


class Data:
    config: Config = None
    data_cache: DirectoryCache = DirectoryCache()

    def __init__(self, config=None):
        self.config = config
        self.init()

    def init(self):
        print(Print.bold(Print.yellow("\nInitializing the data pipeline...")))

        # Load commonly used data into the cache
        self.load_data_recursive(DATA_SETS, self.data_cache)

        print(Print.bold(Print.green(f"Data pipeline initialized with {Print.underline(str(len(self.data_cache)))} data sets.")))

    def run(self):
        print(Print.bold(Print.green("\nRunning the data pipeline...")))

        # Run the data pipeline

        print("Which data set would you like to load?")
        self.print_data()

        choice = user_input("text", "Enter the name of the data set: ")

        while not self.data_cache.has(choice) or isinstance(self.data_cache.get(choice), dict):
            print(Print.bold(Print.red(f"Data set {choice} not found.")))
            choice = user_input("text", "Enter the name of the data set: ")   

        print(Print.bold(Print.green(f"Loading {choice}...")))

        dataset = self.data_cache.get(choice)

        if dataset is not None:
            print(dataset.head())

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
                loaded_data = get_csv_file(value)
                if loaded_data is not None:
                    cache.set('/'.join(keys + [key]), loaded_data)

    def print_data(self):
        """
        Print the data in the cache in a tree-like structure.

        :return:
        """

        print(Print.bold(Print.green("\nData Cache:")))

        self.data_cache.print_tree()

