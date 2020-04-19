##############################
# --- Day 20: Donut Maze --- #
##############################

import AOCUtils
from collections import deque

class Maze:
    def __init__(self, rawMaze):
        self.maze = [s[:] for s in rawMaze]
        self.start, self.end = None, None
        self.size = (len(rawMaze), len(rawMaze[0]))

        rawInner, rawOuter = dict(), dict()
        for y in range(self.size[0]):
            for x in range(self.size[1]):
                portalName, portalPos = self.__parsePortal((y, x))
                if not portalName or not portalPos: continue

                if portalName == "AA":
                    self.start = portalPos
                elif portalName == "ZZ":
                    self.end = portalPos
                else:
                    if 1 < y < self.size[0]-2 and 1 < x < self.size[1]-2:
                        rawInner[portalName] = portalPos
                    else:
                        rawOuter[portalName] = portalPos

        self.outerPortals = {v: rawInner[k] for k, v in rawOuter.items()}
        self.innerPortals = {v: rawOuter[k] for k, v in rawInner.items()}

    def __isPortal(self, pos):
        return 0 <= pos[0] <= self.size[0] and 0 <= pos[1] <= self.size[1] and "A" <= self.maze[pos[0]][pos[1]] <= "Z"
    def __isWalkable(self, pos):
        return 0 <= pos[0] <= self.size[0] and 0 <= pos[1] <= self.size[1] and self.maze[pos[0]][pos[1]] == "."

    def __parsePortal(self, pos):
        if not self.__isPortal(pos): return None, None
        
        y, x = pos
        name, pos = None, None
        if self.__isPortal((y+1, x)): # Vertical (top-to-bottom)
            name = self.maze[y][x] + self.maze[y+1][x]

            # Find portal entrance
            if self.__isWalkable((y-1, x)): # Up
                pos = (y-1, x)
            elif self.__isWalkable((y+2, x)): # Down
                pos = (y+2, x)

            self.maze[y][x], self.maze[y+1][x] = " ", " " # Erase portal
        elif self.__isPortal((y, x+1)): # Horizontal (left-to-right)
            name = self.maze[y][x] + self.maze[y][x+1]

            # Find portal entrance
            if self.__isWalkable((y, x-1)): # Left
                pos = (y, x-1)
            elif self.__isWalkable((y, x+2)): # Right
                pos = (y, x+2)

            self.maze[y][x], self.maze[y][x+1] = " ", " " # Erase portal

        return name, pos

    def getMinDistance(self):
        queue = deque([(self.start, 0)])
        visited = set()
        while queue:
            cur, dist = queue.popleft()

            if cur in visited: continue
            visited.add(cur)

            if cur == self.end: break

            # Inner and outer portals have the same behavior
            if cur in self.innerPortals:
                queue.append((self.innerPortals[cur], dist+1))
            elif cur in self.outerPortals:
                queue.append((self.outerPortals[cur], dist+1))
            
            for m in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                step = (cur[0]+m[0], cur[1]+m[1])
                if self.__isWalkable(step):
                    queue.append((step, dist+1))

        return dist

    def getMinDistanceLayers(self):
        queue = deque([(self.start, 0, 0)])
        visited = set()
        while queue:
            cur, level, dist = queue.popleft()

            if (cur, level) in visited: continue
            visited.add((cur, level))

            # End can only be reached if at level 0
            if level == 0 and cur == self.end: break

            # Outer portals decrease level and can only be accessed at level > 0
            # Inner portals increase level, can be accessed at any level
            if level > 0 and cur in self.outerPortals:
                queue.append((self.outerPortals[cur], level-1, dist+1))
            elif cur in self.innerPortals:
                queue.append((self.innerPortals[cur], level+1, dist+1))

            for m in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                step = (cur[0]+m[0], cur[1]+m[1])
                if self.__isWalkable(step):
                    queue.append((step, level, dist+1))

        return dist

###########################

rawMaze = [list(s) for s in AOCUtils.loadInput(20)]
maze = Maze(rawMaze)

print("Part 1: {}".format(maze.getMinDistance()))

print("Part 2: {}".format(maze.getMinDistanceLayers()))

AOCUtils.printTimeTaken()