'''
This python file is the main file for the project. It will be used to run the project. 
Param:
'''

# Importing the required libraries
import os 
import sys
import time
import random as rd

# Importing the required classes
from enums import Zone
from Location import Location
from Case import Case
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
    i += 1
    print("\n")
    if (i == 2):
        break






# for location in locations:
#     location.determine_zone(celeste_polygon, verde_polygon, tiendas_polygon)
#     print(location)
# for location in locations:
#     location.determine_zone(celeste_polygon, verde_polygon, tiendas_polygon)