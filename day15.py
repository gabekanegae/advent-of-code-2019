#################################
# --- Day 15: Oxygen System --- #
#################################

import AOCUtils
from intcodeVM import VM
from collections import deque

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

def findOxygen(maze, start, moves):
    queue = deque([(start, 0)])
    visited = set()
    while queue:
        cur, dist = queue.popleft()

        if cur in visited: continue
        visited.add(cur)

        if maze[cur] == 2:
            return (cur, dist)

        for move in moves:
            step = (cur[0]+move[0], cur[1]+move[1])
            if maze[step] != 0:
                queue.append((step, dist+1))

def timeToFill(maze, oxygen, moves):
    maxDist = 0

    queue = deque([(oxygen, 0)])
    visited = set()
    while queue:
        cur, dist = queue.popleft()

        if cur in visited: continue
        visited.add(cur)

        maxDist = max(maxDist, dist)

        for move in moves:
            step = (cur[0]+move[0], cur[1]+move[1])
            if maze[step] != 0:
                queue.append((step, dist+1))

    return maxDist

#################################

rawProgram = AOCUtils.loadInput(15)
memory = [int(i) for i in rawProgram.split(",")]

start = (0, 0)
moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
maze = explore(start, VM(memory), moves)

oxygen, distance = findOxygen(maze, start, moves)
print("Part 1: {}".format(distance))

time = timeToFill(maze, oxygen, moves)
print("Part 2: {}".format(time))

AOCUtils.printTimeTaken()