"""
providers/config.py

This driver is responsible for driving the 
program by setting up basic configurations for the user
so they don't have to worry about going through the
hassle of setting up the program themselves.
"""

# Imports
import os
import json

from util.input import (
    get_choice_input,
    get_yes_no_input,
    get_text_input
)

# Constants
from util.constants import (
    VISUALIZATION_ENGINES,
    CONFIG_FILE,
    SAVE_GENERATED_DATA_PATH
)

# Utilities
from util.print import (
    bold,
    error,
    warning,
    success,
    info
)


CONFIGURATIONS: dict[
    str,
    dict[
        str,
        str | bool | list[str]
    ]
] = {
    "name": {
        "message": "What is your name? ",
        "type": "text",
        "default": None
    },
    "save_generated_data_path": {
        "message": "Where would you like to save the generated data? ",
        "type": "text",
        "default": SAVE_GENERATED_DATA_PATH
    },
    "load_genes_at_startup": {
        "message": "Would you like to load genes at startup? ",
        "type": "yes_no",
        "default": False
    },
    "visualization_engine": {
        "message": "Which visualization engine would you like to use? ",
        "type": "list",
        "choices": VISUALIZATION_ENGINES,
        "default": VISUALIZATION_ENGINES[0]
    }
}

class Config:
    def __init__(self, config_file: str = CONFIG_FILE):
        self.configs = {}
        self.config_file: str = config_file

        self.loaded = False
        self.changed = False

        self.init()

    def init(self):
        print(info("Initializing the configuration..."))

        if not Config.config_exists():
            print(warning("No configuration file found."))
            self.create_config_file()
        else:
            # Load the configuration file to get the settings
            self.load_config_file()
            print(success("Configuration loaded."))

        self.loaded = True

    def create_config_file(self):
        default_config = {}

        for key, value in CONFIGURATIONS.items():
            if key not in default_config:
                default_config[key] = value["default"]

            if value["type"] == "text":
                default_config[key] = get_text_input(value["message"], default=value["default"])

            elif value["type"] == "yes_no":
                default_config[key] = get_yes_no_input(value["message"])

            elif value["type"] == "list":
                default_config[key] = get_choice_input(
                    value["message"],
                    value["choices"],
                    can_go_back=False
                )[1]

        self.configs = default_config

        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config

    def load_config_file(self):
        with open(self.config_file, 'r') as f:
            self.configs = json.load(f)

    def get(self, key, default=None):
        return self.configs.get(key, default)

    def set(self, key, value):
        old_value = self.configs.get(key)
        self.configs[key] = value

        if old_value != value:
            self.changed = True

    def save(self):
        if not self.changed:
            return

        with open(self.config_file, 'w') as f:
            json.dump(self.configs, f, indent=4)

    @staticmethod
    def config_exists():
        return os.path.exists(CONFIG_FILE)

    def __del__(self):
        if not self.changed:
            return

        self.save()
        print(success("Configuration saved."))