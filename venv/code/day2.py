import os.path
import intcode

def part1():
    pc = intcode.Computer()
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day2.txt")) as f:
        pc.load_program(f.read().strip())
        pc.memory[1] = 12
        pc.memory[2] = 2
        print(pc.memory)
        pc.run()
        return pc.memory[0]

def part2():
    pc = intcode.Computer()
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day2.txt")) as f:
        program = f.read().strip()
    for i in range(0, 100):
        for j in range(0, 100):
            pc.load_program(program)
            pc.memory[1] = i
            pc.memory[2] = j
            pc.run()
            if pc.memory[0] == 19690720:
                return 100 * i + j
    return "Error!"


if __name__ == '__main__':
    print(part1())
    print("---")
    print(part2())

"""
<Instruction <Opcode.ADD: 1> Mode [<ParamMode.Positon: 0>, <ParamMode.Positon: 0>, <ParamMode.Positon: 0>]>
[135, 6, 0] [4138656, 2, 1]
"""