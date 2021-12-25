#!/usr/bin/env python3

import sys

# This was very hard, but I attempted a blackbox general solution without
# analyzing the code by hand first.
# Trying to solve this with sympy hangs while building and simplifying
# expressions far from the required depth, and I didn't want to mess with
# better solvers.
# I had to look at the solutions thread eventually after noticing the
# regular pattern and running out of time.

with open(sys.argv[1] if len(sys.argv) >= 2 else 'aoc24_input.txt') as f:
    input = f.read().splitlines()
code = [tuple(l.split()) for l in input]

params = list(zip(*[[int(l[2]) for l in code[offs::18]] for offs in (4, 5, 15)]))
# print(params)

# The input code repeats this loop 14 times with an input digit each,
# the only difference being the 3 parameters extracted above.
# This is not really needed except for the final asserts.
def monad(inputs):
    z = 0
    for (a, b, c), d in zip(params, inputs):
        inp = int(d)
        z, x = divmod(z, a)         # a is always either 1 (=noop) or 26 (=pop)
        if x != inp - b:            # for every a==26 this must be avoided
            z = 26 * z + (inp + c)  # push inp + c
    return z

def find(part):
    inputs = []
    z = 0
    pushes = []
    for i in range(14):
        a, b, c = params[i]
        if a == 1:
            z = z * 26 + c
            inputs.append(9 if part == 1 else 1)    # assume best case
            pushes.append(i)
        else:
            assert a == 26
            ptr = pushes.pop()
            z, x = divmod(z, 26)
            inputs.append(inputs[ptr] + x + b)
            if inputs[i] > 9:                       # adjust down
                assert part == 1
                inputs[ptr] += 9 - inputs[i]
                inputs[i] = 9
            elif inputs[i] < 1:                     # adjust up
                assert part == 2
                inputs[ptr] += 1 - inputs[i]
                inputs[i] = 1
    return ''.join(str(d) for d in inputs)

p1 = find(part=1)
assert monad(p1) == 0
print(f'Part 1: {p1=}')

p2 = find(part=2)
assert monad(p2) == 0
print(f'Part 2: {p2=}')
