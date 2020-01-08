import os.path
import intcode
EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4
def part1():
    pc = intcode.Computer()
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day13.txt")) as f:
        prog = f.read().strip()
    pc.load_program(prog)
    screen = {}
    def draw_tile(x, y, id):
        screen[int(x), int(y)] = id
    pc.set_io(out=intcode.out_every(3, draw_tile))
    pc.run()
    print(sum(1 for x in screen.values() if x == BLOCK))

def part2():
    pc = intcode.Computer()
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day13.txt")) as f:
        prog = f.read().strip()
    pc.load_program(prog)
    ball_pos = 0
    paddle_pos = 0
    score = -1
    screen = {}
    def joystick(_):
        if ball_pos < paddle_pos:
            return -1
        elif ball_pos > paddle_pos:
            return 1
        else:
            return 0
    def draw_tile(x, y, id):
        nonlocal score, paddle_pos, ball_pos
        x, y, id = map(int, (x, y, id))
        if x == -1 and y == 0:
            score = int(id)
        if id == PADDLE:
            paddle_pos = int(x)
        elif id == BALL:
            ball_pos = int(x)
        screen[int(x), int(y)] = id
    pc.set_io(in_=joystick, out=intcode.out_every(3, draw_tile))
    pc.memory[0] = 2
    pc.run()
    print(score)

if __name__ == '__main__':
    part1()
    print("---")
    part2()