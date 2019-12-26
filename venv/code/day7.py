import os.path
import itertools
from intcode import *

def part1():
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day7.txt")) as f:
        amp_software = f.read().strip()
    amp1 = Computer()
    amp2 = Computer()
    amp3 = Computer()
    amp4 = Computer()
    amp5 = Computer()
    best = 0
    for (a, b, c, d, e) in itertools.permutations(range(5)):
        amp1.load_program(amp_software)
        amp2.load_program(amp_software)
        amp3.load_program(amp_software)
        amp4.load_program(amp_software)
        amp5.load_program(amp_software)
        in_, out = [a, 0], []
        amp1.set_io(read_from_iterable(in_), write_to_list(out))
        amp1.run()
        in_, out = [b, out[0]], []
        amp2.set_io(read_from_iterable(in_), write_to_list(out))
        amp2.run()
        in_, out = [c, out[0]], []
        amp3.set_io(read_from_iterable(in_), write_to_list(out))
        amp3.run()
        in_, out = [d, out[0]], []
        amp4.set_io(read_from_iterable(in_), write_to_list(out))
        amp4.run()
        in_, out = [e, out[0]], []
        amp5.set_io(read_from_iterable(in_), write_to_list(out))
        amp5.run()
        if out[0] > best:
            #print(f"Best is {out[0]} with settings {[a, b, c, d, e]}")
            best = out[0]
    print("Part 1:", best)

def part2():
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day7.txt")) as f:
        amp_software = f.read().strip()
    amp1 = Computer()
    amp2 = Computer()
    amp3 = Computer()
    amp4 = Computer()
    amp5 = Computer()
    best = 0
    def read_from_list(l):
        def read(_):
            x = l[0]
            del l[0]
            return x
        return read
    for (a, b, c, d, e) in itertools.permutations(range(5, 10)):
        amp1.load_program(amp_software)
        amp2.load_program(amp_software)
        amp3.load_program(amp_software)
        amp4.load_program(amp_software)
        amp5.load_program(amp_software)
        amps = [amp1, amp2, amp3, amp4, amp5]
        e_to_a = [a, 0]
        a_to_b = [b]
        b_to_c = [c]
        c_to_d = [d]
        d_to_e = [e]
        amp1.set_io(read_from_list(e_to_a), write_to_list(a_to_b))
        amp2.set_io(read_from_list(a_to_b), write_to_list(b_to_c))
        amp3.set_io(read_from_list(b_to_c), write_to_list(c_to_d))
        amp4.set_io(read_from_list(c_to_d), write_to_list(d_to_e))
        amp5.set_io(read_from_list(d_to_e), write_to_list(e_to_a))
        while amps:
            amp = amps[0]
            del amps[0]
            amp.run_until_output()
            if not amp.done:
                amps.append(amp)
        out = e_to_a[0]
        if out > best:
            best = out
    print("Part 2:", best)

if __name__ == '__main__':
    part1()
    print("---")
    part2()