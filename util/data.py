"""
util/data.py

This utility module is responsible for providing functions that can be used to
interact with the data that we have collected and processed from our research.

This includes getting data, writing data, and manipulating data.

"""

# Imports
import pandas as pd


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

def contains_nan(data: pd.DataFrame) -> bool:
    """
    Returns True if the data contains NaN values, otherwise False.

    :param data:
    :return:
    """

    return data.isnull().values.any()

def is_gene_data(data: pd.DataFrame) -> bool:
    """
    Returns True if the data is gene data, otherwise False.

    :param data:
    :return:
    """

    return "gene" in data.columns