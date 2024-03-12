"""
visualization/plotly.py

This module is responsible for providing the Plotly visualization engine for the
application.
"""
from typing import List

from pandas import DataFrame

# Imports
from drivers.clustering.clusterer import Clusterer

# Constants
from util.constants import (
    CAN_CLUSTER,
    CLUSTER_LABEL_COLUMN_PREFIX,
    KMEANS_SEED
)

# Utilities
from util.input import get_choice_input, get_comma_separated_int_input, get_yes_no_input

from util.data import (
    get_data_properties,
    remove_non_gene_columns,
    combine_data,
    has_1465_rows
)

from util.print import (
    error,
    info
)

# SciKit-Learn
from sklearn.cluster import KMeans as KMeansClusterer


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

            cluster_k_values.sort()

            new_data = self.cluster(dataset, cluster_k_values)
            new_data = combine_data(removed_columns, new_data)

            if has_1465_rows(new_data):
                # get NonGeneColumns
                non_gene_columns = self.data_driver.data_cache.get("NonGeneColumns")
                if non_gene_columns is not None:
                    new_data = combine_data(non_gene_columns, new_data)


            print(new_data.head())

            self.data_driver.ask_to_save_data_in_memory(new_data)

            cluster_more = get_yes_no_input("Would you like to cluster more data with KMeans?")

            if not cluster_more:
                return

    def cluster(self, data: DataFrame, ks: List[int]) -> DataFrame:
        """
        Clusters the data using KMeans.

        :param data: The data to cluster.
        :param k: The number of clusters to create.
        """
        new_df = DataFrame()

        for k in ks:
            kmeans = KMeansClusterer(n_clusters=k, random_state=KMEANS_SEED)
            labels = kmeans.fit_predict(data)

            print(labels)

            new_df[f"{CLUSTER_LABEL_COLUMN_PREFIX}{k}"] = labels

        # Combine the data
        data = combine_data(new_df, data)

        return data

