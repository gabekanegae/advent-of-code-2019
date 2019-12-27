#####################################
# --- Day 24: Planet of Discord --- #
#####################################

import AOCUtils

#####################################

rawLayout = AOCUtils.loadInput(24)

layout = [list(s) for s in rawLayout]
size = (len(layout), len(layout[0]))

seen = set()
while True:
    # Calculate biodiversity rating
    bioRating = 0
    for x in range(size[0]):
        for y in range(size[1]):
            if layout[x][y] == "#":
                bioRating += 2**(x*size[1] + y)

    if bioRating in seen: break
    seen.add(bioRating)
    
    # Update layout
    newLayout = [s[:] for s in layout]
    for x in range(size[0]):
        for y in range(size[1]):
            aliveNeighbors = 0
            if x-1 >= 0 and layout[x-1][y] == "#": aliveNeighbors += 1
            if y-1 >= 0 and layout[x][y-1] == "#": aliveNeighbors += 1
            if x+1 < size[0] and layout[x+1][y] == "#": aliveNeighbors += 1
            if y+1 < size[1] and layout[x][y+1] == "#": aliveNeighbors += 1

            if layout[x][y] == "#" and aliveNeighbors != 1:
                newLayout[x][y] = "."
            elif layout[x][y] == "." and aliveNeighbors in [1, 2]:
                newLayout[x][y] = "#"
    layout = newLayout

print("Part 1: {}".format(bioRating))

# Each iteration will spread bugs to, at most, +1 upper and +1 lower level
iterations = 200
levels = iterations//2

# Convert list of lists to dict
layout = dict()
for x in range(size[0]):
    for y in range(size[1]):
        for level in range(-levels, levels+1):
            if (x, y) == (2, 2): continue

            if level == 0: layout[(x, y, 0)] = rawLayout[x][y]
            else: layout[(x, y, level)] = "."

# Generate list of neighbors for each position
neighbors = dict()
for x in range(size[0]):
    for y in range(size[1]):
        if (x, y) == (2, 2): continue

        for level in range(-levels, levels+1):
            thisNeighbors = []

            # Same level
            for m in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                xi, yi = x+m[0], y+m[1]
                if 0 <= xi < size[0] and 0 <= yi < size[1] and (xi, yi) != (2, 2):
                    thisNeighbors.append((xi, yi, level))

            # Lower level
            if level-1 >= -levels:
                if x == 0: thisNeighbors.append((1, 2, level-1))
                if y == 0: thisNeighbors.append((2, 1, level-1))
                if x == size[0]-1: thisNeighbors.append((3, 2, level-1))
                if y == size[1]-1: thisNeighbors.append((2, 3, level-1))

            # Upper level
            if level+1 <= levels:
                if (x, y) == (1, 2): thisNeighbors += [(0, yi, level+1) for yi in range(size[1])]
                if (x, y) == (2, 1): thisNeighbors += [(xi, 0, level+1) for xi in range(size[0])]
                if (x, y) == (3, 2): thisNeighbors += [(size[0]-1, yi, level+1) for yi in range(size[1])]
                if (x, y) == (2, 3): thisNeighbors += [(xi, size[1]-1, level+1) for xi in range(size[0])]

            neighbors[(x, y, level)] = thisNeighbors

# Run all iterations
for i in range(iterations):
    newLayout = dict()
    for k, v in layout.items():
        aliveNeighbors = sum([layout[neighbor] == "#" for neighbor in neighbors[k]])

        if v == "#" and aliveNeighbors != 1:
            newLayout[k] = "."
        elif v == "." and aliveNeighbors in [1, 2]:
            newLayout[k] = "#"
        else:
            newLayout[k] = layout[k]

    layout = newLayout

# Count bugs
bugAmt = sum([v == "#" for v in layout.values()])
print("Part 2: {}".format(bugAmt))

AOCUtils.printTimeTaken()