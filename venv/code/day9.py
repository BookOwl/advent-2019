import os.path
import intcode

def part1():
    pc = intcode.Computer()
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day9.txt")) as f:
        prog = f.read().strip()
    pc.load_program(prog)
    pc.set_io(in_ = lambda _: 1)
    pc.run()

def part2():
    pc = intcode.Computer()
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day9.txt")) as f:
        prog = f.read().strip()
    pc.load_program(prog)
    pc.set_io(in_ = lambda _: 2)
    pc.run()

if __name__ == '__main__':
    part1()
    print("---")
    part2()