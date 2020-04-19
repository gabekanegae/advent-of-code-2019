################################
# --- Day 13: Care Package --- #
################################

import AOCUtils
from intcodeVM import VM

def drawScreen(blocks):
    blocksArt = [" ", "#", "X", "-", "*"]

    for y in range(20):
        for x in range(50):
            if (x, y) in blocks:
                block = blocks[(x, y)]
            else:
                block = 0
            print(blocksArt[block]*2, end="")
        print()
    print("Score: {}".format(score))
    # input()

################################

rawProgram = AOCUtils.loadInput(13)
memory = [int(i) for i in rawProgram.split(",")]

vm = VM(memory)
vm.run()
blocksAmt = sum([vm.output[b] == 2 for b in range(2, len(vm.output), 3)])
print("Part 1: {}".format(blocksAmt))

movement = 0
score = 0
blocks = dict()
ballPos, paddlePos = None, None

vm = VM(memory)
vm[0] = 2

while not vm.halted:
    vm.run(movement)

    # Parse screen data
    for i in range(0, len(vm.output), 3):
        pos = (vm.output[i], vm.output[i+1])
        block = vm.output[i+2]
        
        # Get ball and paddle positions
        if pos[0] >= 0 and pos[1] >= 0:
            if block == 3:
                ballPos = pos
            elif block == 4:
                paddlePos = pos
            blocks[pos] = block

        # Get score
        if pos == (-1, 0):
            score = block

    # Clear parsed data
    vm.output = []

    # Paddle AI
    if ballPos[0] < paddlePos[0]:
        movement = 1
    elif ballPos[0] > paddlePos[0]:
        movement = -1
    else:
        movement = 0

    # drawScreen(blocks)

print("Part 2: {}".format(score))

AOCUtils.printTimeTaken()