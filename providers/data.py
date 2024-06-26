"""
providers/data.py

This module is responsible for initiating the 
data pipeline for the
application.

Data is kept in a cache and organized like a file system.
Ex: data/parent/[4k]_DenCor_No_NaN: <4.3K x 1465> DataFrame

"""


# Imports
import os
from typing import Dict
from pandas import DataFrame, Series

# Drivers
from providers.data_suite.data_generator import DataGenerator
from providers.data_suite.data_saver import DataSaver

# Constants
from util.constants import (
    DATA_SETS,
    MAX_DIRECTORY_PRINT_DEPTH,
    MASTER_DATASET,
    STRUCTURE_IDS,
)

# Utilities
from util.data import (
    get_csv_file,
    column_is_gene_data,
    save_csv_file
)

from util.string_util import get_most_alike_from_list

from util.cache import Cache
from util.directory_cache import DirectoryCache
from util.input import (
    get_choice_input,
    get_text_input,
    get_text_input_with_back,
    get_yes_no_input
)

from util.conversion import byte_to_mb

from util.print import (
    bold,
    primary,
    underline,
    error,
    warning,
    success,
    info,
    horizontal_line
)


class Data:
    def __init__(self, config=None):
        self.cache = Cache[object]()
        self.data_cache = DirectoryCache()
        self.config = config
        self.init()

    def init(self):
        print(info("Initializing the data pipeline..."))

        # Load commonly used data into the cache
        self.load_data_recursive(DATA_SETS, self.data_cache)

        # load shared data
        self.load_shared_data()

        # Now that the data is loaded, we can add individual genes into the cache
        # only if the config allows it

        if self.config.get("load_genes_at_startup"):
            print(info("Loading gene data..."))
            self.load_structure_ids()
            self.load_single_genes()

        if self.config.get('load_generated_data_at_startup'):
            print(info("Loading generated data..."))
            self.load_generated_data()

        print(
            success(f"Data pipeline initialized with {bold(str(len(self.data_cache)))}" + success(" data sets ") +
                    info("(" + format(byte_to_mb(self.get_bytes()), '.2f') + " MB)")))

    def run(self):
        print(info("Running the data pipeline..."))
        print(primary("Welcome to the data pipeline. What would you like to do with our data?"))

        # Run the data pipeline

        def generate_new_dataset():
            DataGenerator(self.config, self)

        def load_dataset():
            self.load_data_from_file()

        def unload_dataset():
            self.unload_data_from_memory()

        def index_two_dataframes():
            data1 = self.retrieve_dataset()
            data2 = self.retrieve_dataset()
            if data1 is not None and data2 is not None:
                self.index_two_dataframes(data1, data2)

        def save_dataset():
            DataSaver(self.config, self).run()

        def list_all_loaded_data():
            self.print_data()

        def import_data():
            print("Importing data from file...")
            file_path = get_text_input("Enter the path of the file: ")
            data = get_csv_file(file_path)
            if data is not None:
                self.ask_to_save_data_in_memory(data)

        ans_actions = {
            "Generate a new dataset": generate_new_dataset,
            "Load a dataset": load_dataset,
            "Unload a dataset from memory": unload_dataset,
            "Index two dataframes": index_two_dataframes,
            "Import data from file": import_data,
            "Save a dataset to file": save_dataset,
            "List all loaded data": list_all_loaded_data,
        }

        while True:
            ans_int, ans, did_go_back = get_choice_input("What would you like to do with the data pipeline: ",
                                                         choices=list(ans_actions.keys()),
                                                         can_go_back=True
                                                         )

            if did_go_back:
                break

            ans_actions[ans]()

        print(success("\nData pipeline finished."))

    def load_single_genes(self):
        # CORONAL DENSITY GENES
        cor_density_path = DATA_SETS["Coronal"]["Density"][MASTER_DATASET]
        cor_density: DataFrame = get_csv_file(cor_density_path)

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

    def load_shared_data(self):
        """
        Load shared data into the cache.

        :return:
        """

        for root, dirs, files in os.walk('data/shared'):
            for file in files:
                if file.endswith(".csv"):
                    file_path = str(os.path.join(root, file)).replace("\\", "/")
                    data = get_csv_file(file_path)
                    new_file_path = file_path.replace('data/shared/', "").replace(".csv",
                                                                                                               "")
                    self.data_cache.set(f"Shared/{new_file_path}", data)

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

        print(info(f"Data Cache ({format(byte_to_mb(self.get_bytes()), '.2f')} MB):\n"))
        horizontal_line()
        self.print_tree()
        horizontal_line()
        print()

    def retrieve_dataset(self) -> DataFrame | None:
        """
        Retrieve a dataset from the cache.

        :return:
        """

        while True:
            self.print_data()

            choice, did_go_back = get_text_input_with_back(
                "Enter the name of the data set you want to use: ")

            if did_go_back:
                return None

            while not self.data_cache.has(choice) or isinstance(self.data_cache.get(choice),
                                                                dict):
                # If the data set is not found, try to find the most alike data set
                all_directories = self.data_cache.get_all_directories()
                most_alike = get_most_alike_from_list(choice, all_directories)
                print(error(f"Data set {choice} not found."))
                print(warning(f"Did you mean {most_alike}?"))
                choice, did_go_back = get_text_input_with_back("Enter the name of the data set: ")

                if did_go_back:
                    return None

            print(info(f"\nLoading data set {choice}..."))

            dataset = self.data_cache.get(choice)

            # Convert to dataframe because it could raise errors
            if isinstance(dataset, Series):
                dataset = dataset.to_frame()

            print("Dataset loaded: ")
            print(dataset.head())

            return dataset

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
                print(info(" " * (level + 1) * 4 + f"<{shape[0]} x {shape[1]}> DataFrame"))

    def save_data_from_memory(self):
        """
        Save the data from memory to a file.

        :return:
        """

        print("Which data set would you like to save?")
        self.print_data()

        choice = get_text_input_with_back("Enter the name of the data set: ")

        if choice is None:
            return None

        while not self.data_cache.has(choice) or isinstance(self.data_cache.get(choice), dict):
            # If the data set is not found, try to find the most alike data set
            all_directories = self.data_cache.get_all_directories()
            most_alike = get_most_alike_from_list(choice, all_directories)
            print(error(f"Data set {choice} not found."))
            print(warning(f"Did you mean {most_alike}?"))
            choice = get_text_input("Enter the name of the data set: ")

        name_of_file, did_go_back = get_text_input_with_back("Enter the name of the file to save the data set to: ")

        while name_of_file == "":
            print(error("The name of the file cannot be empty."))
            name_of_file, did_go_back = get_text_input_with_back("Enter the name of the file to save the data set to: ")

            if did_go_back:
                return None

        file_path = self.config.get('save_generated_data_path') + name_of_file.replace(".csv", "") + ".csv"

        print(info(f"\nSaving data set {file_path}..."))

        dataset = self.data_cache.get(choice)

        save_csv_file(dataset, file_path)

        print(success(f"Data set {choice} saved.\n"))

    def load_data_from_file(self):
        """
        Load data from a file into memory.

        :return:
        """

        print("Which data set would you like to load?")

        choice, did_go_back = get_text_input_with_back("Enter the path of the data set you want to load: ")

        if did_go_back:
            return None

        if choice is None:
            return None

        while not os.path.exists(choice):
            print(error(f"File {choice} not found."))
            choice = get_text_input("Enter the path of the data set you want to load: ")

        print(info(f"\nLoading data set {choice}..."))

        data = get_csv_file(choice)

        self.ask_to_save_data_in_memory(data)

    def unload_data_from_memory(self):
        """
        Unload a data set from memory.

        :return:
        """

        print("Which data set would you like to unload?")
        self.print_data()

        choice, did_go_back = get_text_input_with_back("Enter the path of the data set you want to save: ")

        if did_go_back:
            return None

        while not self.data_cache.has(choice) or isinstance(self.data_cache.get(choice), dict):
            # If the data set is not found, try to find the most alike data set
            all_directories = self.data_cache.get_all_directories()
            most_alike = get_most_alike_from_list(choice, all_directories)
            print(error(f"Data set {choice} not found."))
            print(warning(f"Did you mean {most_alike}?"))
            choice = get_text_input("Enter the name of the data set you want to unload: ")

        print(info(f"\nUnloading data set {choice}..."))

        self.data_cache.remove(choice)

        print(success(f"Data set {choice} unloaded. ("
                      f"{format(byte_to_mb(self.get_bytes()), '.2f')} MB)\n"))

    def index_two_dataframes(self, data1: DataFrame, data2: DataFrame) -> tuple[DataFrame, DataFrame] | None:
        """
        Index two dataframes by the same index.
        Create empty rows for the missing indexes.

        :param data1:
        :param data2:
        :return:
        """

        print("First data frame:")
        print(data1.head())

        first_index_column, did_go_back = get_text_input_with_back("Enter the name of the column to index by: ")

        if did_go_back:
            return None

        print("Second data frame:")
        print(data2.head())

        # make a copy of both dataframes
        data1 = data1.copy()
        data2 = data2.copy()

        second_index_column, did_go_back = get_text_input_with_back("Enter the name of the column to index by: ")

        if did_go_back:
            return None

        """
        if first_index_column not in data1.columns or second_index_column not in data2.columns:
            print(error("The column does not exist in the data frame."))
            return self.index_two_dataframes(data1, data2)
        """

        data1.set_index(first_index_column, inplace=True)
        data2.set_index(second_index_column, inplace=True)

        data1, data2 = data1.align(data2, join='outer', axis=0)

        # add the index back as a column

        data1.reset_index(inplace=True)
        data2.reset_index(inplace=True)

        print("Data frames aligned.")
        print("First data frame:")
        print(data1.head())
        self.ask_to_save_data_in_memory(data1)
        print("Second data frame:")
        print(data2.head())
        self.ask_to_save_data_in_memory(data2)

        return data1, data2

    def load_generated_data(self):
        """
        Load generated data from a file.

        :return:
        """

        # Walk through the directory and load all the files

        for root, dirs, files in os.walk(self.config.get('save_generated_data_path')):
            for file in files:
                if file.endswith(".csv"):
                    file_path = str(os.path.join(root, file)).replace("\\", "/")
                    data = get_csv_file(file_path)
                    new_file_path = file_path.replace(self.config.get('save_generated_data_path'), "").replace(".csv", "")
                    self.data_cache.set(f"Generated/{new_file_path}", data)

    def ask_to_save_data_in_memory(self, data: DataFrame):
        """
        Ask the user if they want to save the data in memory.

        :param data:
        :return:
        """

        ans = get_yes_no_input("Would you like to save the data to memory?")

        if ans:
            self.save_data_to_memory(data)

    def save_data_to_memory(self, data: DataFrame):
        """
        Save the data to the cache.

        :param data:
        :return:
        """

        name = get_text_input("Enter the name of the data set: ")

        while name == "":
            print(error("The name of the data set cannot be empty."))
            name = get_text_input("Enter the name of the data set: ")

        self.data_cache.set(name, data)

        print(success(f"Data set {name} saved.\n"))

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
