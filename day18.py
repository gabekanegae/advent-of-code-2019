##############################################
# --- Day 18: Many-Worlds Interpretation --- #
##############################################

import AOCUtils
from collections import deque

class Tunnels:
    def __init__(self, tunnels):
        self.tunnels = tunnels
        self.size = (len(tunnels), len(tunnels[0]))
        self.bots = []
        for x in range(len(tunnels)):
            for y in range(len(tunnels[0])):
                if tunnels[x][y] == "@":
                    self.bots.append((x, y))
                    self.tunnels[x][y] = "."

    def __isDoor(self, tile): return "A" <= tile <= "Z"
    def __isKey(self, tile): return "a" <= tile <= "z"

    def reachableKeys(self, bots, inventory):
        reachable = dict()
        for botID, botPos in enumerate(bots):
            queue = deque([(botPos, 0)])
            visited = set()

            while queue:
                cur, dist = queue.popleft()
                curTile = self.tunnels[cur[0]][cur[1]]

                if cur in visited: continue
                visited.add(cur)

                # If a key is found, take it but don't go further
                if self.__isKey(curTile) and curTile not in inventory:
                    reachable[curTile] = (cur, dist, botID)
                    continue

                for m in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                    step = (cur[0]+m[0], cur[1]+m[1])
                    stepTile = self.tunnels[step[0]][step[1]]
                    if stepTile != "#" and (not self.__isDoor(stepTile) or stepTile.lower() in inventory):
                        queue.append((step, dist+1))

        return reachable

    def distanceToAllKeys(self):
        memo = dict() # Memoization of distanceToAllKeys given (bots, inventory)

        def exploreRecursive(bots, inventory):
            memoKey = (tuple(sorted(bots)), tuple(sorted(inventory)))
            if memoKey in memo:
                return memo[memoKey]

            distances = []
            for key, (pos, dist, botID) in self.reachableKeys(bots, inventory).items():
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

# Modify center of map according to instructions
pos = tunnels.bots[0]
for w in [(-1, 0), (0, 0), (1, 0), (0, -1), (0, 1)]:
    rawTunnels[pos[0]+w[0]][pos[1]+w[1]] = "#"
for p in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
    rawTunnels[pos[0]+p[0]][pos[1]+p[1]] = "@"

tunnels = Tunnels(rawTunnels)
print("Part 2: {}".format(tunnels.distanceToAllKeys()))

AOCUtils.printTimeTaken()