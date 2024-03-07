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
from util.input import user_input

from util.print import (
    bold,
    primary,
    underline,
    error,
    warning,
    success,
    info
)

class Visualizer(Driver):
    engine: str = ENGINES[0]

    def __init__(self, config=None, data_driver=None):
        super().__init__(config, data_driver)

    def init(self):
        print(info("Initializing the visualizer..."))
        
        sleep(1)
        self.engine = self.config.get_visualization_engine()
        
        print(success(f"Visualizer initialized with {underline(self.engine)}."))

    def run(self):  
        print(info("Running the visualizer..."))
        
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
            print(info("Visualizing a clustered dataset..."))
        
        sleep(1)
        print(success("Visualizer finished."))
