""" main.py

This is the main entry point for the application. It drives the program by
offering users a menu of options to choose from when interacting with the data
and algorithms that we implemented from the research we conducted in

Machine-Learning in Brainstem Orofacial Motor Behaviors.

"""

# Imports
import util.data
from util.input import user_input

def main():

    # Program loop

    while True:
        print("Welcome to the Brainstem Orofacial Motor Behaviors program.")
        print("Please choose from the following options:")
        print("1. Load data")
        print("2. Display data")
        print("3. Cluster data")
        print("4. Exit")

        choice = user_input("text",
                            "Enter the number of your choice: ",
                            choices=["Perform K-Means", "Generate a Dataset", "Visualize a Dataset", "Exit"])

        if choice == 1:
            print("K-Means")
        elif choice == 2:
            print("Generate a Dataset")
        elif choice == 3:
            print("Visualize a Dataset")
        elif choice == 4:
            process.exit(0)





if __name__ == "__main__":
    main()
