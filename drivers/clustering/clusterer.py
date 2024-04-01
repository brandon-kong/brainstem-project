"""
drivers/visualization/visualizer.py

This module is responsible for providing the Visualizer class
for the engines.
"""

# Imports
from typing import Optional, List, Tuple
from pandas import DataFrame

from util.input import (
    text_input,
    get_text_input_with_back
)

from util.print import (
    error,
    warning,
    info
)

from util.string_util import get_most_alike_from_list

from providers.data import Data

class Clusterer:
    def __init__(self, config=None, data_driver: Data | None = None):
        self.config = config
        self.data_driver = data_driver

    def run(self):
        raise NotImplementedError("The run method must be implemented by the subclass.")
