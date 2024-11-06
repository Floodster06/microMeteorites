"""
Lab06: Matrix (Loop 2D)
Royal Military College of Canada
CSE101
Dr. Yawei Liang
OCdt Flood 31226
November 11, 2024

The goal of this lab is to gain experience using a two-dimensional array, practice using loops, and using the rand() function to simulate a natural phenomenon.
The program will simulate the impact of micro-meteorites on a space station in low-Earth orbit.
As an added bonus, the program will generate a visualization of the 2D matrix (the space shuttle's surface) and use collision physics to determine the crater diameter upon impact with the space station.
"""
import random
import math
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io

# Grid dimensions
rows, cols = (20, 20)

# Initialize arrays to store meteorite locations and diameters
meteorite_locations = []
meteorite_diameters = []

non_duplicate_coords = []  # stores coordinates without duplicates
unique_diameters = {}  # stores the largest diameter at each unique impact coordinate

meteorites = 0  # accumulator to keep track of meteorites simulated so far

impact_count = {}  # Dictionary to track the number of impacts per coordinate


# Function to simulate a meteorite impact
def simulate_meteorite():
    # random.triangular(low, high, weight) = method to generate pseudorandom numbers between a certain range with a weighting (called a mode) to a specific number
    meteorite_diameter = random.triangular(0.0001, 0.1, 0.001)  # cm
    meteorite_mass = random.triangular(10e-9, 10e-6, 10e-8)  # kg
    meteorite_velocity = random.triangular(11000, 72000, 20000)  # m/s

    # NOTE: error was made when determining variable; should be called meteorite_speed; velocity implies a direction when none is associated

    meteorite_materials = ["Iron-Nickel Alloy", "Silicates (Olivine/Pyroxene)",
                           "Carbonaceous Chondrites"]  # array of most common micro-meteorite materials
    meteorite_material = random.choice(meteorite_materials)  # selects a random material from the list

    crater_constant = {"Iron-Nickel Alloy": 0.1, "Silicates (Olivine/Pyroxene)": 0.2, "Carbonaceous Chondrites": 0.3}[
        meteorite_material]  # sets the crater constant (a constant used in one of the equations, dpenedant on impacting material) to it's respective number

    kinetic_energy = 0.5 * meteorite_mass * meteorite_velocity ** 2  # Calculate kinetic energy (joules)

    # D = k x Ek^1/3 x g^-0.165 x density^-0.3
    crater_diameter = crater_constant * (kinetic_energy ** (1 / 3)) * (8.7 ** -0.165) * (2200 ** -0.3)  # Calculate crater diameter (m)

    radius = (crater_diameter) / 2 # in cm
    crater_area = (math.pi * (radius ** 2)) # cm^2



    return crater_area


# Calculate white space area by converting plot to grayscale and analyzing pixels
def calculate_white_space_area():
    # Save the plot to a buffer instead of saving it to disk
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Load the image from buffer and convert to grayscale
    image = Image.open(buf).convert("L")  # Convert to grayscale

    # Convert image to numpy array
    image_array = np.array(image)

    # Define a threshold to classify white (uncovered) areas vs covered areas
    threshold = 240
    white_pixels = np.sum(image_array > threshold)
    total_pixels = image_array.size

    # Calculate white space and covered area
    white_space_ratio = white_pixels / total_pixels
    white_space_area = white_space_ratio * 400  # Total area in cm² is 400 cm² for a 20x20 grid
    covered_area = 400 - white_space_area  # Covered area by difference

    # Close the buffer
    buf.close()

    return white_space_area, covered_area


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
    crater_diameter = simulate_meteorite()

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
        print("Number of days until half of the window has one or more impacts in each 1 cm^2 section:", days, "days.")

        # Calculate white space and covered area
        plt.figure(figsize=(10, 10))
        scatter = plt.scatter(*zip(*meteorite_locations),
                              s=[d * 10000 for d in meteorite_diameters],  # Scale up crater diameter for visualization
                              c=meteorite_diameters, cmap='magma', alpha=0.6, edgecolors='black')
        cbar = plt.colorbar(scatter)
        cbar.set_label('Crater Diameter, Scaled (cm²)')

        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title(f'Meteorite Impact Locations with Crater Diameter (Day {days})')

        # Calculate white space and covered area from the plot
        white_space_area, covered_area = calculate_white_space_area()

        # Display statistics
        print("Affected area of space shuttle: ~", round(covered_area, 2), "cm².")
        print("Unaffected area of space shuttle: ~", round(white_space_area, 2), "cm².")
        print("Average impacts per cm²: ~", (meteorites / 400), ".")
        print("Most impacts at coordinates", max(impact_count, key=impact_count.get), "with", impact_count[max(impact_count, key=impact_count.get)], "total impacts.")

        halfway_plotted = True  # Set flag to prevent repeated plotting
        plt.show()

    # Check if the entire grid (400 unique coordinates) has been impacted
    if len(non_duplicate_coords) == 400:
        print("------------------------------------------------------")
        print("Number of days until the entire window has one or more impacts in each 1 cm^2 section:", days, "days.")

        # Generate and analyze final plot
        plt.figure(figsize=(10, 10))
        scatter = plt.scatter(*zip(*meteorite_locations),
                              s=[d * 10000 for d in meteorite_diameters],  # Scale up crater diameter for visualization
                              c=meteorite_diameters, cmap='magma', alpha=0.6, edgecolors='black')
        cbar = plt.colorbar(scatter)
        cbar.set_label('Crater Diameter, Scaled (cm²)')

        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title(f'Meteorite Impact Locations with Crater Diameter (Day {days})')

        # Calculate white space and covered area from the plot
        white_space_area, covered_area = calculate_white_space_area()

        # Display statistics
        print("Affected area of space shuttle: ~", round(covered_area, 2), "cm².")
        print("Unaffected area of space shuttle: ~", round(white_space_area, 2), "cm².")
        print("Average impacts per cm²: ~", (meteorites/400), ".")
        print("Most impacts at coordinates", max(impact_count, key=impact_count.get), "with", impact_count[max(impact_count, key=impact_count.get)], "total impacts.")

        plt.show()
        simulating = False
