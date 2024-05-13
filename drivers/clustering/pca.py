"""
clustering/pca.py

This module is responsible for providing the Plotly visualization engine for the
application.
"""
from typing import List

import numpy as np
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

from sklearn.decomposition import PCA as PCAComponent

from util.print import (
    error,
    info
)

# SciKit-Learn
from sklearn.cluster import KMeans as KMeansClusterer


class PCA(Clusterer):
    """
    A class that represents the PCA KMeans clustering engine.

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
        print(info("Running the PCA engine."))

        while True:
            dataset = self.data_driver.retrieve_dataset()

            if dataset is None:
                return

            # Strip the dataset of non-genetic columns
            dataset, removed_columns = remove_non_gene_columns(dataset)

            properties = get_data_properties(dataset)

            if not properties[CAN_CLUSTER]:
                print(error("This dataset cannot be clustered."))
                continue

            new_data = self.cluster(dataset)

            print(new_data)

            self.data_driver.ask_to_save_data_in_memory(new_data)

            cluster_more = get_yes_no_input("Would you like to cluster more data with KMeans?")

            if not cluster_more:
                return

    def cluster(self, data: DataFrame) -> DataFrame:
        """
        Clusters the data using KMeans.

        :param data: The data to cluster.
        :param k: The number of clusters to create.
        """
        new_df = DataFrame()

        num_components = min(data.shape[0], data.shape[1])

        # perform PCA
        pca = PCAComponent(n_components=num_components)
        pca.fit(data)

        # create a new DataFrame with the PCA data

        expl_var = pca.explained_variance_ratio_

        df = DataFrame(
            data=zip(range(1, len(expl_var) + 1), expl_var, expl_var.cumsum()),
            columns=['PCA', 'Explained Variance (%)', 'Total Explained Variance (%)']
        ).set_index('PCA').mul(100).round(1)

        loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

        df_loadings = DataFrame(loadings, columns=[f'PC{i}' for i in range(1, num_components + 1)], index=data.columns)

        print("LOADINGS:")
        print(df_loadings)

        while True:
            # ask the user to choose a component to print in descending order
            print(df)

            indices = list(df.index)
            choice_num, choice, did_go_back = get_choice_input("Choose a component to print in descending order: ", indices, can_go_back=True)

            if did_go_back:
                break

            component = "PC" + str(choice)

            if component is None:
                continue

            print(component)

            print(df_loadings[component].sort_values(ascending=False))

        return df_loadings
