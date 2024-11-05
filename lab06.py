import random
import math
import matplotlib.pyplot as plt
import numpy as np

# Grid dimensions
rows, cols = (20, 20)

# Initialize arrays to store meteorite locations and diameters
meteorite_locations = []
meteorite_diameters = []
non_duplicate_coords = []  # stores coordinates without duplicates
unique_diameters = []  # stores diameters of unique impacts

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
    coord = (impact_x_coord, impact_y_coord)

    # Check if this coordinate is a duplicate
    if coord not in meteorite_locations:
        # Append location and diameter of the impact
        meteorite_locations.append(coord)

        # Simulate a meteorite and store its diameter and kinetic energy
        crater_diameter, _ = simulate_meteorite()
        meteorite_diameters.append(crater_diameter)

        # Store diameter in unique_diameters for unique impacts
        unique_diameters.append(crater_diameter)

        non_duplicate_coords.append(coord)

    # Increment the meteorite counter, regardless of duplicate or not
    meteorites += 1


# Simulate impacts day by day until the entire grid is covered
simulating = True
days = 0

while simulating:
    simulate_impact()  # Generate new impact each day
    days += 1

    # Check if half the grid (200 unique coordinates) has been impacted
    if len(non_duplicate_coords) == 200:
        print("Number of days until half of the window has one or more impacts in each 1 cm^2 section:", days)

    # Check if the entire grid (400 unique coordinates) has been impacted
    if len(non_duplicate_coords) == 400:
        print("Number of days until the entire window has one or more impacts in each 1 cm^2 section:", days)
        print("Total number of impacts for the entire 400 cm^2 area:", meteorites)
        simulating = False

    # Plotting each day to visualize progress (optional, could slow down with large number of days)
    if days % 10 == 0 or not simulating:  # Plot every 10 days for quicker visualization
        # Convert meteorite_locations to a numpy array for plotting
        meteorite_locations_np = np.array(meteorite_locations)
        meteorite_diameters_np = np.array(meteorite_diameters)

        # Create the scatter plot
        plt.figure(figsize=(10, 10))
        scatter = plt.scatter(meteorite_locations_np[:, 0], meteorite_locations_np[:, 1],
                              s=meteorite_diameters_np * 1000,  # Scale up crater diameter for visualization
                              c=meteorite_diameters_np, cmap='viridis', alpha=0.6, edgecolors='w')

        # Add color bar to represent crater diameter
        cbar = plt.colorbar(scatter)
        cbar.set_label('Crater Diameter (scaled)')

        # Label axes and title
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title(f'Meteorite Impact Locations with Crater Diameter (Day {days})')
        plt.show()


