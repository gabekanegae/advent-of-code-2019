#####################################################
# --- Day 1: The Tyranny of the Rocket Equation --- #
#####################################################

import AOCUtils

def reqFuel(m):
    return (m // 3) - 2

#####################################################

masses = AOCUtils.loadInput(1)

fuelSum = sum(reqFuel(m) for m in masses)
print("Part 1: {}".format(fuelSum))

fuelSum = 0
for m in masses:
    fuel = reqFuel(m)
    while fuel >= 0:
        fuelSum += fuel
        fuel = reqFuel(fuel)

print("Part 2: {}".format(fuelSum))

AOCUtils.printTimeTaken()