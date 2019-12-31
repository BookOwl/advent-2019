import os.path
import intcode
from turtle import *

def part1():
    pc = intcode.Computer()
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day11.txt")) as f:
        prog = f.read().strip()
    painting = True
    painted = {}
    x, y = 0, 0
    dir = 0
    def camera(_):
        return painted.get((x, y), 0)
    def paint_or_turn(o):
        nonlocal painting, x, y, dir
        assert o == 0 or o == 1
        if painting:
            painted[x, y] = o
        else:
            if o == 0:
                dir = (dir - 1) % 4
            else:
                dir = (dir + 1) % 4
            if dir == 0:
                y += 1
            elif dir == 1:
                x += 1
            elif dir == 2:
                y -= 1
            elif dir == 3:
                x -= 1
        painting = not painting
    pc.set_io(in_=camera, out=paint_or_turn)
    pc.load_program(prog)
    pc.run()
    print(len(painted.keys()))

def part2():
    bgcolor("black")
    pensize(10)
    delay(0)
    speed(0)
    penup()
    seth(90)
    goto(-420, 75)
    dot(10)
    pc = intcode.Computer()
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day11.txt")) as f:
        prog = f.read().strip()
    painting = True
    painted = {(0, 0): 1}
    x, y = 0, 0
    dir = 0
    def camera(_):
        nonlocal painted
        return painted.get((x, y), 0)
    def paint_or_turn(o):
        nonlocal painting, x, y, dir
        if painting:
            painted[x, y] = o
            if o == 0:
                color("black")
            else:
                color("white")
        else:
            if o == 0:
                dir = (dir - 1) % 4
                left(90)
            else:
                dir = (dir + 1) % 4
                right(90)
            if dir == 0:
                y += 1
            elif dir == 1:
                x += 1
            elif dir == 2:
                y -= 1
            elif dir == 3:
                x -= 1
            dot(20)
            forward(20)
        painting = not painting
    pc.set_io(in_=camera, out=paint_or_turn)
    pc.load_program(prog)
    pc.run()
    print(len(painted.keys()))
    done()

if __name__ == '__main__':
    part1()
    print("---")
    part2()

