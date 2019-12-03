################################
# --- Day 3: Crossed Wires --- #
################################

import AOCUtils

################################

wires = [w.split(",") for w in AOCUtils.loadInput(3)]

wirePaths = [set() for _ in range(len(wires))]
wirePathsLength = [dict() for _ in range(len(wires))]

for w, wire in enumerate(wires):
    pos = (0, 0)
    stepsCount = 0
    for step in wire:
        direction, distance = step[0], int(step[1:])
        for i in range(distance):
            if direction == "R": pos = (pos[0]+1, pos[1])
            elif direction == "L": pos = (pos[0]-1, pos[1])
            elif direction == "U": pos = (pos[0], pos[1]+1)
            elif direction == "D": pos = (pos[0], pos[1]-1)
            
            wirePaths[w].add(pos)

            stepsCount += 1
            if pos not in wirePathsLength[w]:
                wirePathsLength[w][pos] = stepsCount
            wirePathsLength[w][pos] = min(wirePathsLength[w][pos], stepsCount)

intersections = wirePaths[0]
for w in wirePaths[1:]:
    intersections = intersections.intersection(w)

distances = [abs(p[0]) + abs(p[1]) for p in intersections]
print("Part 1: {}".format(min(distances)))

intersectionsSteps = []
for i in intersections:
    s = sum([wl[i] for wl in wirePathsLength])
    intersectionsSteps.append(s)

print("Part 2: {}".format(min(intersectionsSteps)))

AOCUtils.printTimeTaken()