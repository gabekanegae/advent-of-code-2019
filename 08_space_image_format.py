#####################################
# --- Day 8: Space Image Format --- #
#####################################

import AOCUtils

#####################################

w, h = 25, 6
image = [int(i) for i in str(AOCUtils.loadInput(8))]

layerAmt = len(image) // (w*h)

layers = []
layerCounts = []
for l in range(layerAmt):
    layer = []
    for x in range(h):
        s, e = l*w*h + x*w, l*w*h + (x+1)*w
        layer.append(image[s:e])

    layers.append(layer)

    lc0 = sum(l.count(0) for l in layer)
    lc1 = sum(l.count(1) for l in layer)
    lc2 = sum(l.count(2) for l in layer)
    layerCounts.append((lc0, lc1, lc2))

layerCounts.sort()
checksum = layerCounts[0][1] * layerCounts[0][2]

print("Part 1: {}".format(checksum))

image = [[None for _ in range(w)] for _ in range(h)]
for i in range(h):
    for j in range(w):
        for layer in layers:
            if image[i][j] is None and layer[i][j] != 2:
                image[i][j] = layer[i][j]

print("Part 2:")
for i in range(h):
    for j in range(w):
        if image[i][j] == 1:
            print("##", end="")
        else:
            print("  ", end="")
    print()

AOCUtils.printTimeTaken()