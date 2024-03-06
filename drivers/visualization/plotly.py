"""
visualization/plotly.py

This module is responsible for providing the Plotly visualization engine for the
application.
"""

# Imports
from drivers.visualization.main import Visualizer

# Constants

# Utilities
from util.input import Print, user_input

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
        print(Print.bold(Print.green("Running the Plotly engine.")))

        what_to_do = user_input("list",
                                "What would you like to do?",
                                choices=[
                                    "Visualize a CLUSTERED dataset",
                                    "Plot XYZ Coordinates",
                                    "Exit"
                                ])

        if what_to_do == 1:
            print(Print.bold(Print.green("Visualizing a clustered dataset...")))

        print(Print.bold(Print.green("Plotly engine finished.")))
