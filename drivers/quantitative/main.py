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
    STRUCTURE_IDS_COLUMN,
    STRUCTURE_IDS,
    STRUCTURE_ID_ABBREVIATIONS,
)

# Utilities
from util.input import user_input, get_choice_input, extract_k_value

from util.print import (
    bold,
    primary,
    underline,
    error,
    warning,
    success,
    info
)

from util.brainscan import brainScan

from util.data import (
    get_data_properties,
    get_all_cluster_id_columns
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

        while True:
            actions = {}

            dataset = self.data_driver.retrieve_dataset()

            # get the properties of the dataset

            if dataset is None:
                break

            properties = get_data_properties(dataset)

            if properties[HAS_CLUSTER_IDS] and properties[HAS_STRUCTURE_IDS]:
                actions["Analyze cluster compositions"] = self.analyze_cluster_compositions

            actions["Brain Scan"] = self.brainscan

            ans, ans_str, did_go_back = get_choice_input(
                "How would you like to analyze this dataset: ",
                list(actions.keys()),
                can_go_back=True
            )

            if did_go_back:
                return

            actions[ans_str](dataset)

        print(success("Clusterer finished."))

    def brainscan(self, dataset: DataFrame = None):
        brainScan(dataset)

    def analyze_cluster_compositions(self, dataset: DataFrame = None):
        if dataset is None:
            return

        print(info("Analyzing cluster compositions..."))

        cluster_id_columns = get_all_cluster_id_columns(dataset)

        if len(cluster_id_columns) == 0:
            print(error("No cluster columns found."))
            return

        print(info("Cluster columns found:"))

        for col in cluster_id_columns:
            print(f" - {col}")

        # for each cluster column, count the occurrences of each cluster

        new_dataframes = []

        for col in cluster_id_columns:
            # get K value
            k = extract_k_value(col)

            new_df = DataFrame()

            counts = {}
            percentages = {}
            structure_ids = {}

            new_df["Cluster"] = [i for i in range(0, k)]

            for i in range(0, k):
                count = dataset[col].value_counts().get(i, 0)
                to_percentage = float(count / len(dataset))

                counts[i] = count
                percentages[i] = to_percentage

                new_structure_ids = {}

                for sid in STRUCTURE_IDS:
                    new_structure_ids[sid] = 0

                # Get the number of structure ids in the cluster
                structure_id_list = dataset[dataset[col] == i][STRUCTURE_IDS_COLUMN].values
                # each structure id should have a column in the new dataset with the count of the structure id
                for structure_id in structure_id_list:
                    new_structure_ids[structure_id] += 1

                structure_ids[i] = new_structure_ids

            new_df["Count"] = counts.values()
            new_df["Percentage"] = percentages.values()

            for sid in STRUCTURE_IDS:
                new_df[STRUCTURE_ID_ABBREVIATIONS[sid]] = [structure_ids[i][sid] for i in range(0, k)]

            new_dataframes.append(new_df)

            print(f"Composition for K = {k}")
            print(new_df.head())

            self.data_driver.ask_to_save_data_in_memory(new_df)

        print(success("Cluster compositions analyzed."))

