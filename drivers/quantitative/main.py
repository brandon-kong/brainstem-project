"""
quantitative/main.py

This module is responsible for initiating the quantitative pipeline for the
application.

"""

# Imports
from pandas import DataFrame
from time import sleep

from drivers.main import Driver
from providers.data import Data

# Constants
from util.constants import (
    CLUSTER_LABEL_COLUMN_PREFIX,
    HAS_STRUCTURE_IDS,
    HAS_CLUSTER_IDS,
)

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

from util.data import (
    get_data_properties,
)


class Quantitative:
    def __init__(self, config=None, data_driver: Data = None):
        self.config = config
        self.data_driver = data_driver
        self.init()

    def init(self):

        print(info("Initializing the Quantitanator..."))

        sleep(1)

        print(success("Quantitanator initialized."))

    def run(self):
        print(info("Running the Quantitanator..."))

        def analyze_cluster_compositions(dataset_x: DataFrame = None):
            if dataset_x is None:
                return

            print(info("Analyzing cluster compositions..."))

            cluster_id_columns = self.get_all_cluster_id_columns(dataset_x)

            if len(cluster_id_columns) == 0:
                print(error("No cluster columns found."))
                return

            print(info("Cluster columns found:"))

            for col in cluster_id_columns:
                print(f" - {col}")

            # for each cluster column, count the occurrences of each cluster

            new_dataframes = []

            for col in cluster_id_columns:
                # get the K value
                new_df = DataFrame()

                k = int(col.replace(CLUSTER_LABEL_COLUMN_PREFIX, ""))

                counts = {}

                for i in range(0, k):
                    count = dataset_x[col].value_counts().get(i, 0)
                    print(f"Cluster {i} count: {count}")

                    counts[i] = count

                new_df[col] = counts.keys()

        while True:

            actions = {
                "Analyze cluster compositions": analyze_cluster_compositions,
            }

            dataset = self.data_driver.retrieve_dataset()

            # get the properties of the dataset

            if dataset is None:
                break

            properties = get_data_properties(dataset)

            if HAS_CLUSTER_IDS not in properties:
                actions["Analyze cluster compositions"] = None

            ans, ans_str, did_go_back = get_choice_input(
                "How would you like to analyze this dataset: ",
                list(actions.keys()),
                can_go_back=True
            )

            if did_go_back:
                return

            actions[ans_str](dataset)

        print(success("Clusterer finished."))

    def get_all_cluster_id_columns(self, dataset):
        return [col for col in dataset.columns if col.startswith(CLUSTER_LABEL_COLUMN_PREFIX)]