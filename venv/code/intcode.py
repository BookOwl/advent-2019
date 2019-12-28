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
    REL = 9
    HALT = 99
    def num_args(self):
        if self.value in (Opcode.ADD, Opcode.MUL, Opcode.LT, Opcode.EQ):
            return 3
        elif self.value in (Opcode.JT, Opcode.JF):
            return 2
        elif self.value in (Opcode.HALT, Opcode.INPUT, Opcode.OUTPUT, Opcode.REL):
            return 1
        else:
            raise InvalidInstruction

class ParamMode(IntEnum):
    Positon = 0
    Immediate = 1
    Relative = 2

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
    def __init__(self, program = None, in_=None, out=None):
        self.set_io(in_, out)
        if program:
            self.load_program(program)

    def load_program(self, program):
        self.memory = [int(cell.strip()) for cell in program.split(",")]
        self.mem_len = len(self.memory)
        self.rel_base = 0
        self.ip = 0
        self.done = False
        self.outputting = False

    def set_io(self, in_ = None, out = None):
        self.in_ = in_ or input
        self.out = out or print

    def value_of(self, addr, mode):
        if mode == ParamMode.Positon:
            if addr >= self.mem_len:
                self.memory += [0] * ((addr - self.mem_len) * 2)
                self.mem_len = len(self.memory)
            return self.memory[addr]
        elif mode == ParamMode.Relative:
            addr = addr + self.rel_base
            if addr >= self.mem_len:
                self.memory += [0] * ((addr - self.mem_len) * 2)
                self.mem_len = len(self.memory)
            return self.memory[addr]
        else:
            return addr

    def write(self, addr, value):
        addr, mode = addr
        if mode == ParamMode.Relative:
            addr += self.rel_base
        if addr >= self.mem_len:
            self.memory += [0] * ((addr - self.mem_len) * 2)
            self.mem_len = len(self.memory)
        self.memory[addr] = value

    def get_params(self, i):
        return zip(self.memory[self.ip+1:self.ip+i.num_args+1], i.modes)

    def step(self):
        self.outputting = False
        i = Instruction(self.memory[self.ip])
       # print(self.memory[self.ip], i)
        #print(list(self.get_params(i)))
        if i.op == Opcode.ADD:
            a, b, dest = self.get_params(i)
            self.write(dest, self.value_of(*a) + self.value_of(*b))
        elif i.op == Opcode.MUL:
            a, b, dest = self.get_params(i)
            self.write(dest, self.value_of(*a) * self.value_of(*b))
        elif i.op == Opcode.LT:
            a, b, dest = self.get_params(i)
            self.write(dest, int(self.value_of(*a) < self.value_of(*b)))
        elif i.op == Opcode.EQ:
            a, b, dest = self.get_params(i)
            self.write(dest, int(self.value_of(*a) == self.value_of(*b)))
        elif i.op == Opcode.REL:
            a = next(self.get_params(i))
            self.rel_base += self.value_of(*a)
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
            self.write(dest, int(self.in_("> ")))
        elif i.op == Opcode.OUTPUT:
            a, *_ = self.get_params(i)
            self.outputting = True
            self.out(self.value_of(*a))
        elif i.op == Opcode.HALT:
            self.done = True
        else:
            raise InvalidInstruction(f"Invalid opcode '{repr(i.op)}'")
        self.ip += i.num_args + 1

    def run_until_output(self):
        while not (self.outputting or self.done):
            self.step()
        self.outputting = False
    def run(self):
        while not self.done:
            self.step()

def read_from_iterable(x, eof=0):
    i = iter(x)
    def read(_):
        try:
            return next(i)
        except StopIteration:
            return eof
    return read

def write_to_list(lst):
    def write(x):
        lst.append(x)
    return write
