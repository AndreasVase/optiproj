
'''
This file defines a class case, which is one instance of the Warehouse location problem with I warehouses and J stores.
'''

# Importing the required libraries
import random as rd
from shapely.geometry import Polygon, Point
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as mplPolygon
import numpy as np
from scipy.spatial.distance import euclidean
import time
# Importing the required functions
from enums import Zone
from Location import Location
from Config import Config

class Case:
    def __init__(self):
        timestamp = int(time.time())
        rd.seed(timestamp)
        self.costinstallation = rd.randint(1000, 4000)
        self.cv = None # Cantidad en zona verde
        self.cc = None # Cantidad en zona celeste
        self.locations = []
        self.I_locations = []
        self.J_locations = []
        self.distances = []
        self.emissions = []
        self.cost = []
        # Coordinates to the potential location for the warehouse
        # Define the coordinates of the three original zones
        self.celeste_coords = [(0, 0), (0, 600), (600, 600), (600, 0)]
        self.verde_coords = [(100, 100), (100, 500), (500, 500), (500, 100)]
        self.tiendas_coords = [(300 - 75 , 300 - 75 ), (300 - 75, 300 + 75), (300 + 75, 300 + 75), (300 + 75, 300 - 75)]
        # Create polygons for the original zones
        self.celeste_polygon = Polygon(self.celeste_coords)
        self.verde_polygon = Polygon(self.verde_coords)
        self.tiendas_polygon = Polygon(self.tiendas_coords)

        # Define the coordinates for the smaller zones within Celeste
        celeste_zones = [
            [(0, 0), (0, 300), (300, 300), (300, 0)],
            [(0, 300), (0, 600), (300, 600), (300, 300)],
            [(300, 0), (300, 300), (600, 300), (600, 0)],
            [(300, 300), (300, 600), (600, 600), (600, 300)],
        ]

        # Create polygons for the smaller zones within Celeste
        self.celeste_subpolygons = [Polygon(coords) for coords in celeste_zones]

        # Define the coordinates for the smaller zones within Verde
        verde_zones = [
            [(100, 100), (100, 300), (300, 300), (300, 100)],
            [(100, 300), (100, 500), (300, 500), (300, 300)],
            [(300, 100), (300, 300), (500, 300), (500, 100)],
            [(300, 300), (300, 500), (500, 500), (500, 300)],
        ]

        # Create polygons for the smaller zones within Verde
        self.verde_subpolygons = [Polygon(coords) for coords in verde_zones]

        # Define the coordinates for the smaller zone within Tiendas
        tiendas_zone = [(250, 250), (250, 400), (400, 400), (400, 250)]

        # Create a polygon for the smaller zone within Tiendas
        self.tiendas_subpolygon = Polygon(tiendas_zone)
    
    def generate_locations(self, I, J):
        # Generate I locations inside Celeste or Verde
        self.cv = rd.randint(2, int(J/4))
        self.cc = rd.randint(int(J/4), int(J/2))
        while len(self.I_locations) < I:
            subzone = rd.choice(self.celeste_subpolygons + self.verde_subpolygons)
            x = rd.uniform(subzone.bounds[0], subzone.bounds[2])
            y = rd.uniform(subzone.bounds[1], subzone.bounds[3])
            location = Location(x, y)
            location.determine_zone(self.celeste_polygon, self.verde_polygon, self.tiendas_polygon)
            location.determine_capacity(self.cv, self.cc)
        
            if location.zone in (Zone.CELESTE, Zone.VERDE):
                self.I_locations.append(location)

        # Generate J locations inside Tiendas
        while len(self.J_locations) < J:
            x = rd.uniform(self.tiendas_subpolygon.bounds[0], self.tiendas_subpolygon.bounds[2])
            y = rd.uniform(self.tiendas_subpolygon.bounds[1], self.tiendas_subpolygon.bounds[3])
            location = Location(x, y)
            location.determine_zone(self.celeste_polygon, self.verde_polygon, self.tiendas_polygon)
            location.determine_capacity(self.cv, self.cc)
            if location.zone == Zone.TIENDAS:
                self.J_locations.append(location)

        # Combine I and J locations into self.locations
        self.locations = self.I_locations + self.J_locations

    def getMap(self):
        # Create a grid for visualization
        fig, ax = plt.subplots()

        # Define polygons for the zones
        celeste_patch = mplPolygon(self.celeste_coords, edgecolor='blue', facecolor='none', lw=2)
        verde_patch = mplPolygon(self.verde_coords, edgecolor='green', facecolor='none', lw=2)
        tiendas_patch = mplPolygon(self.tiendas_coords, edgecolor='red', facecolor='none', lw=2)

        # Add the polygons to the plot
        ax.add_patch(celeste_patch)
        ax.add_patch(verde_patch)
        ax.add_patch(tiendas_patch)

        # Plot the locations
        location_colors = {
            Zone.CELESTE: 'blue',
            Zone.VERDE: 'green',
            Zone.TIENDAS: 'red',
        }

        for location in self.locations:
            assert self.locations is not None, "You must generate locations first"
            x, y = location.x, location.y
            zone_color = location_colors.get(location.zone, 'gray')
            ax.scatter(x, y, color=zone_color, s=50, label=str(location))

        # Set axis limits
        ax.set_xlim(0, 600)
        ax.set_ylim(0, 600)
        
        # Add legend outside the plot box
        legend_labels = [f"{zone.name}: {zone.value}" for zone in Zone]
        legend = ax.legend(labels=legend_labels, loc='upper left', bbox_to_anchor=(1, 1))
        legend.set_title("Zones")

        # Count the number of locations in each zone
        count_celeste_verde = sum(1 for location in self.locations if location.zone in (Zone.CELESTE, Zone.VERDE))
        count_tiendas = sum(1 for location in self.locations if location.zone == Zone.TIENDAS)

        # Add label to diplay count_celeste_verde and count_tiendas
        ax.text(0.5, 1.1, f"I = {count_celeste_verde}, J = {count_tiendas}", transform=ax.transAxes, horizontalalignment='center')

        # Show the plot
        plt.grid()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
    
    def printCase(self):
        print(f"Locations:")
        for location in self.locations:
            print(location.__str__())

    def determineDistance(self):
        # Making a function to determine the distance between all the points in self.location and appending it to a self.distances
        # Convert filtered locations to numpy arrays for efficient distance calculation
        I_locations_array = np.array([(location.x, location.y) for location in self.I_locations])
        J_locations_array = np.array([(location.x, location.y) for location in self.J_locations])

        for i in range(len(self.I_locations)):
            distances_i = []
            for j in range(len(self.J_locations)):
                distance = euclidean(I_locations_array[i], J_locations_array[j])
                distances_i.append(distance)
            self.distances.append(distances_i)
        return self.distances

    def printDistances(self):
        print(f"Distances:")
        for i in range(len(self.I_locations)):
            for j in range (len(self.J_locations)):
                print(f"I:{i} J:{j} d: {self.distances[i][j]}")
    
    def determineEmissions(self):
        # Making a function to determine the emissions between all the points in self.location and appending it to a self.emissions
        for i in self.distances:
            emissions_i = []
            for d in i:
                emission = d*1.5 + rd.randint(20, 70) # Emisiones per operacion
                emissions_i.append(emission)
            self.emissions.append(emissions_i)
        return self.emissions
    
    def printEmissions(self):
        print(f"Emissions:")
        for i in range(len(self.I_locations)):
            for j in range (len(self.J_locations)):
                print(f"I:{i} J:{j} e: {self.emissions[i][j]}")

    def determineCost(self):
        # Making a function to determine the cost between all the points in self.location and appending it to a self.cost
        for i in range(len(self.I_locations)):
            cost_i = []
            for j in range (len(self.J_locations)):
                if (self.I_locations[i].zone == Zone.CELESTE or self.I_locations[i].zone == Zone.VERDE):
                    cost_i.append(1.25 * self.distances[i][j] + self.costinstallation)
                else:
                    raise ValueError("Invalid zone")
            self.cost.append(cost_i)
        return self.cost

    def printCost(self):
        print(f"Cost:")
        for i in range(len(self.I_locations)):
            for j in range (len(self.J_locations)):
                print(f"I:{i} J:{j} c: {self.cost[i][j]}")
    
    def printCapacity(self):
        # Making a function to determine the capacity between all the points in self.location and appending it to a self.cost
        i = 0
        print(f"Capacity:")
        for location in self.locations:
            print(f"Location {i}, Zone: {location.zone.name}, capacity: {location.capacity}")
            i += 1
        
