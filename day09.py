##############################
#--- Day 9: Sensor Boost --- #
##############################

import AOCUtils

def runProgram(memory, inBuf, pc=None):
    if not pc: # If no pc is provided, run it standalone
        pc = 0
        memory = memory[:]

    memory += [0 for i in range(16384-len(memory))] # Total of 2**14 values

    inPtr = 0
    base = 0
    output = []

    while True:
        paramAndOpcode = "{:05}".format(memory[pc])

        opcode = int(paramAndOpcode[-2:])
        modeC, modeB, modeA = [int(i) for i in paramAndOpcode[:3]]

        try:
            if opcode in [9]:
                a = memory[pc+1]
                if modeA == 0: ia = memory[a]
                elif modeA == 1: ia = a
                elif modeA == 2: ia = memory[base+a]

                npc = pc + 2
            elif opcode in [3, 4]:
                a = memory[pc+1]
                if modeA == 0: ia = a
                elif modeA == 1: ia = a
                elif modeA == 2: ia = base+a

                npc = pc + 2
            elif opcode in [5, 6]:
                a, b = memory[pc+1:pc+3]
                if modeA == 0: ia = memory[a]
                elif modeA == 1: ia = a
                elif modeA == 2: ia = memory[base+a]
                if modeB == 0: ib = memory[b]
                elif modeB == 1: ib = b
                elif modeB == 2: ib = memory[base+b]

                npc = pc + 3
            elif opcode in [1, 2, 7, 8]:
                a, b, c = memory[pc+1:pc+4]
                if modeA == 0: ia = memory[a]
                elif modeA == 1: ia = a
                elif modeA == 2: ia = memory[base+a]
                if modeB == 0: ib = memory[b]
                elif modeB == 1: ib = b
                elif modeB == 2: ib = memory[base+b]
                if modeC == 0: ic = c
                elif modeC == 1: ic = c
                elif modeC == 2: ic = base+c

                npc = pc + 4

            if opcode == 1: # add
                memory[ic] = ia + ib
            elif opcode == 2: # mult
                memory[ic] = ia * ib
            elif opcode == 3: # in
                # If there's no input to be processed, wait for one (return its current state)
                if inPtr < len(inBuf):
                    memory[ia] = inBuf[inPtr]
                    inPtr += 1
                else:
                    return memory, pc, output
            elif opcode == 4: # out
                output.append(memory[ia])
            elif opcode == 5: # jit
                if ia != 0: npc = ib
            elif opcode == 6: # jif
                if ia == 0: npc = ib
            elif opcode == 7: # lt
                memory[ic] = int(ia < ib)
            elif opcode == 8: # eq
                memory[ic] = int(ia == ib)
            elif opcode == 9: # arb
                base += ia
            elif opcode == 99:
                break

            pc = npc
        except IndexError: # Tried to access invalid memory address
            break

    # Halted (no partial memory or pc)
    return None, None, output

##############################

rawProgram = AOCUtils.loadInput(9)
memory = [int(i) for i in rawProgram.split(",")]

_, _, output = runProgram(memory, [1])
print("Part 1: {}".format(output[0]))

_, _, output = runProgram(memory, [2])
print("Part 2: {}".format(output[0]))

AOCUtils.printTimeTaken()