########################################
# --- Day 7: Amplification Circuit --- #
########################################

import AOCUtils
from intcodeVM import VM
from itertools import permutations

########################################

rawProgram = AOCUtils.loadInput(7)
memory = [int(i) for i in rawProgram.split(",")]

vm = VM(memory)
vm.run(1)

thrusterSignals = dict()
for phase in permutations([0, 1, 2, 3, 4]):
    signal = 0
    for i in range(5):
        vm = VM(memory)
        vm.run([phase[i], signal])
        signal = vm.output[0]
    thrusterSignals[phase] = signal

print("Part 1: {}".format(max(thrusterSignals.values())))

thrusterSignals = dict()
for phase in permutations([5, 6, 7, 8, 9]):
    vms = [VM(memory) for _ in range(5)]
    vmOutputs = [0 for _ in range(5)]

    for i in range(5): # Send phase setting, does not expect any output
        vms[i].run(phase[i])

    while not any([vm.halted for vm in vms]):
        for i in range(5): # Run each of the amps in order
            vms[i].run(vmOutputs[(i-1)%5])
            signal = vms[i].output[-1]
            vmOutputs[i] = signal

    thrusterSignals[phase] = signal

print("Part 2: {}".format(max(thrusterSignals.values())))

AOCUtils.printTimeTaken()