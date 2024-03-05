"""
drivers/main.py

Defines a parent class for the drivers of the program.
"""

# Imports
from typing import Optional
from util.input import Print

# Config
from config.main import Config
from providers.data.main import Data

class Driver():
    config: Optional[Config] = None
    data_driver: Optional[Data] = None
    
    def __init__(self, config: Config, data_driver: Optional[Data]):
        self.config = config
        self.data_driver = data_driver
        self.init()
        
    def init(self):
        print(Print.bold(Print.green("Initializing the driver...")))
    
    def run(self):
        raise NotImplementedError("The run method must be implemented by the subclass.")
    