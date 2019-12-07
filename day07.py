#######################################
#--- Day 7: Amplification Circuit --- #
#######################################

import AOCUtils
from itertools import permutations

def runProgram(memory, inBuf, pc=None):
    if not pc: # If no pc is provided, run it standalone
        pc = 0
        memory = memory[:]

    inPtr = 0
    output = []

    while True:
        paramAndOpcode = "{:05}".format(memory[pc])

        opcode = int(paramAndOpcode[-2:])
        modeC, modeB, modeA = [int(i) for i in paramAndOpcode[:3]]

        try:
            if opcode in [3, 4]:
                a = memory[pc+1]
                ia = a if modeA else memory[a]
                npc = pc + 2
            elif opcode in [5, 6]:
                a, b = memory[pc+1:pc+3]
                ia = a if modeA else memory[a]
                ib = b if modeB else memory[b]
                npc = pc + 3
            elif opcode in [1, 2, 7, 8]:
                a, b, c = memory[pc+1:pc+4]
                ia = a if modeA else memory[a]
                ib = b if modeB else memory[b]
                ic = c if modeC else memory[c]
                npc = pc + 4

            if opcode == 1: # add
                memory[c] = ia + ib
            elif opcode == 2: # mult
                memory[c] = ia * ib
            elif opcode == 3: # in
                # If there's no input to be processed, wait for one (return its current state)
                if inPtr < len(inBuf):
                    memory[a] = inBuf[inPtr]
                    inPtr += 1
                else:
                    return memory, pc, output
            elif opcode == 4: # out
                output.append(memory[a])
            elif opcode == 5: # jit
                if ia != 0: npc = ib
            elif opcode == 6: # jif
                if ia == 0: npc = ib
            elif opcode == 7: # lt
                memory[c] = int(ia < ib)
            elif opcode == 8: # eq
                memory[c] = int(ia == ib)
            elif opcode == 99:
                break

            pc = npc
        except:
            break

    # Halted (no partial memory or pc)
    return None, None, output

#######################################

rawProgram = AOCUtils.loadInput(7)
memory = [int(i) for i in rawProgram.split(",")]

thrusterSignals = dict()
for phase in permutations([0, 1, 2, 3, 4]):
    signal = 0
    for i in range(5):
        _, _, signal = runProgram(memory, [phase[i], signal])
        signal = signal[0]
    thrusterSignals[phase] = signal

print("Part 1: {}".format(max(thrusterSignals.values())))

thrusterSignals = dict()
for phase in permutations([5, 6, 7, 8, 9]):
    ampState = [[memory[:], 0, None] for i in range(5)] # [memory, pc, output]
    ampState[4][2] = 0 # Set amp #4 output to 0, so amp #0 receives it as input

    for i in range(5): # Send phase setting, does not expect any output
        ampState[i][0], ampState[i][1], _ = runProgram(ampState[i][0], [phase[i]], ampState[i][1])

    while any([amp[0] for amp in ampState]):
        for i in range(5): # Run each of the amps in order
            ampState[i][0], ampState[i][1], signal = runProgram(ampState[i][0], [ampState[(i-1)%5][2]], ampState[i][1])
            signal = signal[0]
            ampState[i][2] = signal

    thrusterSignals[phase] = signal

print("Part 2: {}".format(max(thrusterSignals.values())))

AOCUtils.printTimeTaken()