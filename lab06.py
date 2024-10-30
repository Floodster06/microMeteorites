import random
import math
import matplotlib.pyplot as plt
import numpy as np

# Grid dimensions
rows, cols = (20, 20)

# Initialize arrays to store meteorite locations and diameters
meteorite_locations = []
meteorite_diameters = []

meteorites = 0


# Function to simulate a meteorite impact
def simulate_meteorite():
    meteorite_diameter = random.triangular(0.0001, 0.1, 0.001)  # cm
    meteorite_velocity = random.triangular(11000, 72000, 20000)  # m/s
    meteorite_mass = random.triangular(10e-9, 10e-6, 10e-8)  # kg

    meteorite_materials = ["Iron-Nickel Alloy", "Silicates (Olivine/Pyroxene)", "Carbonaceous Chondrites"]
    meteorite_material = random.choice(meteorite_materials)

    crater_constant, meteorite_density = 0, 0
    match meteorite_material:
        case "Iron-Nickel Alloy":
            crater_constant = 0.1
            meteorite_density = 7900  # kg/m^3
        case "Silicates (Olivine/Pyroxene)":
            crater_constant = 0.2
            meteorite_density = 3500  # kg/m^3
        case "Carbonaceous Chondrites":
            crater_constant = 0.3
            meteorite_density = 2000  # kg/m^3

    # Calculate kinetic energy (joules)
    kinetic_energy = 0.5 * meteorite_mass * meteorite_velocity ** 2

    # Calculate crater diameter (using the equation from your code)
    crater_diameter = crater_constant * (kinetic_energy ** (1 / 3)) * (8.7 ** -0.165) * (2200 ** -0.3)

    # Return the crater diameter and other info (can extend if needed)
    return crater_diameter, kinetic_energy


# Simulate the meteorite impacts
def simulate_impact():
    global meteorites

    # Randomly generate impact coordinates
    impact_x_coord = random.randint(0, 19)
    impact_y_coord = random.randint(0, 19)

    # Append location and diameter of the impact
    meteorite_locations.append([impact_x_coord, impact_y_coord])

    # Simulate a meteorite and store its diameter and kinetic energy
    crater_diameter, _ = simulate_meteorite()
    meteorite_diameters.append(crater_diameter)

    meteorites += 1


# Simulate a large number of meteorite impacts
for _ in range(20):  # Adjust the number of impacts as needed
    simulate_impact()

# Convert meteorite_locations to a numpy array for plotting
meteorite_locations = np.array(meteorite_locations)
meteorite_diameters = np.array(meteorite_diameters)

# Create the scatter plot
plt.figure(figsize=(10, 10))
scatter = plt.scatter(meteorite_locations[:, 0], meteorite_locations[:, 1],
                      s=meteorite_diameters * 1000,  # Scale up crater diameter for visualization
                      c=meteorite_diameters, cmap='viridis', alpha=0.6, edgecolors='w')

# Add color bar to represent crater diameter
cbar = plt.colorbar(scatter)
cbar.set_label('Crater Diameter (scaled)')

# Label axes and title
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Meteorite Impact Locations with Crater Diameter')

# Show the plot
plt.show()



