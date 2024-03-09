"""
drivers/visualization/visualizer.py

This module is responsible for providing the Visualizer class
for the engines.
"""

# Imports
from typing import Optional, List, Tuple
from pandas import DataFrame

from util.input import (
    text_input,
    get_text_input_with_back
)

from util.print import (
    error,
    warning,
    info
)

from util.string_util import get_most_alike_from_list

from providers.data import Data

class Visualizer:
    def __init__(self, config=None, data_driver: Data | None = None):
        self.config = config
        self.data_driver = data_driver
        self.engine = config.get('visualization_engine')

    def run(self):
        raise NotImplementedError("The run method must be implemented by the subclass.")

    def plot_xyz_coordinates(self, data: DataFrame):
        raise NotImplementedError("The plot_xyz_coordinates method must be implemented by the subclass.")

    def visualize_clustered_data(self, data: DataFrame):
        raise NotImplementedError("The visualize_clustered_data method must be implemented by the subclass.")

    def retrieve_dataset(self) -> DataFrame | None:
        """
        Retrieve a dataset from the cache.

        :return:
        """

        while True:
            print("Which data set would you like to load?")
            self.data_driver.print_data()

            choice, did_go_back = get_text_input_with_back(
                "Enter the name of the data set you want to use for visualization: ")

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