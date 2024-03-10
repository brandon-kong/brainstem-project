"""
util/data.py

This utility module is responsible for providing functions that can be used to
interact with the data that we have collected and processed from our research.

This includes getting data, writing data, and manipulating data.

"""

# Imports
from typing import Tuple

import os
import pandas as pd
from numpy import bool_

# Utilities
from util.constants import (
    NON_GENE_COLUMNS,
    XYZ_COLUMNS,
    STRUCTURE_IDS_COLUMN,
    CLUSTER_LABEL_COLUMN_PREFIX,

    HAS_GENES,
    HAS_NON_GENES,
    HAS_XYZ,
    HAS_STRUCTURE_IDS,
    CAN_CLUSTER,
    HAS_NAN,
    CAN_VISUALIZE,
    WAYS_TO_VISUALIZE,
)


def get_csv_file(path: str) -> pd.DataFrame | None:
    """
    Retrieves a csv file at the specified path if it exists, otherwise
    throws an error.

    :param path:
    :return:
    """

    try:
        return pd.read_csv(path, header=0, float_precision='high', index_col=False)
    except FileNotFoundError:
        print(f"File not found at {path}")
        return None
    

def save_csv_file(data: pd.DataFrame, path: str) -> None:
    """
    Saves the data to a csv file at the specified path.

    :param data:
    :param path:
    :return:
    """

    # Create the directory if it doesn't exist
    new_path = path.split("/")
    new_path.pop()
    new_path = "/".join(new_path)
    os.makedirs(new_path, exist_ok=True)

    data.to_csv(path, index=False)


def column_is_gene_data(column: str) -> bool:
    """
    Returns True if the column is gene data, otherwise False.

    :param data:
    :param column:
    :return:
    """

    return column not in NON_GENE_COLUMNS


def combine_data(data: pd.DataFrame, other_data: pd.DataFrame) -> pd.DataFrame:
    """
    Combines two dataframes together.

    :param data:
    :param other_data:
    :return:
    """

    return pd.concat([data, other_data], axis=1)


def remove_non_gene_columns(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Removes non-gene columns from the data and return the new data along with the removed columns.

    :param data:
    :return:
    """

    new_data = data.copy()
    removed_columns = pd.DataFrame()

    for column in NON_GENE_COLUMNS:
        if column in new_data.columns:
            new_data = new_data.drop(columns=column)
            removed_columns[column] = data[column]

    return new_data, removed_columns


def contains_non_gene_columns(data: pd.DataFrame) -> bool:
    """
    Returns True if the data contains non-gene columns, otherwise False.

    :param data:
    :return:
    """

    return any(column in data.columns for column in NON_GENE_COLUMNS)


# Data properties

"""
- Contains NaN
- Contains XYZ
- Contains Structure-IDs
- Contains Gene Data
- Can be clustered with K-Means
- Can be visualized
- Ways to visualize [3D Scatter, 3D Scatter with Color]
- Can be quantitatively analyzed
- Contains indices
"""


def contains_nan(data: pd.DataFrame) -> bool_:
    """
    Returns True if the data contains NaN values, otherwise False.

    :param data:
    :return:
    """

    return data.isnull().values.any()


def contains_xyz_column(data: pd.DataFrame) -> bool:
    """
    Returns True if the data contains XYZ coordinates, otherwise False
    :param data:
    :return:
    """

    return all(column in data.columns for column in XYZ_COLUMNS)


def contains_structure_ids_column(data: pd.DataFrame) -> bool:
    """
    Returns True if the data contains Structure-IDs, otherwise False
    :param data:
    :return:
    """

    return STRUCTURE_IDS_COLUMN in data.columns

def can_be_clustered_with_kmeans(data: pd.DataFrame) -> bool:
    """
    Returns True if the data can be clustered with K-Means, otherwise False
    :param data:
    :return:
    """

    # NAN values cannot be clustered
    if contains_nan(data):
        return False

    return True  # TODO: Implement this


def can_be_visualized(data: pd.DataFrame) -> bool:
    """
    Returns True if the data can be visualized, otherwise False
    :param data:
    :return:
    """

    return contains_xyz_column(data)


def ways_to_visualize(data: pd.DataFrame) -> list[str]:
    """
    Returns the ways that the data can be visualized
    :param data:
    :return:
    """

    if not can_be_visualized(data):
        return []

    list_of_ways = ["scatter"]

    # See if any columns start with CLUSTER_LABEL_COLUMN_PREFIX
    if any(column.startswith(CLUSTER_LABEL_COLUMN_PREFIX) for column in data.columns):
        list_of_ways.append("scatter_clustered")

    return list_of_ways


def get_data_properties(data: pd.DataFrame) -> dict[str, bool_]:
    """
    Returns the properties of the data
    :param data:
    :return:
    """

    return {
        HAS_GENES: contains_non_gene_columns(data),
        HAS_NON_GENES: contains_non_gene_columns(data),
        HAS_XYZ: contains_xyz_column(data),
        HAS_STRUCTURE_IDS: contains_structure_ids_column(data),
        CAN_CLUSTER: can_be_clustered_with_kmeans(data),
        HAS_NAN: contains_nan(data),
        CAN_VISUALIZE: can_be_visualized(data),
        WAYS_TO_VISUALIZE: ways_to_visualize(data)
    }