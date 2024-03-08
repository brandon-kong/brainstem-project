"""
visualization/config.py

This module is responsible for initiating the visualization pipeline for the
application.

"""

# Imports
from time import sleep

# Constants
from util.constants import DATA_SETS

# Utilities
from util.data import contains_nan
from util.input import user_input, get_choice_input, get_text_input_with_back
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

        while True:

            dataset = self.retrieve_dataset()

            # If the user went back
            if dataset is None:
                return

            print(dataset.head())

            # New line for readability
            print()

            how_to_use_dataset = get_choice_input("How would you like to use your dataset: ",
                                            choices=[
                                                "Thresholding",
                                                "Remove columns",
                                                "Remove rows",
                                            ], can_go_back=True)

            if how_to_use_dataset == 1:
                print("Thresholding")
            elif how_to_use_dataset == 2:
                print("Remove columns")
            elif how_to_use_dataset == 3:
                print("Remove rows")
            elif how_to_use_dataset == 4:
                return

    def run(self):
        print(info("Running the data generator..."))

        # Run the visualization engine
        print(f"\nRunning engine.")

        what_to_do = user_input("list",
                                "What would you like to do?",
                                choices=[
                                    "Visualize a CLUSTERED dataset",
                                    "Plot XYZ Coordinates",
                                    "Exit"
                                ])

        if what_to_do == 1:
            print(info("Visualizing a clustered dataset..."))

        sleep(1)
        print(success("Visualizer finished."))

    def retrieve_dataset(self):
        """
        Retrieve a dataset from the cache.

        :return:
        """

        while True:
            print("Which data set would you like to load?")
            self.data_driver.print_data()
            
            choice, did_go_back = get_text_input_with_back("Enter the name of the data set you want to use for generation: ")

            if did_go_back:
                return None

            while not self.data_driver.data_cache.has(choice) or isinstance(self.data_driver.data_cache.get(choice), dict):
                # If the data set is not found, try to find the most alike data set
                all_directories = self.data_driver.data_cache.get_all_directories()
                most_alike = get_most_alike_from_list(choice, all_directories)
                print(error(f"Data set {choice} not found."))
                print(warning(f"Did you mean {most_alike}?"))
                choice = user_input("text", "Enter the name of the data set: ")

            print(info(f"\nLoading data set {choice}..."))

            dataset = self.data_driver.data_cache.get(choice)
            
            # Get properties of the dataset
            if contains_nan(dataset):
                print(warning("Warning: ") + underline(warning(choice)) + warning(
                    " contains NaN values.\n"))

            return self.data_driver.data_cache.get(choice)
