##############################
# --- Day 25: Cryostasis --- #
##############################

import AOCUtils
from itertools import combinations

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
        elif type(inputValue) is str:
            self.inputBuffer += [ord(c) for c in inputValue]
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

##############################

rawProgram = AOCUtils.loadInput(25)
memory = [int(i) for i in rawProgram.split(",")]

# Play the game manually (by uncommenting the code block below) until you pick up
# all safe items and activate the pressure-sensitive floor. Then, edit the "save"
# list below with the commands used.

# vm = VM(memory)
# vm.run()
# print("".join([chr(c) for c in vm.output]))
# while not vm.halted:
#     vm.run(input()+"\n")
#     print("".join([chr(c) for c in vm.output]))
#     vm.output = []
# exit()

save = ["north",
"take easter egg",
"east",
"take astrolabe",
"south",
"take space law space brochure",
"north",
"north",
"north",
"take fuel cell",
"south",
"south",
"west",
"north",
"take manifold",
"north",
"north",
"take hologram",
"north",
"take weather machine",
"north",
"take antenna",
"west",
"south"] # Last command activates floor

items = [s[5:] for s in save if s.startswith("take")]

tooHeavy = [] # Store all sets of items that are too heavy (can't be a subset of the answer)

# Start game, run command list collecting all items and drop them before the sensitive floor
vm = VM(memory)
vm.run("\n".join(save[:-1])+"\n")
vm.run("\n".join(["drop "+item for item in items])+"\n")

# Bruteforce the pressure floor by trying all item combinations
curItems = set()
done = False
for n in range(len(items)+1): # Try combinations by increasing length
    if done: break
    for pickedItems in combinations(items, n):
        # print("Trying items: {}".format(list(pickedItems)))

        # Check against the invalid subsets, faster than doing it in-game
        if any([set(s).issubset(set(pickedItems)) for s in tooHeavy]): continue

        # Drop all items that aren't part of pickedItems
        toDrop = [item for item in curItems if item not in pickedItems]
        vm.run("\n".join(["drop "+item for item in toDrop])+"\n")
        curItems = curItems.difference(set(toDrop))

        # Pick up all from pickedItems that it doesn't have yet
        toPick = [item for item in pickedItems if item not in curItems]
        vm.run("\n".join(["take "+item for item in toPick])+"\n")
        curItems = curItems.union(set(toPick))

        # Activate floor
        vm.run(save[-1]+"\n")

        # Verify result
        output = "".join([chr(c) for c in vm.output])
        if output.find("Alert!") == -1:
            # print(output)
            print("Part 1: {}".format(output.split()[-8]))
            done = True
            break
        elif output.find("lighter") != -1: # Too heavy, add as invalid subset
            tooHeavy.append(pickedItems)

        vm.output = []

AOCUtils.printTimeTaken()