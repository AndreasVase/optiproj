import random
import tkinter as tk

# Define the list of limits. Each limit is a tuple of the form (x_min, x_max, y_min, y_max)
limitsInstances = [
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

# Generate random (x, y) pairs for each limit
result = []
for limit in limitsInstances:
    x_min, x_max, y_min, y_max = limit
    x = random.randint(x_min, x_max)
    y = random.randint(y_min, y_max)
    result.append((x, y))


# # Print the result
# for i, point in enumerate(result):
#     print(f"Point {i + 1}: ({point[0]}, {point[1]})")

# Making limits for the zones
zonatienda = 150
zonaverde = 400
zonaceleste = 600

x1zonatienda = ((zonaceleste-zonatienda)/2, (zonaceleste-zonatienda)/2)
x2zonatienda = (x1zonatienda[0] + zonatienda, x1zonatienda[1])
x3zonatienda = (x2zonatienda[0], x2zonatienda[1] + zonatienda)
x4zonatienda = (x1zonatienda[0], x3zonatienda[1])

x1zonaverde = ((zonaceleste-zonaverde)/2, (zonaceleste-zonaverde)/2)
x2zonaverde = (x1zonaverde[0] + zonaverde, x1zonaverde[1])
x3zonaverde = (x2zonaverde[0], x2zonaverde[1] + zonaverde)
x4zonaverde = (x1zonaverde[0], x3zonaverde[1])

x1zonaceleste = ((zonaceleste-zonaceleste)/2, (zonaceleste-zonaceleste)/2)
x2zonaceleste = (x1zonaceleste[0] + zonaceleste, x1zonaceleste[1])
x3zonaceleste = (x2zonaceleste[0], x2zonaceleste[1] + zonaceleste)
x4zonaceleste = (x1zonaceleste[0], x3zonaceleste[1])




#Printing all the zones
print("Zona Tienda")
print(x1zonatienda)
print(x2zonatienda)
print(x3zonatienda)
print(x4zonatienda)

print("Zona Verde")
print(x1zonaverde)
print(x2zonaverde)
print(x3zonaverde)
print(x4zonaverde)

print("Zona Celeste")
print(x1zonaceleste)
print(x2zonaceleste)
print(x3zonaceleste)
print(x4zonaceleste)

# # Create a function to draw squares on the canvas
# def draw_squares():
#     canvas.delete("all")  # Clear the canvas
    
#     # Draw zonatienda
#     canvas.create_rectangle(
#         (canvas_width - zonatienda) / 2,
#         (canvas_height - zonatienda) / 2,
#         (canvas_width + zonatienda) / 2,
#         (canvas_height + zonatienda) / 2,
#         fill="red"  # You can change the fill color
#     )

#     # Draw zonaverde
#     canvas.create_rectangle(
#         (canvas_width - zonaverde) / 2,
#         (canvas_height - zonaverde) / 2,
#         (canvas_width + zonaverde) / 2,
#         (canvas_height + zonaverde) / 2,
#         fill="green"  # You can change the fill color
#     )

#     # Draw zonaceleste
#     canvas.create_rectangle(
#         (canvas_width - zonaceleste) / 2,
#         (canvas_height - zonaceleste) / 2,
#         (canvas_width + zonaceleste) / 2,
#         (canvas_height + zonaceleste) / 2,
#         fill="blue"  # You can change the fill color
#     )

# # Create the main window
# root = tk.Tk()
# root.title("Zones Viewer")

# # Define canvas dimensions
# canvas_width = 800
# canvas_height = 800

# # Create a canvas to draw the squares
# canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
# canvas.pack()

# # Create a button to redraw the squares
# draw_button = tk.Button(root, text="Draw Squares", command=draw_squares)
# draw_button.pack()

# # Initialize the canvas with squares
# draw_squares()

# # Start the GUI event loop
# root.mainloop()

