import os.path
import re
from math import gcd

def lcm(a, b):
    return int(abs(a*b)/gcd(a, b))
class Moon:
    def __init__(self, pos):
        self.pos = list(map(int, pos))
        self.vel = [0, 0, 0]
    def apply_gravity(self, moons):
        for moon in moons:
            for i in range(3):
                if moon.pos[i] > self.pos[i]:
                    self.vel[i] += 1
                elif self.pos[i] > moon.pos[i]:
                    self.vel[i] -= 1
    def apply_velocity(self):
        for i in range(3):
            self.pos[i] += self.vel[i]
    def energy(self):
        return sum(map(abs, self.pos)) * sum(map(abs, self.vel))
    def __repr__(self):
        return f"<pos={self.pos}, vel={self.vel}>"

def part1():
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day12.txt")) as f:
        scan = f.read()
    moons = [Moon(pos) for pos in re.findall(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", scan)]
    for i in range(1000):
        for moon in moons:
            moon.apply_gravity(moons)
        for moon in moons:
            moon.apply_velocity()
    print(sum(moon.energy() for moon in moons))

def part2():
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day12.txt")) as f:
        scan = f.read()
    moons = [Moon(pos) for pos in re.findall(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", scan)]
    x_start = [(moon.pos[0], moon.vel[0]) for moon in moons]
    y_start = [(moon.pos[1], moon.vel[1]) for moon in moons]
    z_start = [(moon.pos[2], moon.vel[2]) for moon in moons]
    x_count = 0
    y_count = 0
    z_count = 0
    loops = 0
    i = 0
    while loops < 3:
        i += 1
        for moon in moons:
            moon.apply_gravity(moons)
        for moon in moons:
            moon.apply_velocity()
        if [(moon.pos[0], moon.vel[0]) for moon in moons] == x_start and not x_count:
            x_count = i
            loops += 1
        if [(moon.pos[1], moon.vel[1]) for moon in moons] == y_start and not y_count:
            y_count = i
            loops += 1
        if [(moon.pos[2], moon.vel[2]) for moon in moons] == z_start and not z_count:
            z_count = i
            loops += 1
    print(lcm(x_count, lcm(y_count, z_count)))

if __name__ == '__main__':
    part1()
    print("---")
    part2()