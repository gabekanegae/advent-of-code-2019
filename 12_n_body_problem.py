######################################
# --- Day 12: The N-Body Problem --- #
######################################

import AOCUtils
from math import gcd

class Moon:
    def __init__(self, rawPos, vel=None):
        self.pos = [int(c.split("=")[1]) for c in rawPos[1:-1].split(",")]
        self.vel = vel or [0, 0, 0]

    def getState(self, c):
        return (self.pos[c], self.vel[c])

class MoonSystem:
    def __init__(self, moons):
        self.moons = moons

    def step(self):
        for c in range(3):
            for mooni in self.moons:
                for moonj in self.moons:
                    if mooni is moonj: continue
                    if mooni.pos[c] > moonj.pos[c]:
                        mooni.vel[c] -= 1
                    elif mooni.pos[c] < moonj.pos[c]:
                        mooni.vel[c] += 1

            for mooni in self.moons:
                mooni.pos[c] += mooni.vel[c]

    def getTotalEnergy(self):
        pot = [sum(abs(x) for x in moon.pos) for moon in self.moons]
        kin = [sum(abs(x) for x in moon.vel) for moon in self.moons]
        return sum(p*k for p, k in zip(pot, kin))

    def getState(self, c):
        return str([moon.getState(c) for moon in self.moons])

# Get LCM of 2 values
def lcm2(x, y):
    return abs(x*y) // gcd(x,y)

# Get LCM of a list of N values
def lcmN(a):
    l = lcm2(a[0], a[1])
    for i in a[2:]:
        l = lcm2(l, i)
    
    return l

######################################

rawMoons = AOCUtils.loadInput(12)
moons = [Moon(rawMoon) for rawMoon in rawMoons]

system = MoonSystem(moons)
for _ in range(1000):
    system.step()

print("Part 1: {}".format(system.getTotalEnergy()))

# Find periods of each axis
periods = [0 for _ in range(3)]
seen = [set() for _ in range(3)]

system = MoonSystem(moons)
step = 0
while not all(periods):
    for c in range(3):
        if not periods[c]:
            state = system.getState(c)
            if state in seen[c]:
                periods[c] = step
            else:
                seen[c].add(state)

    system.step()
    step += 1

# Get LCM of all periods
print("Part 2: {}".format(lcmN(periods)))

AOCUtils.printTimeTaken()