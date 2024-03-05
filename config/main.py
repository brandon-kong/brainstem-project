"""
config/main.py

This driver is responsible for driving the 
rogram by setting up basic configurations for the user
so they don't have to worry about going through the
hassle of setting up the program themselves.
"""

# Imports
import os

from util.input import user_input, Print

# Constants
from util.constants import (
    VISUALIZATION_ENGINES,
    CONFIG_FILE
)

class Config():
    loaded: bool = False
    visualization_engine: str = VISUALIZATION_ENGINES[0]

    def __init__(self):
        self.init()

    def init(self):
        print(Print.bold(Print.green("Initializing the configuration...")))

        if not self.config_exists():
            self.create_config_file()
        else:
            # Load the configuration file to get the settings
            self.load_config_file()

        self.loaded = True
        

    def create_config_file(self):
        print(Print.bold(Print.yellow("Creating the configuration file...\n")))

        # Ask the user for the configuration settings
        
        self.generate_config_file()

    def load_config_file(self):
        print(Print.bold(Print.yellow("Loading the configuration file...")))

        # Read the configuration settings from the configuration file

        with open(CONFIG_FILE, "r") as file:
            lines = file.readlines()

            for line in lines:
                key, value = line.split("=")

                if key == "visualization_engine":
                    self.visualization_engine = VISUALIZATION_ENGINES[int(value) - 1]
        
        print(Print.bold(Print.green("Configuration file loaded.\n")))

    def print_config(self):
        print(Print.bold(Print.cyan("Configuration settings:")))
        print(Print.cyan(f"\tVisualization Engine: {self.visualization_engine}"))

    def generate_config_file(self):
        # Ask the user for the configuration settings
        
        visualization_engine = user_input("list",
                                          "Which visualization engine would you like to use: ",
                                          choices=[
                                              "Plotly (Recommended)",
                                              "Matplotlib",
                                              "Seaborn"
                                          ])
        
        # Write the configuration settings to the configuration file

        self.visualization_engine = VISUALIZATION_ENGINES[int(visualization_engine) - 1]

        with open(CONFIG_FILE, "w") as file:
            file.write(f"visualization_engine={visualization_engine}")

        print(Print.bold(Print.green("\nConfiguration file generated.\n")))

    def update_config_file(self):
        if not self.loaded:
            raise Exception("The configuration file has not been loaded yet.")
        
        print(Print.bold(Print.yellow("Updating the configuration file...\n")))
        # Ask the user for the configuration settings
        
        visualization_engine = user_input("list",
                                          "Which visualization engine would you like to use: ",
                                          choices=[
                                              "Plotly (Recommended)",
                                              "Matplotlib",
                                              "Seaborn"
                                          ])
        
        # Write the configuration settings to the configuration file

        self.visualization_engine = VISUALIZATION_ENGINES[int(visualization_engine) - 1]

        with open(CONFIG_FILE, "w") as file:
            file.write(f"visualization_engine={visualization_engine}")

        print(Print.bold(Print.green("\nConfiguration file updated.")))
              
    def config_exists(self):
        return os.path.exists(CONFIG_FILE)
    
    def get_visualization_engine(self):
        return self.visualization_engine