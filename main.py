""" config.py

This is the main entry point for the application. It drives the program by
offering users a menu of options to choose from when interacting with the data
and algorithms that we implemented from the research we conducted in

Machine-Learning in Brainstem Orofacial Motor Behaviors.

"""

# Imports

# Config
from providers.config import Config

# Drivers
from drivers.visualization.main import Visualizer
from providers.data import Data

# Utilities
from util.input import user_input, Print
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
    data = Data(config)

    # drivers

    # keep a cache of the loaded drivers
    drivers_cache = Cache()

    # Add the data driver to the cache because it is always needed
    drivers_cache.set("data", data)
    
    # Program loop
    while True:        
        print(f"What would you like to do with our program?")

        choice = user_input("list",
                            "Enter the number of your choice: ",
                            choices=[
                                "Perform K-Means",
                                "Open Dataset Suite",
                                "Visualize Data",
                                "Update Configurations",
                                "Exit"])

        # New line for readability

        if choice == 1:            
            print(success("K-Means"))
        elif choice == 2:
            data.run()
        elif choice == 3:
            if not drivers_cache.has("visualizer"):
                drivers_cache.add("visualizer", Visualizer(config, data))

            drivers_cache.get("visualizer").run()
        elif choice == 4:
            # Update configs
            config.update_config_file()

            # Clear the cache of drivers except for the data driver
            drivers_cache.clear_except(['data'])

            print(warning("Some configurations may require you to restart the program to take effect."))

        elif choice == 5:
            print(bold(error("\nExiting the program. Goodbye!")))
            break
        
        # New line for readability
        print()


if __name__ == "__main__":
    main()
