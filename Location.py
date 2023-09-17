from enums import Zone
from shapely.geometry import Point

class Location:
    def __init__(self, x, y):
            # Coordinates to the potential location for the warehouse
            self.x = x
            self.y = y
            self.point = Point(self.x, self.y)
            self.zone = None  # Initialize the zone as None

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
             self.zone = Zone.NONE

    def __str__(self):
        return f"Location({self.x}, {self.y}), {self.zone.name}"