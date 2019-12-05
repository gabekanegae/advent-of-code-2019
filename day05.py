###################################################
# --- Day 5: Sunny with a Chance of Asteroids --- #
###################################################

import AOCUtils

def runProgram(memory, inBuf):
    memory = memory[:]

    inPtr = 0
    output = []

    pc = 0
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
                memory[a] = inBuf[inPtr]
                inPtr += 1
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

    return output

###################################################

rawProgram = AOCUtils.loadInput(5)
memory = [int(i) for i in rawProgram.split(",")]

output = runProgram(memory, [1])
print("Part 1: {}".format(output[-1]))

output = runProgram(memory, [5])
print("Part 2: {}".format(output[-1]))

AOCUtils.printTimeTaken()