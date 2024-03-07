"""
providers/config.py

This driver is responsible for driving the 
program by setting up basic configurations for the user
so they don't have to worry about going through the
hassle of setting up the program themselves.
"""

# Imports
import os
import json

from util.input import user_input, Print

# Constants
from util.constants import (
    VISUALIZATION_ENGINES,
    CONFIG_FILE,
    SAVE_GENERATED_DATA_PATH
)

# Utilities
from util.print import (
    bold,
    error,
    warning,
    success,
    info
)


class Config:
    def __init__(self):
        self.loaded: bool = False
        self.name: str = ""
        self.save_generated_data_path: str = SAVE_GENERATED_DATA_PATH
        self.load_genes_at_startup: bool = False
        self.visualization_engine: str = ""

        self.init()

    def init(self):
        print(info("Initializing the configuration..."))

        if not self.config_exists():
            self.create_config_file()
        else:
            # Load the configuration file to get the settings
            self.load_config_file()

        self.loaded = True

    def create_config_file(self):
        print(info("Creating the configuration file...\n"))

        # Ask the user for the configuration settings

        self.generate_config_file()
        print(Print.bold(Print.green("\nConfiguration file generated.\n")))

    def load_config_file(self):
        print(info("Loading the configuration file..."))

        # Read the configuration settings from the configuration file

        with open(CONFIG_FILE, "r") as file:
            data = json.load(file)

            self.name = data["name"]
            self.load_genes_at_startup = data["load_genes_at_startup"]
            self.visualization_engine = data["visualization_engine"]

        print(success("Configuration file loaded.\n"))

    def print_config(self):
        print(Print.bold(Print.cyan("Configuration settings:")))
        print(Print.cyan(f"\tVisualization Engine: {self.visualization_engine}"))

    def generate_config_file(self):
        # Ask the user for the configuration settings

        name = user_input("text", "What is your name: ") or self.name

        save_generated_data_path = user_input("text", f"Where would you like to save any generated data (default: {self.save_generated_data_path}):") or self.save_generated_data_path

        load_genes_at_startup = user_input("list",
                                            "Would you like to load the genes at startup: ",
                                            choices=[
                                                "Yes",
                                                "No"
                                            ])

        visualization_engine = user_input("list",
                                          "Which visualization engine would you like to use: ",
                                          choices=[
                                              "Plotly (Recommended)",
                                              "Matplotlib",
                                              "Seaborn"
                                          ])

        # Write the configuration settings to the configuration file in json format

        self.name = name
        self.save_generated_data_path = save_generated_data_path
        self.load_genes_at_startup = load_genes_at_startup == 1
        self.visualization_engine = VISUALIZATION_ENGINES[int(visualization_engine) - 1]

        json_data = {
            "name": name,
            "save_generated_data_path": save_generated_data_path,
            "load_genes_at_startup": self.load_genes_at_startup,
            "visualization_engine": visualization_engine
        }

        with open(CONFIG_FILE, "w") as file:
            json.dump(json_data, file, indent=4)


    def update_config_file(self):
        if not self.loaded:
            raise Exception("The configuration file has not been loaded yet.")

        print(Print.bold(Print.yellow("Updating the configuration file...\n")))
        # Ask the user for the configuration settings

        self.generate_config_file()

        print(Print.bold(Print.green("\nConfiguration file updated.")))

    def config_exists(self):
        return os.path.exists(CONFIG_FILE)

    def get_visualization_engine(self):
        return self.visualization_engine

    def get_name(self):
        return self.name

    def get_load_genes_at_startup(self):
        return self.load_genes_at_startup
    
    def get_save_generate(self):
        return self.save_generated_data_path
