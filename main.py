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
    #case.printCase()
    case.determineDistance()
    #case.printDistances()
    case.determineEmissions()
    #case.printEmissions()
    case.determineCost()
    #case.toMiniZinc()
    #case.printCost()
    #case.getMap()
    #case.printCapacity()
    case.toMiniZinc(filename=f"case{i}.mzn")
    time.sleep(1) # Sleep for 1 seconds to make sure that the seed is different
    i += 1
    print("\n")
    

    # # Use the code below to only run one instance, for illustrative purposes
    # if (i == 2):
    #     break