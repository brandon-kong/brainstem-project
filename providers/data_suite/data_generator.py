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
from util.input import Print, user_input
from util.string_util import get_most_alike_from_list

# Providers
from providers.config import Config


class DataGenerator:
    config: Config = None
    data_driver = None

    def __init__(self, config=None, data_driver=None):
        super().__init__(config, data_driver)

    def init(self):
        print(Print.bold(Print.yellow("\nInitializing the data generator...")))

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

        print(Print.bold(Print.green(f"Visualizer initialized with {Print.underline(self.engine)}.")))

    def run(self):
        print(Print.bold(Print.green("Running the data generator...")))

        # Run the visualization engine
        print(f"\nRunning the {self.engine} engine.")

        what_to_do = user_input("list",
                                "What would you like to do?",
                                choices=[
                                    "Visualize a CLUSTERED dataset",
                                    "Plot XYZ Coordinates",
                                    "Exit"
                                ])

        if what_to_do == 1:
            print(Print.bold(Print.green("Visualizing a clustered dataset...")))

        sleep(1)
        print(Print.bold(Print.green("Visualizer finished.")))

    def retrieve_dataset(self):
        """
        Retrieve a dataset from the cache.

        :return:
        """

        print("Which data set would you like to load?")
        self.data_driver.print_data()

        choice = user_input("text", "Enter the name of the data set: ")

        while not self.data_driver.data_cache.has(choice) or isinstance(self.data_driver.data_cache.get(choice), dict):
            # If the data set is not found, try to find the most alike data set
            all_directories = self.data_driver.data_cache.get_all_directories()
            most_alike = get_most_alike_from_list(choice, all_directories)
            print(Print.bold(Print.red(f"Data set {choice} not found.")))
            print(Print.bold(Print.red(f"Did you mean {most_alike}?")))
            choice = user_input("text", "Enter the name of the data set: ")

        print(Print.bold(Print.green(f"\nLoading data set {choice}...")))

        dataset = self.data_driver.data_cache.get(choice)

        if contains_nan(dataset):
            print(Print.yellow("Warning: ") + Print.underline(Print.yellow(choice)) + Print.yellow(
                " contains NaN values.\n"))

        return self.data_driver.data_cache.get(choice)
