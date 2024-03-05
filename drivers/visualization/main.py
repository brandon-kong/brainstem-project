"""
visualization/main.py

This module is responsible for initiating the visualization pipeline for the
application.

"""

# Imports
from time import sleep

from util.input import Print
from drivers.main import Driver

# Constants
from util.constants import VISUALIZATION_ENGINES as ENGINES

class Visualizer(Driver):
    engine: str = ENGINES[0]

    def __init__(self, config=None):
        super().__init__(config)

    def init(self):
        print(Print.bold(Print.yellow("\nInitializing the visualizer...")))
        
        sleep(1)
        self.engine = self.config.get_visualization_engine()
        
        print(Print.bold(Print.green(f"Visualizer initialized with {Print.underline(self.engine)}.")))

    def run(self):  
        print(Print.bold(Print.green("Running the visualizer...")))
        
        # Run the visualization engine
        print(f"\nRunning the {self.engine} engine.")
        
        sleep(1)
        print(Print.bold(Print.green("Visualizer finished.")))