"""
visualization/config.py

This module is responsible for initiating the visualization pipeline for the
application.

"""

# Imports
from time import sleep

from drivers.main import Driver

# Constants
from util.constants import VISUALIZATION_ENGINES as ENGINES

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

from drivers.clustering.kmeans import KMeans

class Clustering:
    def __init__(self, config=None, data_driver=None):
        self.config = config
        self.data_driver = data_driver
        self.init()

    def init(self):

        print(info("Initializing the Clusterer..."))

        sleep(1)

        print(success("Clusterer initialized."))

    def run(self):
        print(info("Running the Clusterer..."))

        def kmeans():
            kmeans = KMeans(self)
            kmeans.run()
            print(success("KMeans finished."))

        def hac():
            print(info("Running HAC..."))
            print(success("HAC finished."))

        actions = {
            "KMeans": kmeans,
            "HAC": hac
        }

        while True:

            ans, ans_str, did_go_back = get_choice_input(
                "Please select a clustering algorithm: ",
                list(actions.keys()),
                can_go_back=True
            )

            if did_go_back:
                return

            actions[ans_str]()

        print(success("Clusterer finished."))

