##############################################
# --- Day 18: Many-Worlds Interpretation --- #
##############################################

import AOCUtils
from collections import deque

moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]

class Tunnels:
    def __init__(self, tunnels):
        self.tunnels = tunnels
        self.size = (len(tunnels), len(tunnels[0]))
        self.bots = []
        self.keys = dict()
        
        for x in range(len(tunnels)):
            for y in range(len(tunnels[0])):
                if tunnels[x][y] == "@":
                    self.keys[len(self.bots)] = (x, y)
                    self.bots.append((x, y))
                elif self.__isKey(tunnels[x][y]):
                    self.keys[tunnels[x][y]] = (x, y)

        self.keysToKeys = self.__getKeysToKeysDistance()

    def __isDoor(self, tile): return "A" <= tile <= "Z"
    def __isKey(self, tile): return "a" <= tile <= "z"

    def __getKeysToKeysDistance(self):
        # Dict of dicts with (distance from keyA to keyB, doors inbetween)
        keysToKeys = {k: dict() for k in self.keys}
        
        for keyA, posKeyA in self.keys.items():
            queue = deque([(posKeyA, 0, [])])
            visited = set()

            while queue:
                cur, dist, doors = queue.popleft()
                curTile = self.tunnels[cur[0]][cur[1]]

                if cur in visited: continue
                visited.add(cur)

                newDoors = doors[:]
                if self.__isDoor(curTile):
                    newDoors.append(curTile)

                keyB = curTile
                if keyB != keyA and self.__isKey(keyB):
                    keysToKeys[keyA][keyB] = (dist, newDoors)
                    keysToKeys[keyB][keyA] = (dist, newDoors)

                for m in moves:
                    step = (cur[0]+m[0], cur[1]+m[1])
                    stepTile = self.tunnels[step[0]][step[1]]
                    if stepTile != "#":
                        queue.append((step, dist+1, newDoors))

        return keysToKeys

    def reachableKeys(self, bots, inventory):
        reachable = dict()
        for botID, botPos in enumerate(bots):
            botTile = self.tunnels[botPos[0]][botPos[1]]
            if botTile == "@": botTile = botID # Not a key, but a bot

            for keyB, (dist, newDoors) in self.keysToKeys[botTile].items():
                # If there are locked doors between keyA and keyB, it can't be reached
                if not set([d.lower() for d in newDoors]).issubset(set(inventory)): continue

                # If keyB is already taken, ignore it
                if keyB in inventory: continue

                reachable[keyB] = (self.keys[keyB], dist, botID)

        return reachable

    def distanceToAllKeys(self):
        memo = dict() # Memoization of distanceToAllKeys given (bots, inventory)

        def exploreRecursive(bots, inventory):
            memoKey = (tuple(sorted(bots)), tuple(sorted(inventory)))
            if memoKey in memo: return memo[memoKey]

            distances = []
            for key, (pos, dist, botID) in self.reachableKeys(bots, inventory).items():
                if type(key) is int: continue # If not a key but a bot, ignore it

                # "Teleport" bot to key
                newBots = bots[:]
                newBots[botID] = pos

                # Add key to inventory
                newInventory = set(inventory) | set(key)

                # Add to possible paths (recurse)
                distances.append(dist + exploreRecursive(newBots, newInventory))

            # If no keys are reachable, minDistance is 0
            minDistance = min(distances) if distances else 0

            memo[memoKey] = minDistance
            return minDistance

        return exploreRecursive(self.bots, set())

    # def __repr__(self):
    #     s = ""
    #     for line in self.tunnels:
    #         s += "".join(line) + "\n"
    #     return s

##############################################

rawTunnels = [list(s) for s in AOCUtils.loadInput(18)]

tunnels = Tunnels(rawTunnels)
print("Part 1: {}".format(tunnels.distanceToAllKeys()))

# Modify map center according to instructions
pos = tunnels.bots[0]
for w in [(-1, 0), (0, 0), (1, 0), (0, -1), (0, 1)]:
    rawTunnels[pos[0]+w[0]][pos[1]+w[1]] = "#"
for p in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
    rawTunnels[pos[0]+p[0]][pos[1]+p[1]] = "@"

tunnels = Tunnels(rawTunnels)
print("Part 2: {}".format(tunnels.distanceToAllKeys()))

AOCUtils.printTimeTaken()