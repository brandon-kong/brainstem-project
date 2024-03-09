"""
visualization/plotly.py

This module is responsible for providing the Plotly visualization engine for the
application.
"""
from pandas import DataFrame

# Imports
from drivers.visualization.visualizer import Visualizer

# Constants
from util.constants import (
    HAS_XYZ,
    WAYS_TO_VISUALIZE
)

# Utilities
from util.input import user_input, get_choice_input

from util.data import (
    get_data_properties,
)

from util.print import (
    bold,
    primary,
    underline,
    error,
    warning,
    success,
    info
)

# Matplotlib
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

class Matplotlib(Visualizer):
    """
    A class that represents the Matplotlib visualization engine.

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
        super().__init__(visualizer.config, visualizer.data_driver)

    def run(self):
        """
        Runs the Matplotlib visualization engine.
        """
        print(info("Running the Matplotlib engine."))

        actions = {
            "Plot XYZ Coordinates": self.plot_xyz_coordinates
        }

        while True:
            dataset = self.retrieve_dataset()

            if dataset is None:
                return

            properties = get_data_properties(dataset)

            if not properties[HAS_XYZ]:
                print(error("This dataset does not have XYZ coordinates."))
                continue

            if properties[WAYS_TO_VISUALIZE] and "scatter_clustered" in properties[WAYS_TO_VISUALIZE]:
                actions["Visualize a CLUSTERED dataset"] = self.visualize_clustered_data

            ans_int, ans, did_go_back = get_choice_input("What would you like to do: ",
                                    choices=list(actions.keys()), can_go_back=True)

            if did_go_back:
                continue

            actions[ans](dataset)
    def plot_xyz_coordinates(self, dataset: DataFrame):
        """
        Plots XYZ coordinates.
        """

        print(info("Plotting XYZ Coordinates..."))

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(dataset['X'], dataset['Y'], dataset['Z'], c='r', marker='o')

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        plt.show()


    def visualize_clustered_data(self, dataset: DataFrame):
        """
        Visualizes a clustered dataset.
        :return:
        """

        properties = get_data_properties(dataset)

        if properties[WAYS_TO_VISUALIZE] and "scatter_clustered" in properties[WAYS_TO_VISUALIZE]:
            print(info("Visualizing a CLUSTERED dataset..."))
        else:
            print(error("This dataset cannot be visualized as a clustered dataset."))
