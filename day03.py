################################
# --- Day 3: Crossed Wires --- #
################################

import AOCUtils

################################

wires = [w.split(",") for w in AOCUtils.loadInput(3)]

wirePaths = [set() for _ in range(len(wires))]
wirePathsLength = [dict() for _ in range(len(wires))]

moves = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}

for w, wire in enumerate(wires):
    pos = (0, 0)
    stepsCount = 0
    for step in wire:
        direction, distance = step[0], int(step[1:])
        for i in range(distance):
            m = moves[direction]
            pos = (pos[0]+m[0], pos[1]+m[1])

            wirePaths[w].add(pos)

            # Add step count for Part 2
            stepsCount += 1
            if pos not in wirePathsLength[w]:
                wirePathsLength[w][pos] = stepsCount
            wirePathsLength[w][pos] = min(wirePathsLength[w][pos], stepsCount)

intersections = wirePaths[0]
for w in wirePaths[1:]:
    intersections = intersections.intersection(w)

# Calculate Manhattan distance for every intersection and take min
distances = [abs(p[0]) + abs(p[1]) for p in intersections]
print("Part 1: {}".format(min(distances)))

# Calculate distance sum to every intersection and take min
intersectionsSteps = [sum([wl[i] for wl in wirePathsLength]) for i in intersections]
print("Part 2: {}".format(min(intersectionsSteps)))

AOCUtils.printTimeTaken()