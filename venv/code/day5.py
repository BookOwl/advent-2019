import os.path
import intcode

def part1():
    pc = intcode.Computer()
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day5.txt")) as f:
        print("Provide '1' as input")
        pc.load_program(f.read().strip())
        pc.run()

def part2():
    pc = intcode.Computer()
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day5.txt")) as f:
        print("Provide '5' as input")
        pc.load_program(f.read().strip())
        pc.run()


if __name__ == '__main__':
    part1()
    print("---")
    part2()