""" main.py

This is the main entry point for the application. It drives the program by
offering users a menu of options to choose from when interacting with the data
and algorithms that we implemented from the research we conducted in

Machine-Learning in Brainstem Orofacial Motor Behaviors.

"""

# Imports
import os
import util.data
from util.input import user_input
from util.constants import TERMINAL_COLORS as COLORS

def main():
    print(f"\n{COLORS.BOLD_MAGENTA}Welcome to the Brainstem Orofacial Motor Behaviors program.{COLORS.ENDC}\n")
    # Program loop

    while True:        
        print(f"Please choose from the following options:")

        choice = user_input("list",
                            "Enter the number of your choice: ",
                            choices=["Perform K-Means", "Generate a Dataset", "Visualize a Dataset", "Exit"])

        if choice == 1:            
            print(f"{COLORS.BOLD_GREEN}K-Means{COLORS.ENDC}")
        elif choice == 2:
            print(f"{COLORS.BOLD_GREEN}Generate a Dataset{COLORS.ENDC}")
        elif choice == 3:
            print(f"{COLORS.BOLD_GREEN}Visualize a Dataset{COLORS.ENDC}")
        elif choice == 4:
            print(f"{COLORS.BOLD_RED}Exiting the program.{COLORS.ENDC}\n")
            break
        
        print()






if __name__ == "__main__":
    main()
