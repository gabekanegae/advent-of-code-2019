from time import time

__startTime = None

def loadInput(day):
    global __startTime

    filename = "input" + "{:02}".format(day) + ".txt"

    with open("inputs/" + filename) as f:
        content = [l[:-1] if l[-1] == "\n" else l for l in f.readlines()]

    __startTime = time()

    if len(content) == 1:
        try:
            return int(content[0])
        except:
            try:
                return [int(i) for i in content[0].split()]
            except:
                return content[0]
    else:
        try:
            return [int(i) for i in content]
        except:
            return content

def printTimeTaken():
    global __startTime
    __endTime = time()
    print("Time: {:.3f}s".format(__endTime-__startTime))