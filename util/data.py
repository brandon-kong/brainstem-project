"""
util/data.py

This utility module is responsible for providing functions that can be used to
interact with the data that we have collected and processed from our research.

This includes getting data, writing data, and manipulating data.

"""

# Imports
import pandas as pd
from numpy import bool_

# Utilities
from util.constants import NON_GENE_COLUMNS


def get_csv_file(path: str) -> pd.DataFrame | None:
    """
    Retrieves a csv file at the specified path if it exists, otherwise
    throws an error.

    :param path:
    :return:
    """

    try:
        return pd.read_csv(path, header=0, float_precision='high')
    except FileNotFoundError:
        print(f"File not found at {path}")
        return None


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

    return ("x" in data.columns and "y" in data.columns and "z" in data.columns) or \
        ("X" in data.columns and "Y" in data.columns and "Z" in data.columns)


def is_gene_data(data: pd.DataFrame) -> bool:
    """
    Returns True if the data is gene data, otherwise False.

    :param data:
    :return:
    """

    return not contains_xyz_column(data)


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


def remove_non_gene_columns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Removes non-gene columns from the data.

    :param data:
    :return:
    """

    return data.drop(columns=NON_GENE_COLUMNS)


def contains_non_gene_columns(data: pd.DataFrame) -> bool:
    """
    Returns True if the data contains non-gene columns, otherwise False.

    :param data:
    :return:
    """

    return all(column in data.columns for column in NON_GENE_COLUMNS)
