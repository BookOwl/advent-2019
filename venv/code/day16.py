import itertools
def part1():
    with open("../inputs/day16.txt") as f:
        signal = list(map(int, f.read().strip()))
    #signal = list(map(int, "80871224585914546619083218645595"))
    def pattern(n):
        n += 1
        p = itertools.cycle([0]*n + [1]*n + [0]*n + [-1]*n)
        next(p)
        return p
    def phase(signal):
        out = []
        for j in range(len(signal)):
            out.append(abs(sum([i*p for (i, p) in zip(signal, pattern(j))]))%10)
        return out
    print("Input signal:", "".join(map(str, signal)))
    for n in range(100):
        signal = phase(signal)
        #print(f"After phase {n+1}:", "".join(map(str, signal)))
    print(''.join(map(str, signal[:8])))

def part2():
    with open("../inputs/day16.txt") as f:
        signal = list(map(int, f.read().strip()))*10_000
        offset = int(''.join(map(str, signal[:7])))
    #signal = list(map(int, "03036732577212944063491565474664"))*10_000
    #offset = int(''.join(map(str, signal[:7])))
    signal = list(reversed(signal[offset:]))
    def phase(signal):
        #[sum(signal[j:]) % 10 for j in range(len(signal))]
        out = []
        a = 0
        for i in signal:
            a += i
            out.append(a%10)
        return out
    print(f"Offset: {offset}")
    for n in range(100):
        print(f"Phase {n+1}")
        signal = phase(signal)
    print(''.join(map(str, reversed(signal[-8:]))))

if __name__ == '__main__':
    part1()
    print("---")
    part2()