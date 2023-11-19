'''
This python file is the main file for the project, which will be used to run the project.

'''

# Importing the required libraries
import time
import random as rd

# Importing the required classes
from enums import Zone
from Case import Case
from Location import Location
from Config import Config

config = Config()
config.setInstances()

# Making an instance of each case and printing it
i = 1
for instance in config.instances:
    case = Case()
    case.generate_locations(instance[0], instance[1])
    print(f"Case {i}: ")
    case.printCase()
    case.determineDistance()
    case.printDistances()
    case.determineEmissions()
    case.printEmissions()
    case.determineCost()
    case.printCost()
    # case.getMap()
    case.printCapacity()
    case.toMiniZinc(filename=f"case{i}.mzn")
    print("\n")

    # Use the code below to only run one instance, for illustrative purposes
    i += 1
    if (i == 2):
        break