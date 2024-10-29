import random
import math

rows, cols = (20, 20)
arr = [[0]*cols]*rows



for r in range (rows):

    print(*arr[r])


def simulate_meteorite():

    meteorite_diameter = random.triangular(0.0001, 0.1, 0.001) # cm
    meteorite_velocity = random.triangular(11000, 72000, 20000) # m/s
    meteorite_mass = random.triangular(10e-9, 10e-6, 10e-8) # kg

    meteorite_materials = ["Iron-Nickel Alloy", "Silicates (Olivine/Pyroxene)", "Carbonaceous Chondrites"]
    meteorite_material = random.choice(meteorite_materials)

    crater_constant, meteorite_density = 0, 0
    match meteorite_material:

        case "Iron-Nickel Alloy":

            crater_constant = 0.1
            meteorite_density = 7900 # kg/m^3
        case "Silicates (Olivine/Pyroxene)":

            crater_constant = 0.2
            meteorite_density = 3500 # kg/m^3
        case "Carbonaceous Chondrites":

            crater_constant = 0.3
            meteorite_density = 2000 # kg/m^3

    kinetic_energy = float(0.5 * float(meteorite_mass) * float(math.pow(meteorite_velocity, 2))) # joules
    crater_diameter = crater_constant * math.pow(kinetic_energy, 1/3) * math.pow(8.7, -0.165) * math.pow(2200, -0.3)

    meteorite_info = [crater_diameter, meteorite_material, meteorite_diameter, meteorite_velocity]
    return meteorite_info


def simulate_impact():

    # determine location of impact
    # add impact to visualization




