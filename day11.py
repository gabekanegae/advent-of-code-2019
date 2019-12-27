################################
# --- Day 11: Space Police --- #
################################

import AOCUtils
from intcodeVM import VM

def paintingRobot(memory, start):
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    pos = (0, 0)
    facing = 0
    painted = {(0, 0): start}

    vm = VM(memory)
    while not vm.halted:
        vm.run(pos in painted and painted[pos] == 1)
        color, rotation = vm.output[-2:]
        
        painted[pos] = color

        if rotation == 0: # Left
            facing += 1
        elif rotation == 1: # Right
            facing -= 1
        facing %= len(directions)

        step = directions[facing]
        pos = (pos[0]+step[0], pos[1]+step[1])

    return painted

################################

rawProgram = AOCUtils.loadInput(11)
memory = [int(i) for i in rawProgram.split(",")]

painted = paintingRobot(memory, 0)
print("Part 1: {}".format(len(painted)))

painted = paintingRobot(memory, 1)
whitePanels = [k for k, v in painted.items() if v == 1]

minPoint = list(whitePanels[0])
maxPoint = list(whitePanels[0])
for p in whitePanels[1:]:
    if p[0] < minPoint[0]: minPoint[0] = p[0]
    elif p[0] > maxPoint[0]: maxPoint[0] = p[0]
    if p[1] < minPoint[0]: minPoint[1] = p[1]
    elif p[1] > maxPoint[1]: maxPoint[1] = p[1]

print("Part 2:")
for x in range(minPoint[0], maxPoint[0]+1):
    for y in range(minPoint[1], maxPoint[1]+1):
        if (x, y) in whitePanels:
            print("##", end="")
        else:
            print("  ", end="")
    print()

AOCUtils.printTimeTaken()