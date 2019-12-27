##############################
# --- Day 25: Cryostasis --- #
##############################

import AOCUtils
from intcodeVM import VM
from itertools import combinations
from collections import deque

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