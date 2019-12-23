import os.path

def part1():
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day1.txt")) as f:
        modules = map(int, f.read().split("\n"))
        fuel = sum(mass//3 - 2 for mass in modules)
        return fuel

def part2():
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day1.txt")) as f:
        fuel = 0
        for mass in map(int, f.read().split("\n")):
            while mass//3-2 > 0:
                mass = mass//3 - 2
                fuel += mass
        return fuel


if __name__ == '__main__':
    fuel = part1()
    print(fuel)
    print("---")
    fuel = part2()
    print(fuel)
