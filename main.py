""" config.py

This is the main entry point for the application. It drives the program by
offering users a menu of options to choose from when interacting with the data
and algorithms that we implemented from the research we conducted in

Machine-Learning in Brainstem Orofacial Motor Behaviors.

"""

# Imports
from typing import Callable, Any

# Config
from providers.config import Config

# Drivers
from drivers.visualization.main import Visualizer
from drivers.clustering.main import Clustering
from providers.data import Data

# Utilities
from util.input import user_input, get_choice_input
from util.cache import Cache
from util.print import (
    primary,
    bold,
    error,
    warning,
    success
)


def main():
    print(bold(primary("\nWelcome to the Brainstem Orofacial Motor Behaviors program.\n")))

    config = Config()
    print()
    data = Data(config)

    # drivers

    # keep a cache of the loaded drivers
    drivers_cache = Cache()

    # Add the data driver to the cache because it is always needed
    drivers_cache.set("data", data)

    # Main program functions
    def run_kmeans():
        if not drivers_cache.has("clustering"):
            drivers_cache.add("clustering", Clustering(config, data))

        drivers_cache.get("clustering").run()

    def run_visualizer():
        if not drivers_cache.has("visualizer"):
            drivers_cache.add("visualizer", Visualizer(config, data))

        drivers_cache.get("visualizer").run()

    def update_configs():
        config.create_config_file()
        drivers_cache.clear_except(['data'])
        print(warning("Some configurations may require you to restart the program to take effect."))

    def exit_program():
        print(bold(error("Exiting the program. Goodbye!")))
        exit(0)

    # Program loop
    while True:

        actions: [Callable] = {
            "Perform K-Means": run_kmeans,
            "Open Dataset Suite": data.run,
            "Visualize Data": run_visualizer,
            "Update Configurations": update_configs,
            "Exit": exit_program
        }

        choice_num, choice, can_go_back = get_choice_input(
            "What would you like to do with our program: ",
            list(actions.keys()),
            can_go_back=False
        )

        actions[choice]()


if __name__ == "__main__":
    main()
