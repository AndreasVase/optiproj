# Importing the required libraries
import time
import random as rd

class Config:
    def __init__(self):
        # Making sure that random is random
        timestamp = int(time.time())

        rd.seed(timestamp)

        # Definicion parametros
        self.n = 100 #Numero de tiendas
        self.c = rd.randint(1000, 4000) #Costo
        self.cv = rd.randint(2, n/4) #Cantidad en zona verde
        self.cc = rd.randint(n/4, n/2) #Cantidad en zona celeste
        self.o = rd.randint(20, 70) #Costo de operacion

        # Define the boundaries for each zone
        self.zonatienda = [(225.0, 225.0), (375.0, 225.0), (375.0, 375.0), (225.0, 375.0)]
        self.zonaverde = [(100.0, 100.0), (500.0, 100.0), (500.0, 500.0), (100.0, 500.0)]
        self.zonaceleste = [(0.0, 0.0), (600.0, 0.0), (600.0, 600.0), (0.0, 600.0)]


    


