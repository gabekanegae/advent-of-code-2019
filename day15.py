#################################
# --- Day 15: Oxygen System --- #
#################################

import AOCUtils
from collections import deque

class VM:
    def __init__(self, memory, pc=0, base=0):
        self.memory = memory[:]
        self.pc = pc
        self.base = base
        self.inputPtr = 0
        self.inputBuffer = []
        self.output = []
        self.halted = False

    def copy(self):
        return VM(self.memory, self.pc, self.base)

    def __parseMode(self, data, mode, rw):
        if rw.lower() == "read":
            if mode == 0: return self[data]
            elif mode == 1: return data
            elif mode == 2: return self[self.base+data]
        elif rw.lower() == "write":
            if mode == 0: return data
            elif mode == 1: return data
            elif mode == 2: return self.base+data
        else:
            raise Exception("Invalid read/write mode ({}).".format(rw))

    def __getInput(self):
        if self.inputPtr < len(self.inputBuffer):
            self.inputPtr += 1
            return self.inputBuffer[self.inputPtr-1]
        else:
            return None

    def __getitem__(self, pos):
        if pos < 0: raise Exception("Can't acess negative memory address ({}).".format(pos))

        if pos >= len(self.memory):
            self.memory += [0 for _ in range(pos+1-len(self.memory))]
        return self.memory[pos]

    def __setitem__(self, pos, data):
        if pos < 0: raise Exception("Can't acess negative memory address ({}).".format(pos))

        if pos >= len(self.memory):
            self.memory += [0 for _ in range(pos+1-len(self.memory))]
        self.memory[pos] = data

    def run(self, inputValue=None):
        if type(inputValue) is list:
            self.inputBuffer += inputValue
        elif inputValue is not None:
            self.inputBuffer.append(int(inputValue))

        while self.pc < len(self.memory):
            paramAndOpcode = "{:05}".format(self[self.pc])
            opcode = int(paramAndOpcode[-2:])
            modeC, modeB, modeA = [int(i) for i in paramAndOpcode[:3]]

            a, b, c = None, None, None
            if opcode in [4, 9]: # out, arb
                a = self.__parseMode(self[self.pc+1], modeA, "read")
                npc = self.pc+2
            elif opcode in [3]: # in
                a = self.__parseMode(self[self.pc+1], modeA, "write")
                npc = self.pc+2
            elif opcode in [5, 6]: # jit, jif
                a = self.__parseMode(self[self.pc+1], modeA, "read")
                b = self.__parseMode(self[self.pc+2], modeB, "read")
                npc = self.pc+3
            elif opcode in [1, 2, 7, 8]: # add, mul, lt, eq
                a = self.__parseMode(self[self.pc+1], modeA, "read")
                b = self.__parseMode(self[self.pc+2], modeB, "read")
                c = self.__parseMode(self[self.pc+3], modeC, "write")
                npc = self.pc+4

            if opcode == 1: # add
                self[c] = a + b
            elif opcode == 2: # mul
                self[c] = a * b
            elif opcode == 3: # in
                i = self.__getInput()
                if i is not None:
                    self[a] = i
                else:
                    return
            elif opcode == 4: # out
                self.output.append(a)
            elif opcode == 5: # jit
                if a != 0: npc = b
            elif opcode == 6: # jif
                if a == 0: npc = b
            elif opcode == 7: # lt
                self[c] = int(a < b)
            elif opcode == 8: # eq
                self[c] = int(a == b)
            elif opcode == 9: # arb
                self.base += a
            elif opcode == 99:
                break

            self.pc = npc

        self.halted = True
        return

def explore(start, startVM, moves):
    queue = deque([start])
    vms = {start: startVM}
    maze = {start: 1}
    while queue:
        cur = queue.popleft()

        for m in range(len(moves)):
            step = (cur[0]+moves[m][0], cur[1]+moves[m][1])
            if step not in maze:
                vms[step] = vms[cur].copy()
                vms[step].run(m+1)
                maze[step] = vms[step].output[-1]
                if maze[step] != 0:
                    queue.append(step)

    return maze

def findOxygen(start, moves):
    queue = deque([(start, 0)])
    visited = set([start])
    while queue:
        cur, dist = queue.popleft()

        if maze[cur] == 2:
            return (cur, dist)

        for move in moves:
            step = (cur[0]+move[0], cur[1]+move[1])
            if step not in visited:
                visited.add(cur)
                if maze[step] != 0:
                    queue.append((step, dist+1))

def timeToFill(maze, oxygen, moves):
    maxDist = 0

    queue = deque([(oxygen, 0)])
    visited = set([oxygen])
    while queue:
        cur, dist = queue.popleft()

        maxDist = max(maxDist, dist)

        for move in moves:
            step = (cur[0]+move[0], cur[1]+move[1])
            if step not in visited:
                visited.add(cur)
                if maze[step] != 0:
                    queue.append((step, dist+1))

    return maxDist

#################################

rawProgram = AOCUtils.loadInput(15)
memory = [int(i) for i in rawProgram.split(",")]

start = (0, 0)
moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
maze = explore(start, VM(memory), moves)

oxygen, distance = findOxygen(start, moves)
print("Part 1: {}".format(distance))

time = timeToFill(maze, oxygen, moves)
print("Part 2: {}".format(time))

AOCUtils.printTimeTaken()