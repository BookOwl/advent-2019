import os.path, time
import intcode
from collections import defaultdict
from turtle import *
CLEAR = 1
WALL = 0
TARGET = 2
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

def move_in_dir(x, y, d):
    if d == UP:
        return x, y+1
    elif d == DOWN:
        return x, y-1
    elif d == LEFT:
        return x-1, y
    elif d == RIGHT:
        return x+1, y

def reverse(d):
    return {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}[d]

def render_maze(maze):
    positions = list(sorted(maze.keys()))
    min_x = min(c[0] for c in positions)
    max_x = max(c[0] for c in positions)
    min_y = min(c[1] for c in positions)
    max_y = max(c[1] for c in positions)
    x_range = max_x - min_x
    y_range = max_y - min_y
    render_lst = [["X"]*x_range for _ in range(y_range)]
    for place in positions:
        render_lst[place[1]+abs(min_y)][place[0]+abs(min_x)] = maze[place]
    print("\n".join("".join(row) for row in render_lst))

def neighbors(n, maze):
    for potential in [(n[0], n[1]+1), (n[0], n[1]-1), (n[0]+1, n[1]), (n[0]-1, n[1])]:
        if maze.get(potential, WALL) != WALL:
            yield potential

def a_star(maze, start, goal):
    def reconstruct(came_from, current):
        path = []
        while current in came_from.keys():
            path.append(current)
            current = came_from[current]
        return list(reversed(path))
    def h(node):
        return (node[0]-goal[0])**2 + (node[1]-goal[1])**2
    open_set = {start}
    came_from = {}
    g_score = defaultdict(lambda: float("inf"))
    g_score[start] = 0
    f_score = defaultdict(lambda: float("inf"))
    f_score[start] = h(start)
    while open_set:
        current = min(open_set, key=lambda n: f_score[n])
        if current == goal:
            return reconstruct(came_from, current)
        open_set.remove(current)
        for neighbor in neighbors(current, maze):
            t_gscore = g_score[current] + 1
            if t_gscore < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = t_gscore
                f_score[neighbor] = g_score[neighbor] + h(neighbor)
                open_set.add(neighbor)
    return "ERROR"

def part1():
    pensize(10)
    tracer(8)
    delay(0)
    pc = intcode.Computer()
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day15.txt")) as f:
        prog = f.read().strip()
    pc.load_program(prog)
    maze = {}
    move_stack = [RIGHT]
    dirs = [UP, DOWN, LEFT, RIGHT]
    back = LEFT
    x, y = 0, 0
    delta_x, delta_y = 0, 0
    target_x, target_y = 0, 0
    last_status = CLEAR
    #tried = defaultdict(list)
    def move(_):
        #print(f"STATUS: {['WALL', 'CLEAR', 'TARGET'][last_status]}")
        nonlocal x, y, delta_x, delta_y, maze, move_stack, back, target_x, target_y
        #print(move_stack)
        if last_status == CLEAR or last_status == TARGET:
            x += delta_x
            y += delta_y
            if (x, y) in maze.keys():
                backtrack = True
            else:
                backtrack = False
            maze[x, y] = last_status
            goto(x*10, y*10)
            if last_status == TARGET:
                #dot(15, "blue")
                target_x, target_y = x, y
            options = [d for d in dirs if d != back and d not in maze.keys()]
            if not backtrack:
                move_stack.append(back)
                move_stack += options
        elif last_status == WALL:
            #del move_stack[-1]
            maze[x+delta_x, y+delta_y] = WALL
            penup()
            goto((x+delta_x)*10, (y+delta_y)*10)
            dot(10, "orange")
            goto(x*10, y*10)
            pendown()
        m = move_stack.pop()
        if m == UP:
            delta_x = 0
            delta_y = 1
        elif m == DOWN:
            delta_x = 0
            delta_y = -1
        elif m == LEFT:
            delta_x = -1
            delta_y = 0
        elif m == RIGHT:
            delta_x = 1
            delta_y = 0
        back = reverse(m)
        #print(f"MOVING {['','UP','DOWN','LEFT','RIGHT'][m]} FROM {(x, y)}")
        #print(move_stack)
        #print("---")
        #input()
        #time.sleep(0.01)
        return m
    def read_status(s):
        nonlocal last_status
        last_status = s
    pc.set_io(in_=move, out=read_status)
    while move_stack:
        pc.run_until_output()
    #pc.run_until_output()
    best_path = a_star(maze, (0, 0), (target_x, target_y))
    #print(best_path)
    print(len(best_path))
    penup()
    goto(target_x*10, target_y*10)
    dot(15, "green")
    goto(0, 0)
    color("red")
    pendown()
    for c in best_path:
        goto(c[0]*10, c[1]*10)
    penup()
    goto(target_x * 10, target_y * 10)
    dot(15, "#ADD8FF")
    update()
    print(f"target: {target_x, target_y}")
    return maze, (target_x, target_y)
    #render_maze(maze)

def part2(maze, target):
    Q = []
    dist = {}
    prev = {}
    for v in maze.keys():
        if maze[v] != WALL:
            dist[v] = float("inf")
            prev[v] = None
            Q.append(v)
    dist[target] = 0
    while Q:
        u = min(Q, key=lambda n: dist[n])
        Q.remove(u)
        for v in neighbors(u, maze):
            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
    print("Max O2 time:", max(dist.values()))

if __name__ == '__main__':
    maze, target = part1()
    print("---")
    part2(maze, target)
    done()
