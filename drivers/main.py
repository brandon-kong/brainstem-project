"""
drivers/config.py

Defines a parent class for the drivers of the program.
"""

# Imports
from typing import Optional

# Config
from providers.config import Config
from providers.data import Data

# Utilities
from util.print import (
    info
)

class Driver:
    def __init__(self, config: Config, data_driver: Optional[Data]):
        self.config = config
        self.data_driver = data_driver
        self.init()
        
    def init(self):
        print(info("Initializing the driver..."))
    
    def run(self):
        raise NotImplementedError("The run method must be implemented by the subclass.")
    