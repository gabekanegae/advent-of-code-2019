###############################
# --- Day 9: Sensor Boost --- #
###############################

import AOCUtils
from intcodeVM import VM

###############################

rawProgram = AOCUtils.loadInput(9)
memory = [int(i) for i in rawProgram.split(",")]

vm = VM(memory)
vm.run(1)
print("Part 1: {}".format(vm.output[0]))

vm = VM(memory)
vm.run(2)
print("Part 2: {}".format(vm.output[0]))

AOCUtils.printTimeTaken()