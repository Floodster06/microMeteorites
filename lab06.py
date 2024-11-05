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
unique_diameters = {}  # stores the largest diameter at each unique impact coordinate

meteorites = 0

# Dictionary to track the number of impacts per coordinate
impact_count = {}


# Function to simulate a meteorite impact
def simulate_meteorite():
    meteorite_diameter = random.triangular(0.0001, 0.1, 0.001)  # cm
    meteorite_velocity = random.triangular(11000, 72000, 20000)  # m/s
    meteorite_mass = random.triangular(10e-9, 10e-6, 10e-8)  # kg

    meteorite_materials = ["Iron-Nickel Alloy", "Silicates (Olivine/Pyroxene)", "Carbonaceous Chondrites"]
    meteorite_material = random.choice(meteorite_materials)

    crater_constant = {"Iron-Nickel Alloy": 0.1, "Silicates (Olivine/Pyroxene)": 0.2, "Carbonaceous Chondrites": 0.3}[
        meteorite_material]

    # Calculate kinetic energy (joules)
    kinetic_energy = 0.5 * meteorite_mass * meteorite_velocity ** 2

    # Calculate crater diameter
    crater_diameter = crater_constant * (kinetic_energy ** (1 / 3)) * (8.7 ** -0.165) * (2200 ** -0.3)

    return crater_diameter, kinetic_energy


# Calculate total area covered based on largest crater diameters at each coordinate
def calculate_total_area_covered():
    total_area = 0
    for diameter in unique_diameters.values():
        radius = diameter / 2  # Convert diameter to radius
        area = math.pi * (radius ** 2)  # Area of circle
        total_area += area
    return total_area


# Simulate the meteorite impacts
def simulate_impact():
    global meteorites

    # Randomly generate impact coordinates
    impact_x_coord = random.randint(0, 19)
    impact_y_coord = random.randint(0, 19)
    coord = (impact_x_coord, impact_y_coord)

    # Update impact count for each coordinate
    if coord not in impact_count:
        impact_count[coord] = 0
    impact_count[coord] += 1

    # Generate meteorite impact properties
    crater_diameter, _ = simulate_meteorite()

    # Check if this is a new coordinate
    if coord not in non_duplicate_coords:
        non_duplicate_coords.append(coord)
        unique_diameters[coord] = crater_diameter  # Initialize with the first crater diameter
    else:
        # Update to the largest crater diameter at this coordinate
        unique_diameters[coord] = max(unique_diameters[coord], crater_diameter)

    # Append all impact data
    meteorite_locations.append(coord)
    meteorite_diameters.append(crater_diameter)

    # Increment the meteorite counter
    meteorites += 1


# Simulate impacts day by day until the entire grid is covered
simulating = True
days = 0
halfway_plotted = False  # flag to ensure halfway plot only once

while simulating:
    simulate_impact()  # Generate new impact each day
    days += 1

    # Check if half the grid (200 unique coordinates) has been impacted
    if len(non_duplicate_coords) == 200 and not halfway_plotted:
        print("Number of days until half of the window has one or more impacts in each 1 cm^2 section:", days, " days.")

        # Calculate statistics
        total_area_covered = calculate_total_area_covered()
        avg_impacts_per_cm2 = meteorites / 400
        max_impacts_per_cm2 = max(impact_count.values())

        # Display statistics
        print("Average impacts per cm² at half coverage: ~", round(avg_impacts_per_cm2), 2, "impacts.")
        print("Highest number of impacts on any cm² at half coverage:", max_impacts_per_cm2, "impacts.")
        print("Total area covered at half coverage: ~", round(total_area_covered, 2), "cm².")

        # Plot meteorite impacts
        meteorite_locations_np = np.array(meteorite_locations)
        meteorite_diameters_np = np.array(meteorite_diameters)

        # Create the scatter plot
        plt.figure(figsize=(10, 10))
        scatter = plt.scatter(meteorite_locations_np[:, 0], meteorite_locations_np[:, 1],
                              s=meteorite_diameters_np * 1000,  # Scale up crater diameter for visualization
                              c=meteorite_diameters_np, cmap='viridis', alpha=0.6, edgecolors='w')

        # Add color bar to represent crater diameter
        cbar = plt.colorbar(scatter)
        cbar.set_label('Crater Diameter, Scaled (cm²)')

        # Label axes and title
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title(f'Meteorite Impact Locations with Crater Diameter (Day {days})')
        plt.show()

        halfway_plotted = True  # Set flag to prevent repeated plotting

    # Check if the entire grid (400 unique coordinates) has been impacted
    if len(non_duplicate_coords) == 400:
        print("------------------------------------------------------")

        print("Number of days until the entire window has one or more impacts in each 1 cm^2 section:", days, "days.")

        # Calculate statistics
        total_area_covered = calculate_total_area_covered()
        avg_impacts_per_cm2 = meteorites / 400
        max_impacts_per_cm2 = max(impact_count.values())

        # Display statistics
        print("Total impacts for the entire 400 cm² area:", meteorites, "impacts.")
        print("Average impacts per cm² for the entire area: ~", round(avg_impacts_per_cm2, 2), "impacts.")
        print("Highest number of impacts on any cm² for the entire area:", max_impacts_per_cm2, "impacts.")
        print("Total area covered for the entire area: ~", round(total_area_covered, 2), "cm².")

        # Plot meteorite impacts
        meteorite_locations_np = np.array(meteorite_locations)
        meteorite_diameters_np = np.array(meteorite_diameters)

        # Create the scatter plot
        plt.figure(figsize=(10, 10))
        scatter = plt.scatter(meteorite_locations_np[:, 0], meteorite_locations_np[:, 1],
                              s=meteorite_diameters_np * 1000,  # Scale up crater diameter for visualization
                              c=meteorite_diameters_np, cmap='viridis', alpha=0.6, edgecolors='w')

        # Add color bar to represent crater diameter
        cbar = plt.colorbar(scatter)
        cbar.set_label('Crater Diameter, Scaled (cm²)')

        # Label axes and title
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title(f'Meteorite Impact Locations with Crater Diameter (Day {days})')
        plt.show()

        # Stop simulation
        simulating = False
