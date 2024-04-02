
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
from util.data import contains_nan, save_csv_file
from util.input import get_text_input, get_text_input_with_back, get_choice_input, get_yes_no_input
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


class DataSaver:
    def __init__(self, config=None, data_driver=None):
        self.config = config
        self.data_driver = data_driver
        self.init()

    def init(self):
        pass

    def run(self):
        while True:
            print("Which data set would you like to save?")
            dataset = self.data_driver.retrieve_dataset()

            name_of_file, did_go_back = get_text_input_with_back("Enter the name of the file to save the data set to: ")

            if did_go_back:
                break

            while name_of_file == "":
                print(error("The name of the file cannot be empty."))
                name_of_file = get_text_input("Enter the name of the file to save the data set to: ")

            file_path = self.config.get('save_generated_data_path') + name_of_file + ".csv"

            print(info(f"\nSaving data set {file_path}..."))

            dataset = self.data_driver.data_cache.get(choice)
            save_csv_file(dataset, file_path)
            print(success(f"Data set {choice} saved.\n"))

            save_another = get_yes_no_input("Would you like to save another data set?")

            if not save_another:
                break
