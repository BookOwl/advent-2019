import intcode
import pprint

def ascii_out():
    output = [[]]
    def write(c):
        c = chr(c)
        if c == "\n":
            output.append([])
        else:
            output[-1].append(c)
    return output, write

UP, LEFT, DOWN, RIGHT = range(4)

def create_path(out):
    start_x, start_y = 0, 0
    for y, row in enumerate(out):
        for x, o in enumerate(row):
            if o == "^":
                start_x = x
                start_y = y
                break
        else:
            continue
        break
    x = start_x
    y = start_y
    if x > 1 and out[start_y][start_x-1] == "#":
        dir = LEFT
        path = ["L"]
    elif x < len(out[start_y]) - 1:
        dir = RIGHT
        path = ["R"]
    while True:
        segment_len = 1
        if dir == UP:
            while y-segment_len-1 >= 0 and out[y-segment_len-1][x] == "#":
                segment_len += 1
            y -= segment_len
            path.append(str(segment_len))
            if x > 1 and out[y][x-1] == "#":
                dir = LEFT
                path.append("L")
            elif x < len(out[y]) - 1 and out[y][x+1] == "#":
                path.append("R")
                dir = RIGHT
            else:
                break
        elif dir == DOWN:
            while y+segment_len+1 < len(out) and out[y+segment_len+1][x] == "#":
                segment_len += 1
            y += segment_len
            path.append(str(segment_len))
            if x > 1 and out[y][x-1] == "#":
                path.append("R")
                dir = LEFT
            elif x < len(out[y]) - 1 and out[y][x+1] == "#":
                path.append("L")
                dir = RIGHT
            else:
                break
        elif dir == LEFT:
            while x-segment_len-1 >= 0 and out[y][x-segment_len-1] == "#":
                segment_len += 1
            x -= segment_len
            path.append(str(segment_len))
            if y > 1 and out[y-1][x] == "#":
                path.append("R")
                dir = UP
            elif y < len(out) - 1 and out[y+1][x] == "#":
                path.append("L")
                dir = DOWN
            else:
                break
        elif dir == RIGHT:
            while x+segment_len+1 < len(out[y]) and out[y][x+segment_len+1] == "#":
                segment_len += 1
            x += segment_len
            path.append(str(segment_len))
            if y > 1 and out[y-1][x] == "#":
                path.append("L")
                dir = UP
            elif y < len(out) - 1 and out[y+1][x] == "#":
                path.append("R")
                dir = DOWN
            else:
                break
    return path

def chunk_in(chunk, lst):
    loc = []
    i = 0
    chunk_len = len(chunk)
    top = len(lst)-chunk_len+1
    while i < top:
        if chunk == lst[i:i+chunk_len]:
            loc.append(i)
        i += 1
    return loc

def compress_path(path):
    return compress_path_rec(path, "ABC", {})[1]

def compress_path_rec(path, names, routines):
    if len(names) == 0:
        routines["main"] = path
        return all(c in "ABC" for c in path), routines
    #path = path[:] # make copy so mutations aren't passed to the caller
    i = 0
    while path[i] in "ABC":
        i += 1
    chunk_len = 0
    locs = None
    while chunk_len < 10 and not any(x in path[i:i+chunk_len+2] for x in "ABC") and len(potental_locs := chunk_in(path[i:i+chunk_len+2], path)) > 1:
        chunk_len += 2
        locs = potental_locs
        p = path[:]
        r = {**routines}
        chunk_name = names[0]
        chunk = p[i:i+chunk_len]
        r[chunk_name] = chunk
        for loc in reversed(locs):
            p[loc:loc + chunk_len] = [chunk_name]
        solved, nr = compress_path_rec(p, names[1:], r)
        if solved:
            return solved, nr
    return False, routines

def compile_routines(routines):
    compiled = []
    for k in ["main", "A", "B", "C"]:
        for c in ",".join(routines[k]):
            compiled.append(ord(c))
        compiled.append(ord("\n"))
    compiled.append(ord("n"))
    compiled.append(ord("\n"))
    return compiled

def part1():
    with open("../inputs/day17.txt") as f:
        pc = intcode.Computer()
        code = f.read().strip()
        pc.load_program(code)
    out, ascii = ascii_out()
    pc.set_io(out=ascii)
    pc.run()
    out = [row for row in out if len(row) != 0]
    #print('\n'.join(''.join(row) for row in out))
    alignment = 0
    for y, row in enumerate(out):
        for x, obj in enumerate(row):
            if obj == "#":
                i = 0
                if x > 0:
                    i += out[y][x-1] == "#"
                if x < len(row)-1:
                    i += out[y][x+1] == "#"
                if y > 0:
                    i += out[y-1][x] == "#"
                if y < len(out)-1:
                    i += out[y+1][x] == "#"
                if i == 4:
                    alignment += x * y
    print(f"Alignment: {alignment}")
    return out

def part2(out):
    with open("../inputs/day17.txt") as f:
        pc = intcode.Computer()
        code = f.read().strip()
        pc.load_program(code)
    path = create_path(out)
    routines = compress_path(path)
    compiled = compile_routines(routines)
    dust = 0
    def in_(_):
        x = compiled.pop(0)
        print(chr(x), end="")
        return x
    def out(o):
        nonlocal dust
        if o > 256:
            dust = o
        else:
            print(chr(o), end="")
    pc.memory[0] = 2
    pc.set_io(in_=in_, out=out)
    pc.run()
    print("Dust collected:", dust)

if __name__ == '__main__':
    out = part1()
    print("---")
    part2(out)