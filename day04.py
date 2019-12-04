###################################
# --- Day 4: Secure Container --- #
###################################

import AOCUtils

###################################

pwRange = [int(i) for i in AOCUtils.loadInput(4).split("-")]

passwords1 = set()
for pw in range(pwRange[0], pwRange[1]+1):
    hasRepeat, neverDecreases = False, True
    pw = str(pw)

    for i in range(len(pw)-1):
        if pw[i+1] < pw[i]:
            neverDecreases = False
            break
        if pw[i+1] == pw[i]:
            hasRepeat = True

    if hasRepeat and neverDecreases:
        passwords1.add(pw)

print("Part 1: {}".format(len(passwords1)))

passwords2 = set()
for pw in passwords1:
    sequences = [1]

    for i in range(len(pw)-1):
        if pw[i+1] == pw[i]:
            sequences[-1] += 1
        else:
            sequences.append(1)

    if 2 in sequences:
        passwords2.add(pw)

print("Part 2: {}".format(len(passwords2)))

AOCUtils.printTimeTaken()