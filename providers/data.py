"""
providers/data.py

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

# Drivers
from providers.data_suite.data_generator import DataGenerator
from util.cache import Cache

# Constants
from util.constants import (
    DATA_SETS,
    MAX_DIRECTORY_PRINT_DEPTH,
    MASTER_DATASET,
    STRUCTURE_IDS,
    SAVE_GENERATED_DATA_PATH
)

# Utilities
from util.data import (
    get_csv_file,
    contains_nan,
    column_is_gene_data,
    save_csv_file
)

from util.string_util import get_most_alike_from_list

from util.directory_cache import DirectoryCache
from util.input import Print, user_input
from util.conversion import byte_to_mb


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
        # only if the config allows it

        if self.config.get_load_genes_at_startup():
            print(Print.bold(Print.green("\nLoading gene data...\n")))
            self.load_structure_ids()
            self.load_single_genes()

        print(Print.bold(
            Print.green(f"Data pipeline initialized with {Print.underline(str(len(self.data_cache)))} data sets ("
                        f"{format(byte_to_mb(self.get_bytes()), '.2f')} MB)")))

    def run(self):
        print(Print.bold(Print.green("\nRunning the data pipeline...")))

        # Run the data pipeline

        what_to_do = user_input("list",
                                "What would you like to do: ",
                                choices=[
                                    "Generate a new dataset",
                                    "Load a dataset",
                                    "Save a dataset from memory",
                                    "List all loaded data",
                                    "Back"
                                ])

        if what_to_do == 1:
            DataGenerator(self.config, self).run()
        elif what_to_do == 2:
            dataset = self.retrieve_dataset()
            print(dataset.head())
        elif what_to_do == 3:
            self.save_data_from_memory()
        elif what_to_do == 4:
            self.print_data()
        elif what_to_do == 5:
            return

        sleep(1)
        print(Print.bold(Print.green("Data pipeline finished.")))

    def load_single_genes(self):
        # CORONAL DENSITY GENES
        cor_density_path = DATA_SETS["Coronal"]["Density"][MASTER_DATASET]
        cor_density = get_csv_file(cor_density_path)

        # For each column that is a gene, add it to the cache

        for column in cor_density.columns:
            if column_is_gene_data(column):
                self.data_cache.set(f"Coronal/Density/Genes/{column}", cor_density[column])

    def load_structure_ids(self):
        # CORONAL DENSITY GENES
        cor_density_path = DATA_SETS["Coronal"]["Density"][MASTER_DATASET]
        cor_density: DataFrame = get_csv_file(cor_density_path)

        for structure in STRUCTURE_IDS:
            isolated_structure = cor_density[cor_density["Structure-ID"] == structure]
            self.data_cache.set(f"Coronal/Density/Structure-IDs/{structure}", isolated_structure)

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

    def save_data_from_memory(self):
        """
        Save the data from memory to a file.

        :return:
        """

        print("Which data set would you like to save?")
        self.print_data()

        choice = user_input("text", "Enter the name of the data set: ")

        while not self.data_cache.has(choice) or isinstance(self.data_cache.get(choice), dict):
            # If the data set is not found, try to find the most alike data set
            all_directories = self.data_cache.get_all_directories()
            most_alike = get_most_alike_from_list(choice, all_directories)
            print(Print.bold(Print.red(f"Data set {choice} not found.")))
            print(Print.bold(Print.red(f"Did you mean {most_alike}?")))
            choice = user_input("text", "Enter the name of the data set: ")

        name_of_file = user_input("text", "Enter the name of the file to save the data set to: ")

        while name_of_file == "":
            print(Print.bold(Print.red("The name of the file cannot be empty.")))
            name_of_file = user_input("text", "Enter the name of the file to save the data set to: ")

        file_path = self.config.get_save_generate() + name_of_file + ".csv"

        print(Print.bold(Print.green(f"\nSaving data set {file_path}...")))

        dataset = self.data_cache.get(choice)
        
        save_csv_file(dataset, file_path)

        print(Print.bold(Print.green(f"Data set {choice} saved.")))

    def get_bytes(self):
        """
        Get the bytes of the cache.

        :return: The bytes of the cache.
        """

        dataframes = self.data_cache.get_leafs_values()

        byte_sum = 0
        for df in dataframes:
            mem_usage = df.memory_usage(index=True)
            if isinstance(mem_usage, int):
                byte_sum += mem_usage
            else:
                byte_sum += mem_usage.sum()

        return byte_sum
    

