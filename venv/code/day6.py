import os.path

def part1():
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day6.txt")) as f:
        orbit_data = f.read()
    orbit_map = {}
    for orbit in orbit_data.split("\n"):
        a, b = orbit.strip().split(")")
        orbit_map.setdefault(a, []).append(b)
    orbit_counts = {"COM": 0}
    queue = ["COM"]
    while queue:
        a = queue.pop()
        for b in orbit_map.get(a, []):
            orbit_counts[b] = orbit_counts[a] + 1
        queue.extend(orbit_map.get(a, []))
    print(sum(orbit_counts.values()))

def part2():
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day6.txt")) as f:
        orbit_data = f.read()
    parents = {}
    for orbit in orbit_data.split("\n"):
        a, b = orbit.strip().split(")")
        parents[b] = a
    you_chain = []
    you = "YOU"
    while you != "COM":
        you_chain.append(parents[you])
        you = parents[you]
    san = "SAN"
    san_chain = []
    while san not in you_chain:
        san_chain.append(parents[san])
        san = parents[san]
    #print("You:", you_chain)
    #print("San:", san_chain)
    print(len(san_chain) + you_chain.index(san_chain[-1]) - 1)


if __name__ == '__main__':
    part1()
    print("---")
    part2()