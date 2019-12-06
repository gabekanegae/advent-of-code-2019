######################################
# --- Day 6: Universal Orbit Map --- #
######################################

import AOCUtils
from collections import deque

class Tree:
    def __init__(self, children):
        self.root = Node("COM", 0)
        self.checksum = 0
        self.depths = {"COM": 0}

        queue = deque([self.root])
        while queue:
            cur = queue.popleft()
            if cur.name not in children: continue

            depth = self.depths[cur.name] + 1
            for childName in children[cur.name]:
                cur.children.append(Node(childName, depth))
                self.depths[childName] = depth

            queue += cur.children

        self.checksum = sum(self.depths.values())

    def getPath(self, name):
        queue = deque([(self.root, [])])
        while queue:
            cur, path = queue.popleft()

            if cur.name == name:
                return path + [name]

            for child in cur.children:
                newPath = path + [cur.name]
                queue.append((child, newPath))

    def getLCA(self, nameA, nameB):
        pathA = self.getPath(nameA)
        pathB = self.getPath(nameB)

        minLen = min(len(pathA), len(pathB))
        for i in range(minLen):
            if pathA[i] != pathB[i]:
                return pathA[i-1]

class Node:
    def __init__(self, name, depth):
        self.name = name
        self.children = []

######################################

orbits = [s.split(")") for s in AOCUtils.loadInput(6)]

children = dict()
for orb in orbits:
    if orb[0] not in children:
        children[orb[0]] = []
    children[orb[0]].append(orb[1])

tree = Tree(children)

print("Part 1: {}".format(tree.checksum))

lca = tree.getLCA("YOU", "SAN")
dist = tree.depths["YOU"] + tree.depths["SAN"] - 2*tree.depths[lca] - 2
print("Part 2: {}".format(dist))

AOCUtils.printTimeTaken()