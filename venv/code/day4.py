import re
def part1():
    low = 231832
    high = 767346
    double_digits = re.compile(r"(\d)\1")
    valid = 0
    for password in range(low, high+1):
        p = str(password)
        if ''.join(sorted(p)) == p and double_digits.search(p):
            valid += 1
    return valid

def part2():
    low = 231832
    high = 767346
    repeated_digits = re.compile(r"1+|2+|3+|4+|5+|6+|7+|8+|9+|0+")
    valid = 0
    for password in range(low, high+1):
        p = str(password)
        if ''.join(sorted(p)) == p and 2 in map(len, repeated_digits.findall(p)):
            valid += 1
    return valid

if __name__ == '__main__':
    print(part1())
    print("---")
    print(part2())