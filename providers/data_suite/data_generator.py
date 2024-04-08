"""
visualization/config.py

This module is responsible for initiating the visualization pipeline for the
application.

"""

# Imports
from time import sleep
from typing import Optional
import pandas as pd
from pandas import DataFrame

# Constants
from util.constants import (
    STRUCTURE_IDS,
    STRUCTURE_IDS_COLUMN,
    HAS_STRUCTURE_IDS,
    HAS_NAN, HAS_CLUSTER_IDS,
)

# Utilities
from util.data import (
    get_data_properties,
    remove_non_gene_columns,
    combine_data,
    get_all_cluster_id_columns,
    extract_k_value

)

from util.input import (
    get_choice_input,
    get_text_input_with_back,
    get_float_input,
    get_yes_no_input,
    get_comma_separated_int_input
)

from util.string_util import get_most_alike_from_list
from util.print import (
    error,
    success,
    bold,
    info,
    underline,
    warning
)

# Providers
from providers.config import Config


class DataGenerator:
    config: Config = None
    data_driver = None

    def __init__(self, config=None, data_driver=None):
        self.config = config
        self.data_driver = data_driver
        self.init()

    def init(self):
        print(info("Initializing the data generator..."))

        def reduce_columns(data: DataFrame):
            print(info("Any columns that have a single value below the threshold will be removed."))
            threshold = get_float_input("Enter the threshold for column reduction: ")

            print(info(f"Threshold set to {threshold}\n"))
            # temporarily remove non-gene columns
            data, removed_columns = remove_non_gene_columns(data)

            # iterate through the columns and remove the columns which for any row have a single value below the threshold

            def check_below_threshold(column: pd.Series):
                return column.min() < threshold

            should_drop = data.apply(check_below_threshold)
            data = data.drop(columns=should_drop[should_drop].index)

            # re-add the removed columns
            data = combine_data(removed_columns, data)

            print(data.head())

            print(success(f"Removed {len(should_drop)} columns"))

            self.data_driver.ask_to_save_data_in_memory(data)

        def reduce_rows(data: DataFrame):
            pass

        def remove_cluster_ids_where_voxel_below_threshold(data: DataFrame):
            print(info("Removing cluster ids where the voxel value is below the threshold..."))

            threshold = get_float_input("Enter the threshold for voxel value: ")

            print(info(f"Threshold set to {threshold}\n"))

            # get the number of rows before filtering
            num_rows_before = data.shape[0]

            cluster_id_columns = get_all_cluster_id_columns(data)

            # ask the user which cluster id to filter




            self.data_driver.ask_to_save_data_in_memory(data)

        def get_cluster_ids_where_voxel_below_threshold(data: DataFrame):
            print(info("Getting cluster ids where the voxel value is below the threshold..."))

            threshold = get_float_input("Enter the threshold for voxel value: ")

            print(info(f"Threshold set to {threshold}\n"))

            # get the number of rows before filtering
            num_rows_before = data.shape[0]

            cluster_id_columns = get_all_cluster_id_columns(data)

            # ask the user which cluster id to filter
            choice, cluster_id, went_back = get_choice_input("Which cluster id would you like to filter: ",
                                                       choices=cluster_id_columns, can_go_back=True)\

            if went_back:
                return

            as_k = extract_k_value(cluster_id)

            # strip the data of non-gene columns
            data, _ = remove_non_gene_columns(data)

            # add the cluster id column back
            data[cluster_id] = _[cluster_id]

            # instantiate a dictionary with range 0-k
            cluster_ids = {i: False for i in range(0, as_k)}

            # get the cluster ids where the voxel value is below the threshold
            for i in range(0, as_k):
                all_columns_below_threshold = data[data[cluster_id] == i].min() < threshold
                # remove the cluster id column
                all_columns_below_threshold = all_columns_below_threshold.drop(cluster_id)

                cluster_ids[i] = all_columns_below_threshold.any()

            # print the cluster ids where the voxel value is below the threshold

            for cluster_id_x, below_threshold in cluster_ids.items():
                print(f"Cluster ID: {str(cluster_id_x)} - Below Threshold: {below_threshold}")

        def replace_nan(data: DataFrame):
            replacement_val = get_float_input("What value would you like to replace NaN with: ")

            # get the number of nan values
            nan_count = data.isna().sum().sum()

            data = data.fillna(replacement_val)
            print(success(f"Replaced {nan_count} NaN values with {replacement_val}"))
            self.data_driver.ask_to_save_data_in_memory(data)

        def filter_structure_ids(data: DataFrame):
            print(info("Filtering data by structure ids..."))

            valid = True
            structure_ids = get_comma_separated_int_input("Enter the list of structure ids to keep: ",
                                                          choices=STRUCTURE_IDS)

            # delete rows where its structure id is not in the list

            data = data[data[STRUCTURE_IDS_COLUMN].isin(structure_ids)]
            print(data.head())
            self.data_driver.ask_to_save_data_in_memory(data)

        while True:
            actions = {
                "Reduce columns": reduce_columns,
                "Reduce rows": reduce_rows,
                "Replace NaN": replace_nan,
                "Filter structure ids": filter_structure_ids,
                "Get cluster ids where voxel below threshold": get_cluster_ids_where_voxel_below_threshold,
            }

            dataset = self.data_driver.retrieve_dataset()

            # If the user went back
            if dataset is None:
                return

            print(dataset.head())

            # get the data properties of the dataset
            data_properties = get_data_properties(dataset)

            # if the dataset doesn't have NaN, remove it as an action
            if not data_properties[HAS_NAN]:
                actions.pop("Replace NaN")

            if not data_properties[HAS_STRUCTURE_IDS]:
                actions.pop("Filter structure ids")

            if not data_properties[HAS_CLUSTER_IDS]:
                actions.pop("Get cluster ids where voxel below threshold")

            # Decide which actions the user can take with the dataset


            ans_int, ans, did_go_back = get_choice_input("How would you like to use your dataset: ",
                                                         choices=list(actions.keys()), can_go_back=True)

            if did_go_back:
                return

            actions[ans](dataset)

            do_something_else = get_yes_no_input("Would you like to generate another dataset?")

            if not do_something_else:
                return
