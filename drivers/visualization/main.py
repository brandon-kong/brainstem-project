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
from util.input import user_input, get_choice_input

from util.print import (
    bold,
    primary,
    underline,
    error,
    warning,
    success,
    info
)

from drivers.visualization.plotly import Plotly
from drivers.visualization.matplotlib import Matplotlib


class Visualizer:
    def __init__(self, config=None, data_driver=None):
        self.config = config
        self.data_driver = data_driver
        self.engine = config.get('visualization_engine')
        self.engine_instance: Visualizer | None = None

    def init(self):
        print(info("Initializing the visualizer..."))
        
        sleep(1)
        self.engine = self.config.get('visualization_engine')
        
        print(success(f"Visualizer initialized with {underline(self.engine)}."))

    def run(self):  
        print(info("Running the visualizer..."))

        if self.engine == "plotly":
            self.engine_instance = Plotly(self)
        elif self.engine == "matplotlib":
            self.engine_instance = Matplotlib(self)
        else:
            raise ValueError(f"Invalid visualization engine: {self.engine}")

        self.engine_instance.run()
        
        print(success("Visualizer finished."))

    def visualize_clustered_data(self):
        print(info("Visualizing a CLUSTERED dataset..."))

    def plot_xyz_coordinates(self):
        print(info("Plotting XYZ Coordinates..."))
