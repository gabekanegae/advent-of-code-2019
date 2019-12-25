##############################
# --- Day 25: Cryostasis --- #
##############################

import AOCUtils
from itertools import combinations
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

def playGame(memory):
    vm = VM(memory)
    vm.run()
    print("".join([chr(c) for c in vm.output]))
    while not vm.halted:
        vm.output = []
        vm.run(input()+"\n")
        print("".join([chr(c) for c in vm.output]))
    exit()

def oppositeDoor(direction):
    opp = {"north": "south", "south": "north", "east": "west", "west": "east"}
    return opp[direction]

##############################

rawProgram = AOCUtils.loadInput(25)
memory = [int(i) for i in rawProgram.split(",")]

# The game can be played manually by uncommenting the line below:
# playGame(memory)

# Items that can't (shouldn't) be picked up
blacklist = set(["infinite loop", "molten lava", "giant electromagnet", "photons", "escape pod"])

vm = VM(memory)
vm.run()

# Store the command list that reaches the final room with the maximum amount of items
maxInventorySize, maxInventoryState = 0, None

# BFS through all rooms, storing (room, inventory) visited states
visited = set()
queue = deque([(set(), [], vm)])
while queue:
    inventory, path, vm = queue.popleft()

    # Save output and clear it
    text = "".join([chr(c) for c in vm.output])
    vm.output = []

    # Get room name
    room = text.split("==")[1].strip()
    # print(room, "-->", sorted(inventory))

    if (room, tuple(inventory)) in visited: continue
    visited.add((room, tuple(inventory)))

    # Parse room's doors and items
    doors, items = [], []
    doorsStart = text.find("Doors here lead:")
    itemsStart = text.find("Items here:")
    if doorsStart != -1:
        doors = [line[2:] for line in text[doorsStart:itemsStart].split("\n") if line.startswith("-")]
    if itemsStart != -1:
        items = [line[2:] for line in text[itemsStart:].split("\n") if line.startswith("-")]

    # If at Security Checkpoint (final room before floor)
    if room == "Security Checkpoint":
        if len(inventory) > maxInventorySize: # Update best answer (vm, inventory, floorDirection)
            floorDirection = [door for door in doors if door not in [path[-1], oppositeDoor(path[-1])]][0]
            maxInventorySize, maxInventoryState = len(inventory), (vm, list(inventory), floorDirection)
        doors = [oppositeDoor(path[-1])] # Only go back, don't go to the pressure-sensitive floor
    
    # Pick up all items on the floor
    for item in items:
        if item in blacklist: continue # But ignore the game-ending ones
        path.append("take " + item)
        vm.run("take " + item + "\n")
        inventory.add(item)

    # Queue all next steps, copying the current VM for each one
    for door in doors:
        newVM = vm.copy()
        newVM.run(door+"\n")

        queue.append((set(inventory), path+[door], newVM))

# Get VM at the checkpoint, list of all safe items and direction of pressure-sensitive floor
vm, allItems, floorDirection = maxInventoryState

# Store all sets of items that are too heavy (can't be a subset of the final answer)
tooHeavy = []

# Drop all items before going on the floor
vm.run("\n".join(["drop "+item for item in allItems])+"\n")

# Bruteforce the pressure floor by trying all item combinations
inventory = set()
done = False
for n in range(len(allItems)): # Try combinations by increasing length
    if done: break
    for attemptItems in combinations(allItems, n):
        # print("Trying items: {}".format(list(attemptItems)))

        # Check against the invalid subsets, faster than doing it in-game
        if any([set(s).issubset(set(attemptItems)) for s in tooHeavy]): continue

        # Drop all items that aren't in attemptItems
        toDrop = [item for item in inventory if item not in attemptItems]
        vm.run("\n".join(["drop "+item for item in toDrop])+"\n")
        inventory = inventory.difference(set(toDrop))

        # Pick up all from attemptItems that aren't yet in inventory
        toPick = [item for item in attemptItems if item not in inventory]
        vm.run("\n".join(["take "+item for item in toPick])+"\n")
        inventory = inventory.union(set(toPick))

        # Activate floor
        vm.run(floorDirection+"\n")

        # Verify result
        output = "".join([chr(c) for c in vm.output])
        if output.find("Alert!") == -1:
            # print(output)
            print("Part 1: {}".format(output.split()[-8]))
            done = True
            break
        elif output.find("lighter") != -1: # Too heavy, add as invalid subset
            tooHeavy.append(attemptItems)

        vm.output = []

AOCUtils.printTimeTaken()