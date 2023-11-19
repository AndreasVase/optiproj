
'''
This file defines a class Config, which will define the configuration for the project, based on the task description "Proyecto_FIO_OPTI_2023S2_v4.pdf"
'''
# Importing the required libraries
from shapely.geometry import Polygon, Point
import matplotlib.pyplot as plt
import time
import random as rd

# Importing the required classes
from enums import Zone



class Config:
    def __init__(self):
        # Config is being used to generate the 15 cases with correct instances
        self.instances = []

        # Define the list of limits, defined in "Tabla de Instancias". Each limit is a tuple of the form (x_min, x_max, y_min, y_max)
        self.limitsInstances = [
            (3, 6, 11, 20),
            (7, 11, 11, 20),
            (12, 15, 11, 20),
            (12, 15, 20, 29),
            (15, 18, 20, 29),
            (19, 23, 20, 29),
            (19, 23, 26, 35),
            (24, 28, 26, 35)
        ]
        
    def setInstances(self):
        # Making a list of tuples based on the limits from limitsInstances, in our case 15 instances from Tabla de Instancias

        # Making sure that we get random numbers each time we run the program
        rd.seed(3)

        # Generate random (x, y) pairs for each limit
        for limit in self.limitsInstances:
            x_min, x_max, y_min, y_max = limit
            x = rd.randint(x_min, x_max)
            y = rd.randint(y_min, y_max)
            self.instances.append((x, y))

