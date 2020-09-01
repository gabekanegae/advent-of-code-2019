######################################
# --- Day 10: Monitoring Station --- #
######################################

import AOCUtils
import math

def countInLOS(station, asteroids, size):
    detected = set()
    for asteroid in asteroids:
        if asteroid != station:
            dx, dy = asteroid[0]-station[0], asteroid[1]-station[1]

            # Divide by gcd to determine direction from origin,
            # reducing all colinear asteroids to one
            g = abs(math.gcd(dx, dy))
            reduced = (dx//g, dy//g)
            detected.add(reduced)

    return detected

######################################

rawAsteroids = AOCUtils.loadInput(10)
size = (len(rawAsteroids), len(rawAsteroids[0]))

asteroids = set()
for x in range(size[0]):
    for y in range(size[1]):
        if rawAsteroids[x][y] == "#":
            asteroids.add((x, y))

# Count asteroids in line of sight for all possible station positions
stationCounts = []
for station in asteroids:
    inLOS = countInLOS(station, asteroids, size)
    stationCounts.append((len(inLOS), station, inLOS))

# Sort by most asteroids in line of sight and get first
stationCounts.sort(reverse=True)
amtInLOS, station, inLOS = stationCounts[0]

print("Part 1: {}".format(amtInLOS))

n = 200

# Sort by atan2 of swapped coordinates
# (starts pointing up and rotates cw, instead of pointing right and rotating ccw)
destroyed = [(math.atan2(dy, dx), (dx, dy)) for dx, dy in inLOS]
destroyed.sort(reverse=True)

# Assumes nth asteroid can be destroyed in a single full rotation
dx, dy = destroyed[n-1][1]

x, y = station[0]+dx, station[1]+dy
while (x, y) not in asteroids:
    x, y = x+dx, y+dy

print("Part 2: {}".format(y*100 + x))

AOCUtils.printTimeTaken()