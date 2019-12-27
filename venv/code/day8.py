import os.path

WIDTH = 25
HEIGHT = 6

def part1():
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day8.txt")) as f:
        img = f.read()
    layer_size = WIDTH * HEIGHT
    best_layer = ""
    x = 999
    for i in range(0, len(img), layer_size):
        layer = img[i:i+layer_size]
        if layer.count("0") < x:
            best_layer = layer
            x = layer.count("0")
    print(best_layer.count("1") * best_layer.count("2"))

def part2():
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day8.txt")) as f:
        img_data = f.read()
    layer_size = WIDTH * HEIGHT
    layers = []
    for i in range(0, len(img_data), layer_size):
        layers.append(img_data[i:i+layer_size])
    img = []
    for i, pixel in enumerate(zip(*layers)):
        if i % WIDTH == 0:
            img.append("\n")
        for p in pixel:
            if p != "2":
                img.append("████" if p == "1" else "    ")
                break
    print("".join(img))



if __name__ == '__main__':
    part1()
    print("---")
    part2()