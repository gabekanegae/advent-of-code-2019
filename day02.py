#####################################
# --- Day 2: 1202 Program Alarm --- #
#####################################

import AOCUtils

def runProgram(memory, noun, verb):
    memory = memory[:]

    memory[1] = noun
    memory[2] = verb

    pc = 0
    while True:
        opcode, a, b, c = memory[pc:pc+4]
        try:
            if opcode == 1:
                memory[c] = memory[a] + memory[b]
            elif opcode == 2:
                memory[c] = memory[a] * memory[b]
            elif opcode == 99:
                break
            pc += 4
        except:
            break

    return memory[0]

#####################################

rawProgram = AOCUtils.loadInput(2)
memory = [int(i) for i in rawProgram.split(",")]

print("Part 1: {}".format(runProgram(memory, 12, 2)))

for noun in range(100):
    for verb in range(100):
        if runProgram(memory, noun, verb) == 19690720:
            print("Part 2: {}".format(100*noun+verb))
            break

AOCUtils.printTimeTaken()