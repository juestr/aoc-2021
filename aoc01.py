#!/usr/bin/env python3

from itertools import pairwise

with open('aoc01_input.txt') as f:
    a1 = f.read().splitlines()

xs = list(map(int, a1))
n1 = sum(a < b for a, b in pairwise(xs))

print(f'Part 1: {n1=}')

triples = ((a, b, c) for (a, b), (_, c) in pairwise(pairwise(xs)))
n2 = sum(sum(a) < sum(b) for a, b in pairwise(triples))

print(f'Part 2: {n2=}')
