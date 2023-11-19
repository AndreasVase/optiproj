'''
This python file defines a Location class, which will be used to define locations: warehouses and shops.

'''

# Importing the required libraries
from shapely.geometry import Point

# Importing the required classes
from enums import Zone
from Config import Config
import random as rd
import time

class Location:
    def __init__(self, x, y):   
            # Coordinates to the potential location for the warehouse
            self.x = x
            self.y = y
            self.point = Point(self.x, self.y)
            self.zone = None  # Initialize the zone as None
            self.instalationcost = None
            self.capacity = None
            self.emission = rd.randint(20, 70)


    def determine_zone(self, celeste_polygon, verde_polygon, tiendas_polygon):
        point = Point(self.x, self.y)
        in_celeste = celeste_polygon.contains(point)
        in_verde = verde_polygon.contains(point)
        in_tiendas = tiendas_polygon.contains(point)

        if in_tiendas:
            self.zone = Zone.TIENDAS
        elif in_celeste and in_verde:
            self.zone = Zone.VERDE
        elif in_celeste:
            self.zone = Zone.CELESTE
        else:
            raise Exception("All locations need to have a zone")
    
    def determine_instalationcost(self, cv, cc):
        if self.zone == Zone.VERDE:
            self.instalationcost = cv
        elif self.zone == Zone.CELESTE:
            self.instalationcost = cc
    
    def determine_capacity(self, capacity):
        if self.zone == Zone.VERDE or self.zone == Zone.CELESTE:
            self.capacity = capacity
        elif self.zone == Zone.TIENDAS:
            self.capacity = 1
    
    
        
             
    def __str__(self):
        return f"Location({self.x}, {self.y}), {self.zone.name}"