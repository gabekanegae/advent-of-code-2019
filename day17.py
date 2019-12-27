##################################
# --- Day 17: Set and Forget --- #
##################################

import AOCUtils
from intcodeVM import VM

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
    #         s += "".join(line) + "\n"
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

##################################

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
        
        # Assumes that each function will appear at least thrice
        if countSub(main, curFunc) < 3: break

        lastGoodFunc = curFunc[:]

    main = replaceSub(main, lastGoodFunc, i)
    funcs.append(lastGoodFunc)

main = formatInput(main)
A, B, C = [formatInput(f) for f in funcs]
videoFeed = "n"

vm = VM(memory)
vm[0] = 2
vm.run("\n".join([main, A, B, C, videoFeed])+"\n")
print("Part 2: {}".format(vm.output[-1]))

AOCUtils.printTimeTaken()