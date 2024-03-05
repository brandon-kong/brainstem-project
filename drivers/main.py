"""
drivers/main.py

Defines a parent class for the drivers of the program.
"""

# Imports
from typing import Optional
from util.input import Print

# Config
from config.main import Config

class Driver():
    config: Optional[Config] = None
    
    def __init__(self, config: Config):
        self.config = config
        self.init()
        
    def init(self):
        print(Print.bold(Print.green("Initializing the driver...")))
    
    def run(self):
        raise NotImplementedError("The run method must be implemented by the subclass.")
    