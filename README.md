Hi! 
To get all the packages needed to run this project, please run "pip install -r requirements.txt" or "pip3 install -r requirements.txt" in the terminal. 

This README is for describing what we have done in the project. Our task was the following:

1. Formule el Warehouse Location Problem, definiendo Conjuntos, Parámetros, Variables, Res- tricciones y Función Objetivo. Además, debe agregar una breve descripción de las restricciones y función objetivo. Comente sobre la naturaleza del problema y casos de infactibilidad.
2. Genere al menos 15 instancias de prueba factibles, 1 de cada dimensión descrita en la Tabla de Instancias. Para ello debe desarrollar una rutina en Python.
3. Explique detenidamente el proceso de generación de instancias exponiendo además cuáles fueron las consideraciones tomadas para cumplir con lo solicitado en el enunciado, lograr factibilidad y el manejo de la aleatoriedad.

To explain how we made the instances, we will look at it in a cronological order, in regards of how we worked with the project:

Instances:
First of all, we knew that we were going to make instances based on the "Tabla de Instancia", which defined the limits for I and J. To be able to make a list of all the instances, one instance for each dimention, we made a Config class which defined the information in Tabla de Instancia and generated a random number of I and J for each instances, regarding to the limits. 

Locations:
After getting our instances, we had to define locations for I and J. To do this we defined a class called Location, which contain the X and Y coordinates of the location, the zone and the quantity restriccion.


Distances, cost, emissions and illustration:
Now that we had all the locations for one instance, it was time to find the distances, costs and emmisions between all the warehouses and stores. To do this, we made a class called Case, which is one instance. This class have functions to determine the distances, costs and emmisions. In addition, Case has a function getMap(), which can be used to illustrate the points in a 600x600 grid.


Libraries that have been used:
Random: We have used random to generate random numbers for the locations, capacity and emissions. To avoid a repetition of the random numbers, we have been using timestamp = int(time.time()) and random.seed(timestamp) to make the random function work properly.

Matplotlib and Shapely:
To define warehouses inside either zone "verde" or "celeste" and stores inside "tiendas", we have been using the shapely.geometry library defining the zones as polygons and locations as point. Since we knew the dimentions of celeste, verde and tiendas, we could calculate the zone of each location by defining each zone as a polygon and thereafter check if the x and y coordinates were inside the polygon.

Numpy and Euclidean from Scipy:
To find the distance between each point, we used Numpy and Scipy to calculate the euclidean value of the distance from each I to each J.

