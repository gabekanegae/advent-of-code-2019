#################################################
# --- Day 16: Flawed Frequency Transmission --- #
#################################################

import AOCUtils

def getMultiplier(pos, i):
    pattern = [0, 1, 0, -1]
    if i < pos:
        return pattern[0]
    else:
        i = ((i-pos) // (pos+1)) + 1
        return pattern[i%len(pattern)]

#################################################

signal = [int(i) for i in str(AOCUtils.loadInput(16))]
size = len(signal)

for _ in range(100):
    for i in range(size):
        newSignal = sum(signal[j] * getMultiplier(i, j) for j in range(size))
        signal[i] = abs(newSignal) % 10

firstEight = "".join(str(i) for i in signal[:8])
print("Part 1: {}".format(firstEight))

signal = [int(i) for i in str(AOCUtils.loadInput(16))] * 10000
offset = int("".join(str(i) for i in signal[:7]))
signal = signal[offset:]
size = len(signal)

# Partial Sum (% 10), assuming offset > size/2
for _ in range(100):
    total = 0
    for i in range(size, 0, -1):
        total = (total + signal[i-1]) % 10
        signal[i-1] = total

message = "".join(str(i) for i in signal[:8])
print("Part 2: {}".format(message))

AOCUtils.printTimeTaken()