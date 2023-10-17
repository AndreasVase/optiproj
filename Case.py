
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
        if (J < 8):
            self.cv = 2
        else:
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
        numerator = 0
        for i in self.distances:
            emissions_i = []
            for d in i:
                emission = d*1.5 + self.I_locations[numerator].emission # Emisiones per operacion
                emissions_i.append(emission)
            self.emissions.append(emissions_i)
            numerator += 1
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
    
    def toMiniZinc(self, filename):
        txt = 'I = {};\nJ = {};\nC = {};\nCV = {};\nCC = {};\n'.format(len(self.I_locations), len(self.J_locations), self.costinstallation, self.cv, self.cc)
        
        Oi = []
        for i in self.I_locations:
            Oi.append(i.emission)
        txt += 'O_i = {};\n'.format(Oi)

        Vi = []
        for i in self.I_locations:
            if i.zone == Zone.VERDE:
                Vi.append(1)
            else:
                Vi.append(0)
        txt += 'V_i = {};\n'.format(Vi)
            
        txt += 'D_ij = \n['
        for i in range(len(self.I_locations)):
            txt += '|'
            for j in range(len(self.J_locations)):
                txt += str(int(self.distances[i][j]))
                if j != len(self.J_locations) - 1:
                    txt += ', '
            txt += '\n'
        txt += '|];\n'

        txt += 'E_ij = \n['
        for i in range(len(self.I_locations)):
            txt += '|'
            for j in range(len(self.J_locations)):
                txt += str(int(self.emissions[i][j]))
                if j != len(self.J_locations) - 1:
                    txt += ', '
            txt += '\n'
        txt += '|];\n\n'

        txt += '% Define sets I and J\n'
        txt += 'int: I;\n'
        txt += 'int: J;\n\n'

        # Define parameters
        txt += 'int: C; % Cost of installing a warehouse in all zones\n'
        txt += 'int: CV; % Capacity in green zone\n'
        txt += 'int: CC; % Capacity in blue zone\n\n'

        txt += 'array[1..I] of int: O_i; % Emissions per operation for each warehouse i\n'
        txt += 'array[1..I, 1..J] of int: D_ij; % Distance between warehouse i and store j\n'
        #txt += 'array[1..I, 1..J] of float: T_ij = [1.25 * D_ij[i, j] | i, j in 1..I, j in 1..J]; % Transportation cost\n' Not in use
        txt += 'array[1..I, 1..J] of int: E_ij; % Transportation emissions\n'
        txt += 'array[1..I] of int: V_i; % 1 if warehouse i is in the green zone, 0 if in the blue zone\n'

        txt += '\n% Define decision variables\n'
        txt += 'array[1..I, 1..J] of var 0..1: X; % 1 if warehouse i supplies store j, 0 otherwise\n'
        txt += 'array[1..I] of var 0..1: Y;\n\n'

        txt += '% Define constraints\n\n'

        txt += '% Add the constraint to ensure Y_i is 1 if the warehouse I supplies at least one store\n'
        txt += 'constraint forall(i in 1..I)(\n'
        txt += '  sum(j in 1..J)(X[i,j]) > 0 -> Y[i] == 1\n'
        txt += ');\n\n'

        txt += '% Emissions constraint\n'
        txt += 'constraint sum(i in 1..I, j in 1..J)(E_ij[i, j] * X[i, j]) + sum(i in 1..I)(O_i[i] * Y[i]) <= 500 * J;\n\n'

        txt += '% Assignment constraint\n'
        txt += 'constraint forall(j in 1..J)(sum(i in 1..I)(X[i, j]) == 1);\n\n'

        txt += '% Green zone capacity constraint\n'
        txt += 'constraint forall(i in 1..I)(sum(j in 1..J)(X[i, j] * V_i[i]) <= CV);\n\n'

        txt += '% Blue zone capacity constraint\n'
        txt += 'constraint forall(i in 1..I)(sum(j in 1..J)(X[i, j] * (1 - V_i[i])) <= CC);\n\n'

        txt += '% Solve the optimization problem using a solver\n'
        txt += '% Define the objective function\n'
        txt += 'solve minimize sum(i in 1..I, j in 1..J)(1.25 * D_ij[i, j] * X[i, j]) + sum(i in 1..I)(C * Y[i]);\n\n'
        txt += 'output ["Solution:", ""];\n'
        txt += 'output ["X = \\n", show2d(X), ";"];\n'
        txt += 'output ["\\n"];\n'
        txt += 'output ["Y = ", show(Y), ";"];\n'
        txt += 'output ["\\n"];\n'
        txt += 'output ["FO = ", show(sum(i in 1..I, j in 1..J)(1.25 * D_ij[i, j] * X[i, j]) + sum(i in 1..I)(C * Y[i])), \"\\n"];'
        mzn = open(filename,'w')
        mzn.write(txt)
        print(txt)
        mzn.close()

