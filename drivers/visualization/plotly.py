"""
visualization/plotly.py

This module is responsible for providing the Plotly visualization engine for the
application.
"""

# Imports
from drivers.visualization.main import Visualizer

# Constants

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

class Plotly:
    """
    A class that represents the Plotly visualization engine.

    Attributes
    ----------
    visualizer : Visualizer
        The visualizer instance.

    Methods
    -------
    __init__(visualizer: Visualizer)
        Initializes the Plotly visualization engine.
    run()
        Runs the Plotly visualization engine.
    """

    visualizer: Visualizer

    def __init__(self, visualizer: Visualizer):
        self.visualizer = visualizer

    def run(self):
        """
        Runs the Plotly visualization engine.
        """
        print(info("Running the Plotly engine."))

        what_to_do = user_input("list",
                                "What would you like to do?",
                                choices=[
                                    "Visualize a CLUSTERED dataset",
                                    "Plot XYZ Coordinates",
                                    "Exit"
                                ])

        if what_to_do == 1:
            print(info("Visualizing a clustered dataset..."))

        print(success("Plotly engine finished."))
