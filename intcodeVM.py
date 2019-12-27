import AOCUtils

OP_READ, OP_WRITE = False, True

class VM:
    def __init__(self, memory, pc=0, base=0):
        self.memory = memory[:]
        self.pc = pc
        self.base = base
        self.inputPtr = 0
        self.inputBuffer = []
        self.output = []
        self.halted = False

    # Returns a copy of itself (ignoring input and output buffer)
    def copy(self):
        return VM(self.memory, self.pc, self.base)

    def __parseMode(self, data, mode, op):
        if op == OP_READ:
            if mode == 0: return self[data]
            elif mode == 1: return data
            elif mode == 2: return self[self.base+data]
        elif op == OP_WRITE:
            if mode == 0: return data
            elif mode == 1: return data
            elif mode == 2: return self.base+data

    def __getInput(self):
        if self.inputPtr < len(self.inputBuffer):
            self.inputPtr += 1
            return self.inputBuffer[self.inputPtr-1]
        else:
            return None

    def __getitem__(self, pos):
        if pos < 0: raise Exception("Can't acess negative memory address ({}).".format(pos))

        if pos >= len(self.memory): # Extends memory to fit data request
            self.memory += [0 for _ in range(pos+1-len(self.memory))]
        return self.memory[pos]

    def __setitem__(self, pos, data):
        if pos < 0: raise Exception("Can't acess negative memory address ({}).".format(pos))

        if pos >= len(self.memory): # Extends memory to fit data request
            self.memory += [0 for _ in range(pos+1-len(self.memory))]
        self.memory[pos] = data

    def run(self, inputValue=None):
        # Load input into inputBuffer
        if type(inputValue) is list:
            self.inputBuffer += inputValue # Assumes list of ints
        elif type(inputValue) is str:
            self.inputBuffer += [ord(c) for c in inputValue]
        elif inputValue is not None:
            self.inputBuffer.append(int(inputValue))

        # Run VM
        while self.pc < len(self.memory):
            paramAndOpcode = "{:05}".format(self[self.pc])
            opcode = int(paramAndOpcode[-2:])
            modeC, modeB, modeA = [int(i) for i in paramAndOpcode[:3]]

            # Parse parameters according to modes and operation types
            a, b, c = None, None, None
            if opcode in [4, 9]: # out, arb
                a = self.__parseMode(self[self.pc+1], modeA, OP_READ)
                npc = self.pc+2
            elif opcode in [3]: # in
                a = self.__parseMode(self[self.pc+1], modeA, OP_WRITE)
                npc = self.pc+2
            elif opcode in [5, 6]: # jit, jif
                a = self.__parseMode(self[self.pc+1], modeA, OP_READ)
                b = self.__parseMode(self[self.pc+2], modeB, OP_READ)
                npc = self.pc+3
            elif opcode in [1, 2, 7, 8]: # add, mul, lt, eq
                a = self.__parseMode(self[self.pc+1], modeA, OP_READ)
                b = self.__parseMode(self[self.pc+2], modeB, OP_READ)
                c = self.__parseMode(self[self.pc+3], modeC, OP_WRITE)
                npc = self.pc+4

            # Execute operation
            if opcode == 1: # add
                self[c] = a + b
            elif opcode == 2: # mul
                self[c] = a * b
            elif opcode == 3: # in
                i = self.__getInput()
                
                # If no input is buffered, pause execution until some is given
                if i is not None:
                    self[a] = i
                else:
                    return
            elif opcode == 4: # out
                self.output.append(a)
            elif opcode == 5: # jit
                if a != 0: npc = b
            elif opcode == 6: # jif
                if a == 0: npc = b
            elif opcode == 7: # lt
                self[c] = int(a < b)
            elif opcode == 8: # eq
                self[c] = int(a == b)
            elif opcode == 9: # arb
                self.base += a
            elif opcode == 99: # hlt
                break

            # Update PC
            self.pc = npc

        self.halted = True
        return