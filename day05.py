###################################################
# --- Day 5: Sunny with a Chance of Asteroids --- #
###################################################

import AOCUtils
from intcodeVM import VM

###################################################

rawProgram = AOCUtils.loadInput(5)
memory = [int(i) for i in rawProgram.split(",")]

vm = VM(memory)
vm.run(1)
print("Part 1: {}".format(vm.output[-1]))

vm = VM(memory)
vm.run(5)
print("Part 2: {}".format(vm.output[-1]))

AOCUtils.printTimeTaken()