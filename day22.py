################################
# --- Day 22: Slam Shuffle --- #
################################

import AOCUtils

# Modular inverse of n (assumes mod is prime, uses Euler's Theorem)
def modinv(n, mod):
    return pow(n, mod-2, mod)

################################

shuffle = AOCUtils.loadInput(22)
size = 10007

deck = list(range(size))
for step in shuffle:
    if step == "deal into new stack":
        deck.reverse()
    elif step.startswith("cut"):
        n = int(step.split()[-1])
        deck = deck[n:] + deck[:n]
    elif step.startswith("deal with increment"):
        n = int(step.split()[-1])
        ndeck = [None for _ in range(size)]
        for i in range(size):
            ndeck[(i*n)%size] = deck[i]
        deck = ndeck

card = 2019
print("Part 1: {}".format(deck.index(card)))

# Define deck by (offset, increment, size)
# Position of card N can be taken by ((offset + increment * N) % size)
size = 119315717514047
offset, increment = 0, 1
for step in shuffle:
    if step == "deal into new stack":
        increment *= -1
        offset += increment
    elif step.startswith("cut"):
        n = int(step.split()[-1])
        offset += increment * n
    elif step.startswith("deal with increment"):
        n = int(step.split()[-1])
        increment *= modinv(n, size)

iterations = 101741582076661

# Get offset and increment after iterations
n = (1-increment) % size
itIncrement = pow(increment, iterations, size)
itOffset = (offset * (1-itIncrement) * modinv(n, size)) % size # Geometric series

card = 2020
cardPosition = (itOffset + itIncrement * card) % size
print("Part 2: {}".format(cardPosition))

AOCUtils.printTimeTaken()