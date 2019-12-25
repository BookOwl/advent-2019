from enum import IntEnum

class Opcode(IntEnum):
    ADD = 1
    MUL = 2
    HALT = 99

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

    def step(self):
        op = self.memory[self.ip]
        if op == Opcode.ADD:
            a, b, dest = self.memory[self.ip+1:self.ip+4]
            self.memory[dest] = self.memory[a] + self.memory[b]
        elif op == Opcode.MUL:
            a, b, dest = self.memory[self.ip + 1:self.ip + 4]
            self.memory[dest] = self.memory[a] * self.memory[b]
        elif op == Opcode.HALT:
            self.done = True
        else:
            raise InvalidInstruction(f"Invalid opcode '{op}'")
        self.ip += 4

    def run(self):
        while not self.done:
            self.step()


