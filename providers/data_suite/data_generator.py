"""
visualization/config.py

This module is responsible for initiating the visualization pipeline for the
application.

"""

# Imports
from time import sleep
from typing import Optional
import pandas as pd
from pandas import DataFrame

# Constants
from util.constants import DATA_SETS

# Utilities
from util.data import (
    get_data_properties,
    remove_non_gene_columns,
)

from util.input import (
    get_choice_input,
    get_text_input_with_back,
    get_float_input
)

from util.string_util import get_most_alike_from_list
from util.print import (
    error,
    success,
    bold,
    info,
    underline,
    warning
)

# Providers
from providers.config import Config


class DataGenerator:
    config: Config = None
    data_driver = None

    def __init__(self, config=None, data_driver=None):
        self.config = config
        self.data_driver = data_driver
        self.init()

    def init(self):
        print(info("Initializing the data generator..."))

        def reduce_columns(data: DataFrame):
            print(info("Any columns that have a single value below the threshold will be removed."))
            threshold = get_float_input("Enter the threshold for column reduction: ")

            # temporarily remove non-gene columns
            data, removed_columns = remove_non_gene_columns(data)

            # iterate through the columns and remove the columns which for any row have a single value below the threshold

            def check_below_threshold(column: pd.Series):
                return column.min() < threshold

            should_drop = data.apply(check_below_threshold)
            data = data.drop(columns=should_drop[should_drop].index)

            print(data.head())

            print(success(f"Removed {len(should_drop)} columns"))

            self.data_driver.ask_to_save_data(data)

        def reduce_rows(data: DataFrame):
            pass

        actions = {
            "Reduce columns": reduce_columns,
            "Reduce rows": reduce_rows
        }

        while True:
            dataset = self.retrieve_dataset()

            # If the user went back
            if dataset is None:
                return

            print(dataset.head())

            # New line for readability
            print()

            # get the data properties of the dataset
            data_properties = get_data_properties(dataset)

            ans_int, ans, did_go_back = get_choice_input("How would you like to use your dataset: ",
                                                         choices=list(actions.keys()), can_go_back=True)

            if did_go_back:
                return

            actions[ans](dataset)

    def retrieve_dataset(self) -> DataFrame | None:
        """
        Retrieve a dataset from the cache.

        :return:
        """

        while True:
            print("Which data set would you like to load?")
            self.data_driver.print_data()

            choice, did_go_back = get_text_input_with_back(
                "Enter the name of the data set you want to use for generation: ")

            if did_go_back:
                return None

            while not self.data_driver.data_cache.has(choice) or isinstance(self.data_driver.data_cache.get(choice),
                                                                            dict):
                # If the data set is not found, try to find the most alike data set
                all_directories = self.data_driver.data_cache.get_all_directories()
                most_alike = get_most_alike_from_list(choice, all_directories)
                print(error(f"Data set {choice} not found."))
                print(warning(f"Did you mean {most_alike}?"))
                choice, did_go_back = get_text_input_with_back("Enter the name of the data set: ")

                if did_go_back:
                    return None

            print(info(f"\nLoading data set {choice}..."))

            dataset = self.data_driver.data_cache.get(choice)
            return self.data_driver.data_cache.get(choice)
