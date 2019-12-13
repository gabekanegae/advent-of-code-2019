###############################
#--- Day 13: Care Package --- #
###############################

import AOCUtils

class VM:
    def __init__(self, memory):
        self.memory = memory[:]
        self.pc = 0
        self.inputPtr = 0
        self.inputBuffer = []
        self.output = []
        self.base = 0
        self.halted = False

    def parseMode(self, data, mode, rw):
        if rw.lower() == "read":
            if mode == 0: return self.getMemory(data)
            elif mode == 1: return data
            elif mode == 2: return self.getMemory(self.base+data)
        elif rw.lower() == "write":
            if mode == 0: return data
            elif mode == 1: return data
            elif mode == 2: return self.base+data
        else:
            raise Exception("Invalid read/write mode ({}).".format(rw))

    def getInput(self):
        if self.inputPtr < len(self.inputBuffer):
            self.inputPtr += 1
            return self.inputBuffer[self.inputPtr-1]
        else:
            return None

    def getMemory(self, pos):
        if pos < 0: raise Exception("Can't acess negative memory address ({}).".format(pos))

        if pos >= len(self.memory):
            self.memory += [0 for _ in range(pos+1-len(self.memory))]
        return self.memory[pos]

    def setMemory(self, pos, data):
        if pos < 0: raise Exception("Can't acess negative memory address ({}).".format(pos))

        if pos >= len(self.memory):
            self.memory += [0 for _ in range(pos+1-len(self.memory))]
        self.memory[pos] = data

    def getMemoryPC(self, offset=0): return self.getMemory(self.pc+offset)

    def run(self, inputValue=None):
        if type(inputValue) is int:
            self.inputBuffer.append(inputValue)
        elif type(inputValue) is list:
            self.inputBuffer += inputValue

        while self.pc < len(self.memory):
            paramAndOpcode = "{:05}".format(self.getMemoryPC())
            opcode = int(paramAndOpcode[-2:])
            modeC, modeB, modeA = [int(i) for i in paramAndOpcode[:3]]

            a, b, c = None, None, None
            if opcode in [4, 9]: # out, arb
                a = self.parseMode(self.getMemoryPC(1), modeA, "read")
                npc = self.pc+2
            elif opcode in [3]: # in
                a = self.parseMode(self.getMemoryPC(1), modeA, "write")
                npc = self.pc+2
            elif opcode in [5, 6]: # jit, jif
                a = self.parseMode(self.getMemoryPC(1), modeA, "read")
                b = self.parseMode(self.getMemoryPC(2), modeB, "read")
                npc = self.pc+3
            elif opcode in [1, 2, 7, 8]: # add, mul, lt, eq
                a = self.parseMode(self.getMemoryPC(1), modeA, "read")
                b = self.parseMode(self.getMemoryPC(2), modeB, "read")
                c = self.parseMode(self.getMemoryPC(3), modeC, "write")
                npc = self.pc+4

            if opcode == 1: # add
                self.setMemory(c, a + b)
            elif opcode == 2: # mul
                self.setMemory(c, a * b)
            elif opcode == 3: # in
                i = self.getInput()
                if i is not None:
                    self.setMemory(a, i)
                else:
                    return 0
            elif opcode == 4: # out
                self.output.append(a)
            elif opcode == 5: # jit
                if a != 0: npc = b
            elif opcode == 6: # jif
                if a == 0: npc = b
            elif opcode == 7: # lt
                self.setMemory(c, int(a < b))
            elif opcode == 8: # eq
                self.setMemory(c, int(a == b))
            elif opcode == 9: # arb
                self.base += a
            elif opcode == 99:
                break

            self.pc = npc

        self.halted = True
        return 0

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
    input()

###############################

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
lastOutputLength = 0

vm = VM(memory)
vm.setMemory(0, 2)

while not vm.halted:
    vm.run(movement)

    # Parse screen data
    for i in range(lastOutputLength, len(vm.output), 3):
        pos = (vm.output[i], vm.output[i+1])
        block = vm.output[i+2]

        # Get ball and paddle positions
        if block == 3:
            ballPos = pos
        elif block == 4:
            paddlePos = pos

        # Get score
        if pos == (-1, 0):
            score = block
        else:
            blocks[pos] = block
    
    lastOutputLength = len(vm.output)

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