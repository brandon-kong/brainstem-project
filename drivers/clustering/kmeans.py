"""
visualization/plotly.py

This module is responsible for providing the Plotly visualization engine for the
application.
"""
from pandas import DataFrame

# Imports
from drivers.clustering.clusterer import Clusterer

# Constants
from util.constants import (
    STRUCTURE_IDS,
    STRUCTURE_ID_COLORS,
    STRUCTURE_IDS_COLUMN,
    HAS_XYZ,
CAN_CLUSTER,
    WAYS_TO_VISUALIZE,
    HAS_STRUCTURE_IDS
)

# Utilities
from util.input import get_choice_input, get_comma_separated_int_input, get_yes_no_input

from util.data import (
    get_data_properties,
    remove_non_gene_columns
)

from util.print import (
    error,
    info
)

# Plotly
import plotly.express as px
import plotly.graph_objects as go


class KMeans(Clusterer):
    """
    A class that represents the KMeans clustering engine.

    Attributes
    ----------
    clusterer : Clusterer
        The clusterer instance.

    Methods
    -------
    __init__(clusterer: Clusterer)
        Initializes the KMeans engine.
    run()
        Runs the KMeans engine.
    """

    clusterer: Clusterer

    def __init__(self, clusterer: Clusterer):
        self.clusterer = clusterer
        super().__init__(clusterer.config, clusterer.data_driver)

    def run(self):
        """
        Runs the KMeans engine.
        """
        print(info("Running the KMeans engine."))

        while True:
            dataset = self.retrieve_dataset()

            if dataset is None:
                return

            # Strip the dataset of non-genetic columns
            dataset, removed_columns = remove_non_gene_columns(dataset)

            properties = get_data_properties(dataset)

            if not properties[CAN_CLUSTER]:
                print(error("This dataset cannot be clustered."))
                continue

            cluster_k_values = get_comma_separated_int_input("Enter the list of K values to cluster: ")

            if not cluster_k_values:
                continue

            wants_to_visualize = get_yes_no_input("Would you like to visualize the clusters?")

            for k in cluster_k_values:
                self.cluster(dataset, k)

            cluster_more = get_yes_no_input("Would you like to cluster more data with KMeans?")

            if not cluster_more:
                return

    def cluster(self, data: DataFrame, k: int):
        """
        Clusters the data using KMeans.

        :param data: The data to cluster.
        :param k: The number of clusters to create.
        """
        print(info(f"Clustering the data using KMeans with k={k}."))
