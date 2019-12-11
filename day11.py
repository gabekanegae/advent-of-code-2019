###############################
#--- Day 11: Space Police --- #
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
        if rw.lower() == "memory":
            if mode == 0: return self.getMemory(data)
            elif mode == 1: return data
            elif mode == 2: return self.getMemory(self.base+data)
        elif rw.lower() == "address":
            if mode == 0: return data
            elif mode == 1: return data
            elif mode == 2: return self.base+data
        else:
            raise Exception("Invalid memory/address mode ({}).".format(rw))

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
                a = self.parseMode(self.getMemoryPC(1), modeA, "memory")
                npc = self.pc+2
            elif opcode in [3]: # in
                a = self.parseMode(self.getMemoryPC(1), modeA, "address")
                npc = self.pc+2
            elif opcode in [5, 6]: # jit, jif
                a = self.parseMode(self.getMemoryPC(1), modeA, "memory")
                b = self.parseMode(self.getMemoryPC(2), modeB, "memory")
                npc = self.pc+3
            elif opcode in [1, 2, 7, 8]: # add, mult, lt, eq
                a = self.parseMode(self.getMemoryPC(1), modeA, "memory")
                b = self.parseMode(self.getMemoryPC(2), modeB, "memory")
                c = self.parseMode(self.getMemoryPC(3), modeC, "address")
                npc = self.pc+4

            if opcode == 1: # add
                self.setMemory(c, a + b)
            elif opcode == 2: # mult
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

def paintingRobot(memory, start):
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    pos = (0, 0)
    facing = 0
    painted = {(0, 0): start}

    vm = VM(memory)
    while not vm.halted:
        vm.run(int(pos in painted and painted[pos]))
        color, rotation = vm.output[-2:]
        
        painted[pos] = color

        if rotation == 0: # Left
            facing += 1
        elif rotation == 1: # Right
            facing -= 1
        facing %= len(directions)

        step = directions[facing]
        pos = (pos[0]+step[0], pos[1]+step[1])

    return painted

###############################

rawProgram = AOCUtils.loadInput(11)
memory = [int(i) for i in rawProgram.split(",")]

painted = paintingRobot(memory, 0)
print("Part 1: {}".format(len(painted)))

painted = paintingRobot(memory, 1)
whitePanels = [k for k, v in painted.items() if v == 1]

minPoint = list(whitePanels[0])
maxPoint = list(whitePanels[0])
for p in whitePanels[1:]:
    if p[0] < minPoint[0]: minPoint[0] = p[0]
    elif p[0] > maxPoint[0]: maxPoint[0] = p[0]
    if p[1] < minPoint[0]: minPoint[1] = p[1]
    elif p[1] > maxPoint[1]: maxPoint[1] = p[1]

print("Part 2:")
for x in range(minPoint[0], maxPoint[0]+1):
    for y in range(minPoint[1], maxPoint[1]+1):
        if (x, y) in whitePanels:
            print("##", end="")
        else:
            print("  ", end="")
    print()

AOCUtils.printTimeTaken()