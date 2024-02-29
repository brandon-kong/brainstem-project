""" main.py

This is the main entry point for the application. It drives the program by
offering users a menu of options to choose from when interacting with the data
and algorithms that we implemented from the research we conducted in

Machine-Learning in Brainstem Orofacial Motor Behaviors.

"""

# Imports
import os
import util.data
from util.input import user_input, Print
from util.constants import TERMINAL_COLORS as COLORS

def main():
    Print.print_bold_magenta("\nWelcome to the Brainstem Orofacial Motor Behaviors program.\n")

    # Program loop
    while True:        
        print(f"Please choose from the following options:")

        choice = user_input("list",
                            "Enter the number of your choice: ",
                            choices=["Perform K-Means", "Generate a Dataset", "Visualize a Dataset", "Exit"])

        if choice == 1:            
            Print.print_bold_green("K-Means")
        elif choice == 2:
            Print.print_bold_green("Generate a Dataset")
        elif choice == 3:
            Print.print_bold_green("Visualize a Dataset")
        elif choice == 4:
            Print.print_bold_red("Exiting the program")
            break
        
        # New line for readability
        print()






if __name__ == "__main__":
    main()
