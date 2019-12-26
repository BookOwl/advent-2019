from enum import IntEnum

class Opcode(IntEnum):
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    JT = 5
    JF = 6
    LT = 7
    EQ = 8
    HALT = 99
    def num_args(self):
        if self.value in (Opcode.ADD, Opcode.MUL, Opcode.LT, Opcode.EQ):
            return 3
        elif self.value in (Opcode.JT, Opcode.JF):
            return 2
        elif self.value in (Opcode.HALT, Opcode.INPUT, Opcode.OUTPUT):
            return 1
        else:
            raise InvalidInstruction

class ParamMode(IntEnum):
    Positon = 0
    Immediate = 1

class Instruction:
    def __init__(self, x):
        op = x % 100
        self.op = Opcode(op)
        self.num_args = self.op.num_args()
        self.modes = [ParamMode(x // 10**n % 10) for n in range(2, 2+self.num_args)]
    def __repr__(self):
        return f"<Instruction {repr(self.op)} Mode {self.modes}>"


class InvalidInstruction(Exception):
    pass

class Computer:
    def __init__(self, program = None):
        if program:
            self.load_program(program)

    def load_program(self, program):
        self.memory = [int(cell.strip()) for cell in program.split(",")]
        self.ip = 0
        self.done = False

    def value_of(self, addr, mode):
        if mode == ParamMode.Positon:
            return self.memory[addr]
        else:
            return addr

    def write(self, addr, value):
        self.memory[addr] = value

    def get_params(self, i):
        return zip(self.memory[self.ip+1:self.ip+i.num_args+1], i.modes)

    def step(self):
        i = Instruction(self.memory[self.ip])
        #print(self.memory[self.ip], i)
        #print(list(self.get_params(i)))
        if i.op == Opcode.ADD:
            a, b, dest = self.get_params(i)
            self.write(dest[0], self.value_of(*a) + self.value_of(*b))
        elif i.op == Opcode.MUL:
            a, b, dest = self.get_params(i)
            self.write(dest[0], self.value_of(*a) * self.value_of(*b))
        elif i.op == Opcode.LT:
            a, b, dest = self.get_params(i)
            self.write(dest[0], int(self.value_of(*a) < self.value_of(*b)))
        elif i.op == Opcode.EQ:
            a, b, dest = self.get_params(i)
            self.write(dest[0], int(self.value_of(*a) == self.value_of(*b)))
        elif i.op == Opcode.JF:
            a, target = self.get_params(i)
            if self.value_of(*a) == 0:
                self.ip = self.value_of(*target)
                return
        elif i.op == Opcode.JT:
            a, target = self.get_params(i)
            if self.value_of(*a) != 0:
                self.ip = self.value_of(*target)
                return
        elif i.op == Opcode.INPUT:
            dest, *_ = self.get_params(i)
            self.write(dest[0], int(input("> ")))
        elif i.op == Opcode.OUTPUT:
            a, *_ = self.get_params(i)
            print(self.value_of(*a))
        elif i.op == Opcode.HALT:
            self.done = True
        else:
            raise InvalidInstruction(f"Invalid opcode '{repr(i.op)}'")
        self.ip += i.num_args + 1

    def run(self):
        while not self.done:
            self.step()
