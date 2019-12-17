##################################
# --- Day 17: Set and Forget --- #
##################################

import AOCUtils

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

class BotCam:
    def __init__(self, cam):
        self.cam = [list(line) for line in cam]
        self.size = (len(cam), len(cam[0]))
        self.botPos, self.botFacing = None, None

        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if self.cam[x][y] != "." and self.cam[x][y] != "#":
                    self.botPos, self.botFacing = (x, y), self.cam[x][y]
                    self.cam[x][y] = "#"

    def sumIntersections(self):
        total = 0
        for x in range(1, self.size[0]-2):
            for y in range(1, self.size[1]-2):
                if self.cam[x][y] != "#": continue
                if self.cam[x-1][y] == self.cam[x+1][y] == self.cam[x][y-1] == self.cam[x][y+1]:
                    total += x*y

        return total

    def __rotate(self, direction):
        faces = "^>v<"
        if direction == "R":
            newFace = (faces.index(self.botFacing)+1) % len(faces)
        elif direction == "L":
            newFace = (faces.index(self.botFacing)-1) % len(faces)
        return faces[newFace]

    def getPath(self):
        moves = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}

        path = []
        while True:
            nxtTile = {"fwd": moves[self.botFacing], "left": moves[self.__rotate("L")], "right": moves[self.__rotate("R")]}
            nxtStep = {"fwd": None, "left": None, "right": None}
            for k, v in nxtTile.items():
                if not (0 <= self.botPos[0]+v[0] < self.size[0]): continue
                if not (0 <= self.botPos[1]+v[1] < self.size[1]): continue
                if self.cam[self.botPos[0]+v[0]][self.botPos[1]+v[1]] == "#":
                    nxtStep[k] = (self.botPos[0]+v[0], self.botPos[1]+v[1])

            # Always go forward, if possible
            if nxtStep["fwd"]:
                self.botPos = nxtStep["fwd"]
                path[-1] += 1
            elif nxtStep["left"]:
                self.botPos = nxtStep["left"]
                self.botFacing = self.__rotate("L")
                path += ["L", 1]
            elif nxtStep["right"]:
                self.botPos = nxtStep["right"]
                self.botFacing = self.__rotate("R")
                path += ["R", 1]
            else:
                return path

    # def __repr__(self):
    #     s = ""
    #     for line in self.cam:
    #         s += "".join(line)
    #         s += "\n"
    #     return s

def formatInput(s): return ",".join([str(c) for c in s])
def countSub(l, s): return sum([l[i:i+len(s)] == s for i in range(len(l))])

def replaceSub(l, f, r):
    nl = []
    i = 0
    while i < len(l):
        if l[i:i+len(f)] == f:
            nl.append("ABC"[r])
            i += len(f)
        else:
            nl.append(l[i])
            i += 1
    return nl

#################################

rawProgram = AOCUtils.loadInput(17)
memory = [int(i) for i in rawProgram.split(",")]

vm = VM(memory)
vm.run()

cam = "".join([chr(c) for c in vm.output]).split()
botcam = BotCam(cam)

print("Part 1: {}".format(botcam.sumIntersections()))

path = botcam.getPath()

main = path[:]
funcs = []
for i in range(3):
    lastGoodFunc = []
    curFunc = []

    curPos = 0
    while main[curPos] in "ABC": curPos += 1

    while True:
        curFunc += main[curPos:curPos+2]
        curPos += 2
        
        # Formatted input can't be longer than 20
        if len(formatInput(curFunc)) > 20: break
        
        # Assume that each function will appear at least thrice
        if countSub(main, curFunc) < 3: break

        lastGoodFunc = curFunc[:]

    main = replaceSub(main, lastGoodFunc, i)
    funcs.append(lastGoodFunc)

main = formatInput(main)
A, B, C = [formatInput(f) for f in funcs]
videoFeed = "n"

rawBotInput = "\n".join([main, A, B, C, videoFeed])+"\n"
botInput = [ord(c) for c in rawBotInput]

vm = VM(memory)
vm[0] = 2
vm.run(botInput)
print("Part 2: {}".format(vm.output[-1]))

AOCUtils.printTimeTaken()