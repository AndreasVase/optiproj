from shapely.geometry import Polygon, Point
from Location import Location
import matplotlib.pyplot as plt
from enums import Zone

# Importing the required libraries
import time
import random as rd

class Config:
    def __init__(self):
        #In config we will define the parameters for the problem
        # Making sure that random is random
        timestamp = int(time.time())
        rd.seed(timestamp)
        self.n = 100 #Numero de tiendas
        self.costceleste = rd.randint(1000, 1500)
        self.costverde = rd.randint(1500, 4000)
        self.cv = rd.randint(2, self.n/4) #Cantidad en zona verde
        self.cc = rd.randint(self.n/4, self.n/2) #Cantidad en zona celeste
        self.o = rd.randint(20, 70) #Emisiones por operacion
        self.instances = []

        # Define the list of limits. Each limit is a tuple of the form (x_min, x_max, y_min, y_max)
        self.limitsInstances = [
            (5, 7, 6, 10),
            (8, 12, 10, 20),
            (13, 18, 20, 30),
            (19, 23, 30, 40),
            (24, 30, 40, 50),
            (32, 38, 39, 45),
            (46, 53, 54, 65),
            (66, 72, 50, 65),
            (65, 80, 80, 95),
            (95, 110, 110, 125),
            (72, 81, 125, 145),
            (82, 91, 145, 165),
            (92, 101, 165, 185),
            (102, 111, 185, 205),
            (112, 131, 205, 225)
        ]
        
    def setInstances(self):
        # Making a list of tuples based on the limits from limitsInstances, in our case 15 instances from Tabla de Instancias

        # Making sure that random is random
        timestamp = int(time.time())
        rd.seed(timestamp)

        # Generate random (x, y) pairs for each limit
        for limit in self.limitsInstances:
            x_min, x_max, y_min, y_max = limit
            x = rd.randint(x_min, x_max)
            y = rd.randint(y_min, y_max)
            self.instances.append((x, y))
