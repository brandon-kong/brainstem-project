"""
visualization/config.py

This module is responsible for initiating the visualization pipeline for the
application.

"""

# Imports
from time import sleep

from drivers.main import Driver

# Constants
from util.constants import VISUALIZATION_ENGINES as ENGINES

# Utilities
from util.input import Print, user_input


class DataGenerator(Driver):
    engine: str = ENGINES[0]

    def __init__(self, config=None, data_driver=None):
        super().__init__(config, data_driver)

    def init(self):
        print(Print.bold(Print.yellow("\nInitializing the visualizer...")))

        sleep(1)
        self.engine = self.config.get_visualization_engine()

        print(Print.bold(Print.green(f"Visualizer initialized with {Print.underline(self.engine)}.")))

    def run(self):
        print(Print.bold(Print.green("Running the visualizer...")))

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