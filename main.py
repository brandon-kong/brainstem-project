""" config.py

This is the main entry point for the application. It drives the program by
offering users a menu of options to choose from when interacting with the data
and algorithms that we implemented from the research we conducted in

Machine-Learning in Brainstem Orofacial Motor Behaviors.

"""

# Imports
from util.input import user_input, Print
from util.cache import Cache

# Config
from providers.config import Config

# Drivers
from drivers.visualization.main import Visualizer
from providers.data import Data

def main():
    print(Print.bold(Print.magenta("\nWelcome to the Brainstem Orofacial Motor Behaviors program.\n")))

    config = Config()
    data = Data(config)

    # drivers

    # keep a cache of the loaded drivers
    drivers_cache = Cache()

    # Add the data driver to the cache because it is always needed
    drivers_cache.set("data", data)
    
    # Program loop
    while True:        
        print(f"Please choose from the following options:\n")

        choice = user_input("list",
                            "Enter the number of your choice: ",
                            choices=[
                                "Perform K-Means", 
                                "Generate a Dataset", 
                                "Visualize a Dataset",
                                "See Data Cache",
                                "Update Configurations",
                                "Exit"])

        # New line for readability

        if choice == 1:            
            print(Print.bold(Print.green("K-Means")))
        elif choice == 2:
            drivers_cache.get("data").run()
        elif choice == 3:
            if not drivers_cache.has("visualizer"):
                drivers_cache.add("visualizer", Visualizer(config, data))

            drivers_cache.get("visualizer").run()
        elif choice == 4:
            data.print_data()
        elif choice == 5:
            # Update configs
            config.update_config_file()

            # Clear the cache of drivers except for the data driver
            drivers_cache.clear_except(['data'])

        elif choice == 6:
            print(Print.bold(Print.red("\nExiting the program. Goodbye!\n")))
            break
        
        # New line for readability
        print()


if __name__ == "__main__":
    main()
