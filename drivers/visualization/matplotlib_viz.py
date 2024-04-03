"""
visualization/matplotlib.py

This module is responsible for providing the Plotly visualization engine for the
application.
"""
from pandas import DataFrame

# Imports
from drivers.visualization.visualizer import Visualizer

# Constants
from util.constants import (
    STRUCTURE_IDS,
    STRUCTURE_ID_COLORS_MATPLOTLIB,
    STRUCTURE_IDS_COLUMN,
    HAS_XYZ,
    WAYS_TO_VISUALIZE,
    HAS_STRUCTURE_IDS, CLUSTER_LABEL_COLUMN_PREFIX
)

# Utilities
from util.input import user_input, get_choice_input, get_comma_separated_int_input, get_yes_no_input, get_formatted_input, get_text_input_with_back
from util.colors import generate_k_distinct_colors

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
from matplotlib import colormaps
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

rainbow = colormaps.get_cmap('rainbow')


def color_certain_structure_ids(dataset: DataFrame):
    """
    Colors certain structure ids while keeping the rest the same.
    :return:
    """

    print(info("Coloring certain structure ids..."))

    input_structure_ids = get_comma_separated_int_input("Enter the list of structure ids to color: ",
                                                  choices=STRUCTURE_IDS)

    # Modify the colors and opacity of the dataset
    colors = [STRUCTURE_ID_COLORS_MATPLOTLIB[sid] if sid in input_structure_ids else 'b' for sid in dataset[STRUCTURE_IDS_COLUMN]]

    # create color map



    fig = plt.figure()

    title, did_go_back = get_text_input_with_back("What would you like to title the plot?")

    if did_go_back:
        return

    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(title)
    ax.scatter(dataset['X'], dataset['Y'], dataset['Z'], c=dataset[STRUCTURE_IDS_COLUMN], marker='o')
    plt.show()


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
        Runs the Plotly visualization engine.
        """
        print(info("Running the Matplotlib engine."))

        while True:
            actions = {
                "Plot XYZ Coordinates": self.plot_xyz_coordinates
            }

            dataset = self.data_driver.retrieve_dataset()

            if dataset is None:
                return

            properties = get_data_properties(dataset)

            if not properties[HAS_XYZ]:
                print(error("This dataset does not have XYZ coordinates."))
                continue

            if properties[WAYS_TO_VISUALIZE] and "scatter_clustered" in properties[WAYS_TO_VISUALIZE]:
                actions["Visualize a CLUSTERED dataset"] = self.visualize_clustered_data

            if properties[HAS_STRUCTURE_IDS]:
                actions["Color certain Structure IDs"] = color_certain_structure_ids

            ans_int, ans, did_go_back = get_choice_input("What would you like to do: ",
                                                         choices=list(actions.keys()), can_go_back=True)

            if did_go_back:
                continue

            actions[ans](dataset)

            visualize_more = get_yes_no_input("Would you like to visualize more data?")

            if not visualize_more:
                return

    def plot_xyz_coordinates(self, dataset: DataFrame):
        """
        Plots XYZ coordinates.
        """

        print(info("Plotting XYZ Coordinates..."))

        title, did_go_back = get_text_input_with_back("What would you like to title the plot?")

        if did_go_back:
            return

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_title(title)

        ax.scatter(dataset['X'], dataset['Y'], dataset['Z'], c='b', marker='o')

        plt.show()

    def visualize_clustered_data(self, dataset: DataFrame):
        """
        Colors cluster labels in the dataset.
        :return:
        """

        print(info("Visualizing cluster labels..."))

        # get all columns that start with CLUSTER_LABEL_COLUMN_PREFIX

        cluster_label_columns = [column for column in dataset.columns if column.startswith(CLUSTER_LABEL_COLUMN_PREFIX)]

        title, did_go_back = get_text_input_with_back("What would you like to title the plot?")

        if did_go_back:
            return

        for cluster_label_column in cluster_label_columns:
            cluster_label = int(cluster_label_column.split(CLUSTER_LABEL_COLUMN_PREFIX)[1])

            options = {
                "k": str(cluster_label)
            }

            # create a new column for the color of the cluster label
            dataset['Cluster ID'] = dataset[cluster_label_column].apply(lambda x: f"{x}")

            # sort the dataset by the cluster label
            dataset = dataset.sort_values(by=cluster_label_column)

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.set_title(get_formatted_input(title, options))

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')

            scatter = ax.scatter(dataset['X'], dataset['Y'], dataset['Z'], c=dataset[cluster_label_column], cmap=rainbow, marker='o', alpha=0.6)

            fig.colorbar(scatter, ax=ax, label='Cluster ID')

            plt.show()
