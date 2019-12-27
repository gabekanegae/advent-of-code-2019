################################
# --- Day 19: Tractor Beam --- #
################################

import AOCUtils
from intcodeVM import VM
from collections import deque

def check(memory, x, y):
    vm = VM(memory)
    vm.run([x, y])
    return vm.output[-1]

################################

rawProgram = AOCUtils.loadInput(19)
memory = [int(i) for i in rawProgram.split(",")]

total = 0
x0 = 0
for y in range(50):
    zeros, ones = 0, 0
    for x in range(x0, 50):
        if check(memory, x, y) == 1:
            # Assumes that it can start the next line
            # at the pos of first ocurrence of 1 in this one
            if ones == 0: x0 = x
            ones += 1
        else:
            # Assumes that there won't be 1s after...
            if ones > 0: # 10
                total += ones
                break
            else: # 00000
                zeros += 1
                if zeros > 5: break

print("Part 1: {}".format(total))

result = None
x0 = 0
for y in range(100, 10000): # Skip first 100 lines
    if result: break
    for x in range(x0, 10000):
        # Go along bottom edge of beam (square bottom-left)
        if check(memory, x, y) == 1:
            if check(memory, x+99, y-99) == 1: # Check square top-right
                result = 10000*x+(y-99) # Result is square top-left
            x0 = x
            break

print("Part 2: {}".format(result))

AOCUtils.printTimeTaken()