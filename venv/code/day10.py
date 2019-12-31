import os.path
from collections import defaultdict
import math

def part1():
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day10.txt")) as f:
        map = list(f)
    roids = []
    for y, line in enumerate(map):
        for x, spot in enumerate(line):
            if spot == "#":
                roids.append((x, y))
    spots = {}
    for roid in roids:
        x, y = roid
        angles_seen = []
        spots_detected = []
        count = 0
        for other in sorted(roids, key = lambda c: (c[0]-x)**2+(c[1]-y)**2):
            x_, y_ = other
            angle = math.atan2(y_ - y, x_ - x)
            if (x_, y_) == (x, y): continue
            if angle not in angles_seen:
                angles_seen.append(angle)
                spots_detected.append((x_, y_))
                count += 1
        spots[(x, y)] = count
        """
        print(f"({x}, {y}) => {count}")
        for y_, line in enumerate(map):
            for x_, spot in enumerate(line):
                if (x, y) == (x_, y_):
                    a = "#"
                elif (x_, y_) in spots_detected:
                    a = "*"
                elif spot == ".":
                    a = "."
                else:
                    a = "_"
                print(a, end="")
            print()
            """
        #print()
    best = max(spots.items(), key = lambda a: a[1])
    print(best[0], "=>", best[1])
    return best[0]

def part2(x, y):
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day10.txt")) as f:
        map = list(f)
    roids = []
    for y_, line in enumerate(map):
        for x_, spot in enumerate(line):
            if spot == "#":
                roids.append((x_, y_))
    killed = 0
    roids.remove((x, y))
    roids_by_angles = defaultdict(list)
    for roid in roids:
        x_, y_ = roid
        angle = math.atan2(-(y_ - y), x_ - x)
        if math.pi/2 >= angle >= 0:
            angle = abs(angle-math.pi/2)
        elif angle < 0:
            angle = abs(angle) + math.pi/2
        else:
            angle =(5*math.pi)/2 - angle
        roids_by_angles[angle].append((x_, y_))
    for v in roids_by_angles.values(): v.sort(key = lambda c: (c[0]-x)**2+(c[1]-y)**2)
    while roids:
        for angle in sorted(roids_by_angles.keys()):
            if not roids_by_angles[angle]:
                continue
            x_, y_ = roids_by_angles[angle].pop(0)
            if (x_, y_) == (x, y): continue
            killed += 1
            roids.remove((x_, y_))
            #print(f"Asteroid #{killed} is at ({x_}, {y_})")
            if killed == 200:
                print(f"({x_}, {y_}) => {x_*100+y_}")
                return



if __name__ == '__main__':
    x, y = part1()
    print("---")
    part2(x, y)
