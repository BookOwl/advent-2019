import os.path
import math
from collections import namedtuple, defaultdict

def part1():
    reactions = {}
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day14.txt")) as f:
        for reaction in f:
            in_, out = reaction.split(" => ")
            out = out.strip()
            in_ = [(int(n), x) for (n, x) in [x.split(" ") for x in in_.split(", ")]]
            out_amount, out_name = out.split(" ")
            reactions[out_name] = {"produced": int(out_amount), "inputs": in_}
    #print(reactions)
    needed = defaultdict(int)
    needed["FUEL"] = 1
    ore_reactions = defaultdict(int)
    ore_needed = 0
    extra = defaultdict(int)
    while needed:
        out, _amount = needed.popitem()
        amount = _amount - extra[out]
        reaction = reactions[out]
        produced = reaction["produced"]
        inputs = reaction["inputs"]
        multiplier = math.ceil(amount/produced)
        #print(f"PRODUCING {produced*multiplier} ({_amount} NEEDED MINUS {extra[out]} ALREADY MADE) UNITS OF {out} USING REACTION {inputs} => {produced} {out}")
        extra[out] = produced*multiplier - amount
        for in_ in inputs:
            in_amount, in_name = in_
            if in_name == "ORE":
                ore_reactions[out] += _amount
                #print(f"ADDING {amount} {out} TO ORE REACTIONS")
            else:
                needed[in_name] += in_amount * multiplier
                #print(f"NEED {in_amount * multiplier} MORE {in_name}")
    while ore_reactions:
        needed, amount = ore_reactions.popitem()
        amount = math.ceil(amount)
        reaction = reactions[needed]
        produced = reaction["produced"]
        ore_in = reaction["inputs"][0][0]
        ore_needed += math.ceil(amount/produced) * ore_in
        #print(f"USING {math.ceil(amount/produced) * ore_in} ORE TO PRODUCE {math.ceil(amount/produced)*produced} {needed}")
    print(f"ORE NEEDED: {ore_needed}")

def part2():
    reactions = {}
    with open(os.path.join(os.path.dirname(__file__), "../inputs/day14.txt")) as f:
        for reaction in f:
            in_, out = reaction.split(" => ")
            out = out.strip()
            in_ = [(int(n), x) for (n, x) in [x.split(" ") for x in in_.split(", ")]]
            out_amount, out_name = out.split(" ")
            reactions[out_name] = {"produced": int(out_amount), "inputs": in_}
    #print(reactions)
    def ore_for_fuel(n):
        extra = defaultdict(int)
        needed = defaultdict(int)
        needed["FUEL"] = n
        ore_reactions = defaultdict(int)
        ore_needed = 0
        while needed:
            out, _amount = needed.popitem()
            amount = _amount - extra[out]
            reaction = reactions[out]
            produced = reaction["produced"]
            inputs = reaction["inputs"]
            multiplier = math.ceil(amount/produced)
            #print(f"PRODUCING {produced*multiplier} ({_amount} NEEDED MINUS {extra[out]} ALREADY MADE) UNITS OF {out} USING REACTION {inputs} => {produced} {out}")
            extra[out] = produced*multiplier - amount
            for in_ in inputs:
                in_amount, in_name = in_
                if in_name == "ORE":
                    ore_reactions[out] += _amount
                    #print(f"ADDING {amount} {out} TO ORE REACTIONS")
                else:
                    needed[in_name] += in_amount * multiplier
                    #print(f"NEED {in_amount * multiplier} MORE {in_name}")
        while ore_reactions:
            needed, amount = ore_reactions.popitem()
            amount = math.ceil(amount)
            reaction = reactions[needed]
            produced = reaction["produced"]
            ore_in = reaction["inputs"][0][0]
            ore_needed += math.ceil(amount/produced) * ore_in
            #print(f"USING {math.ceil(amount/produced) * ore_in} ORE TO PRODUCE {math.ceil(amount/produced)*produced} {needed}")
        return ore_needed
    TRILLION = 1000000000000
    old_max_fuel = 0
    max_fuel = 2
    ore_needed = ore_for_fuel(max_fuel)
    # Find lower and upper bounds
    while ore_needed < TRILLION:
        old_max_fuel = max_fuel
        max_fuel *= 2
        ore_needed = ore_for_fuel(max_fuel)
    print("Bounds:", old_max_fuel, max_fuel)
    # Binary search
    old_guess = 0
    guess = (max_fuel+old_max_fuel)//2
    ore_needed = ore_for_fuel(guess)
    while old_guess != guess:
        if ore_needed < TRILLION:
            old_max_fuel = guess
        else:
            max_fuel = guess
        old_guess = guess
        guess = (max_fuel + old_max_fuel) // 2
        ore_needed = ore_for_fuel(guess)
        print("GUESS:", guess, "ORE NEEDED:", ore_needed)

if __name__ == '__main__':
    part1()
    print("---")
    part2()
        

