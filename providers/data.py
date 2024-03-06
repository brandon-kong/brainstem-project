"""
data/config.py

This module is responsible for initiating the 
data pipeline for the
application.

Data is kept in a cache and organized like a file system.
Ex: data/parent/[4k]_DenCor_No_NaN: <4.3K x 1465> DataFrame

"""

from time import sleep
from typing import Dict

# Imports
from pandas import DataFrame

# Config
from providers.config import Config

# Constants
from util.constants import (
    DATA_SETS,
    MAX_DIRECTORY_PRINT_DEPTH,
    MASTER_DATASET
)

# Utilities
from util.data import (
    get_csv_file,
    contains_nan,
    column_is_gene_data
)

from util.string_util import get_most_alike_from_list

from util.directory_cache import DirectoryCache
from util.input import Print, user_input


class Data:
    config: Config = None
    data_cache: DirectoryCache[DataFrame] = DirectoryCache()

    def __init__(self, config=None):
        self.config = config
        self.init()

    def init(self):
        print(Print.bold(Print.yellow("\nInitializing the data pipeline...")))

        # Load commonly used data into the cache
        self.load_data_recursive(DATA_SETS, self.data_cache)

        # Now that the data is loaded, we can add individual genes into the cache
        print(Print.bold(Print.green("\nLoading gene data...\n")))

        # CORONAL DENSITY GENES
        cor_density_path = DATA_SETS["Coronal"]["Density"][MASTER_DATASET]
        cor_density = get_csv_file(cor_density_path)

        # For each column that is a gene, add it to the cache

        for column in cor_density.columns:
            if column_is_gene_data(column):
                self.data_cache.set(f"Coronal/Density/Genes/{column}", cor_density[column])

        print(Print.bold(
            Print.green(f"Data pipeline initialized with {Print.underline(str(len(self.data_cache)))} data sets.")))

    def run(self):
        print(Print.bold(Print.green("\nRunning the data pipeline...")))

        # Run the data pipeline

        dataset = self.retrieve_dataset()
        print(dataset.head())

        # New line for readability
        print()

        how_to_use_dataset = user_input("list",
                                        "How would you like to use your dataset: ",
                                        choices=[
                                            "Thresholding",
                                            "Remove columns",
                                            "Remove rows",
                                            "Back"
                                        ])

        if how_to_use_dataset == 1:
            print("Thresholding")
        elif how_to_use_dataset == 2:
            print("Remove columns")
        elif how_to_use_dataset == 3:
            print("Remove rows")
        elif how_to_use_dataset == 4:
            return

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
        self.print_tree()

    def retrieve_dataset(self):
        """
        Retrieve a dataset from the cache.

        :return:
        """

        print("Which data set would you like to load?")
        self.print_data()

        choice = user_input("text", "Enter the name of the data set: ")

        while not self.data_cache.has(choice) or isinstance(self.data_cache.get(choice), dict):
            # If the data set is not found, try to find the most alike data set
            all_directories = self.data_cache.get_all_directories()
            most_alike = get_most_alike_from_list(choice, all_directories)
            print(Print.bold(Print.red(f"Data set {choice} not found.")))
            print(Print.bold(Print.red(f"Did you mean {most_alike}?")))
            choice = user_input("text", "Enter the name of the data set: ")

        print(Print.bold(Print.green(f"\nLoading data set {choice}...")))

        dataset = self.data_cache.get(choice)

        if contains_nan(dataset):
            print(Print.yellow("Warning: ") + Print.underline(Print.yellow(choice)) + Print.yellow(
                " contains NaN values.\n"))

        return self.data_cache.get(choice)

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

        self.print_tree_recursive(self.data_cache.cache)

    def print_tree_recursive(self, data: dict[str, DataFrame], level: int = 0):
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
                # If there are over 20 data sets, don't print them all
                if len(value) > MAX_DIRECTORY_PRINT_DEPTH:
                    print(" " * (level + 1) * 4 + f"<{len(value)} data sets>")
                else:
                    self.print_tree_recursive(value, level + 1)

            else:
                # get the properties of the DataFrame
                shape = value.shape
                print(Print.cyan(" " * (level + 1) * 4 + f"<{shape[0]} x {shape[1]}> DataFrame"))
