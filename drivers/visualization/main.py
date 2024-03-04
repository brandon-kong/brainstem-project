"""
visualization/main.py

This module is responsible for initiating the visualization pipeline for the
application.

"""

# Imports
from util.input import Print, user_input


# Constants

engines = ["matplotlib", "plotly", "seaborn"]

class Visualizer:
    engine = "matplotlib"

    def __init__(self):
        self.init()

    def init(self):
        print(Print.bold(Print.green("\nInitializing the visualizer...\n")))

        choice: int | None = None

        while not choice:
            choice = user_input("list",
                                "Which visualization engine would you like to use: ",
                                choices=engines)

            self.engine = engines[choice - 1]

        print(Print.bold(Print.green(f"\nVisualizer initialized with {Print.underline(self.engine)}.")))
