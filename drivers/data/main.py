"""
data/main.py

This module is responsible for initiating the 
data pipeline for the
application.

"""

# Imports
from time import sleep

from util.cache import Cache
from util.input import Print
from drivers.main import Driver

# Constants
from util.constants import DATA_SETS

class Data(Driver):
    data_cache: Cache = Cache()

    def __init__(self, config=None):
        super().__init__(config)

    def init(self):
        print(Print.bold(Print.yellow("\nInitializing the data pipeline...")))
        
        # Load commonly used data into the cache
        
        print(Print.bold(Print.green(f"Data pipeline initialized with {Print.underline(len(DATA_SETS))} data sets.")))

    def run(self):  
        print(Print.bold(Print.green("Running the data pipeline...")))
        
        # Run the visualization engine
        
        sleep(1)
        print(Print.bold(Print.green("Data pipeline finished.")))

    def get_all_loaded_data(self):
        return self.data_cache.get_all()