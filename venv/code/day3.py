import os.path

def part1():
    #with open(os.path.join(os.path.dirname(__file__), "../inputs/day3.txt")) as f:
    #    w1, w2 = f.read().split("\n")
    w1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
    w2 = "U62,R66,U55,R34,D71,R55,D58,R83"
    def wire_cords(wire):
        w = wire.split(",")
        p = []
        x, y = 0, 0
        for q in w:
            direction, dist = q[0], int(q[1:])
            if direction == "U":
                p += [(x, y_) for y_ in range(y, y+dist+1)]
                y += dist
            elif direction == "D":
                p += [(x, y_) for y_ in range(y, y - (dist+1), -1)]
                y -= dist
            elif direction == "L":
                p += [(x_, y) for x_ in range(x, x - (dist+1), -1)]
                x -= dist
            elif direction == "R":
                p += [(x_, y) for x_ in range(x, x+dist+1)]
                x += dist
        return set(p)
    p1 = wire_cords(w1)
    p2 = wire_cords(w2)
    intersections = p1 & p2
    return list(sorted(abs(x) + abs(y) for (x, y) in intersections))[1]

def part2():
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day3.txt")) as f:
        w1, w2 = f.read().split("\n")
    #w1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
    #w2 = "U62,R66,U55,R34,D71,R55,D58,R83"
    def wire_cords(wire):
        w = wire.split(",")
        p = []
        x, y = 0, 0
        steps = 0
        for q in w:
            direction, dist = q[0], int(q[1:])
            if direction == "U":
                p += [(x, y_, steps+i) for (y_, i) in zip(range(y, y+dist+1), range(0, dist+1))]
                y += dist
                steps += dist
            elif direction == "D":
                p += [(x, y_, steps+i) for (y_, i) in zip(range(y, y - (dist+1), -1), range(0, dist+1))]
                y -= dist
                steps += dist
            elif direction == "L":
                p += [(x_, y, steps+i) for (x_, i) in zip(range(x, x - (dist+1), -1), range(0, dist+1))]
                x -= dist
                steps += dist
            elif direction == "R":
                p += [(x_, y, steps+i) for (x_, i) in zip(range(x, x+dist+1), range(0, dist+1))]
                x += dist
                steps += dist
        return p
    p1 = wire_cords(w1)
    p2 = wire_cords(w2)
    intersections = {(x, y) for (x, y, _) in p1} & {(x, y) for (x, y, _) in p2}
    steps = []
    for c in intersections:
        s = 0
        for (x, y, step) in p1:
            if (x, y) == c:
                s += step
                break
        for (x, y, step) in p2:
            if (x, y) == c:
                s += step
                break
        steps.append(s)
    steps.sort()
    return steps[1]


if __name__ == '__main__':
    print(part1())
    print("---")
    print(part2())