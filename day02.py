#####################################
# --- Day 2: 1202 Program Alarm --- #
#####################################

import AOCUtils
from intcodeVM import VM

#####################################

rawProgram = AOCUtils.loadInput(2)
memory = [int(i) for i in rawProgram.split(",")]

vm = VM(memory)
vm[1], vm[2] = 12, 2
vm.run()
print("Part 1: {}".format(vm[0]))

found = False
for noun in range(100):
    if found: break
    for verb in range(100):
        vm = VM(memory)
        vm[1], vm[2] = noun, verb
        vm.run()
        if vm[0] == 19690720:
            print("Part 2: {}".format(100*noun+verb))
            found = True
            break

AOCUtils.printTimeTaken()