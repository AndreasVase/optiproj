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
case = Case()
case.generate_locations(5, 6)
case.printCase()