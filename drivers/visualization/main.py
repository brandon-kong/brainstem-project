"""
visualization/main.py

This module is responsible for initiating the visualization pipeline for the
application.

"""

# Imports
from util.input import Print, user_input


# Constants

engines = ["matplotlib", "seaborn", "plotly"]

class Visualizer:
    software = "matplotlib"

    def __init__(self):
        pass

    def init(self):
        print(Print.bold(Print.green("Initializing the visualizer...")))

        choice = None

        while not choice:
            choice = user_input("list",
                                "Please choose a visualization library: ",
                                choices=engines)

            software = engines[choice - 1]

        print(Print.bold(Print.green(f"Visualizer initialized with {self.software}.")))
