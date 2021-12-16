#!/usr/bin/env python3

from collections import Counter
from itertools import permutations
import operator

with open('aoc08_input.txt') as f:
    a8 = f.read().splitlines()


displays = [[side.split() for side in l.split(' | ')] for l in a8]
ctr = Counter([len(o) for _, outp in displays for o in outp])
digits1478 = ctr[2] + ctr[3] + ctr[4] + ctr[7]

print(f'Part 1: {digits1478=}')


signals = 'abcdefg'
digits = 'abcefg cf acdeg acdfg bcdf abdfg abdefg acf abcdefg abcdfg'.split()
digits_set = set(digits)
decoders = [lambda s, t=t: ''.join(sorted(s.translate(t))) for t in
    [str.maketrans(''.join(p), signals) for p in permutations(signals)]]

def decode_display(disp):
    inout = sum(disp, [])
    for d in decoders:
        if set(ds:=[d(s) for s in inout]) <= digits_set:
            return sum(map(operator.mul,
                (1000, 100, 10, 1), map(digits.index, ds[-4:])))

outputs_sum = sum(map(decode_display, displays))

print(f'Part 2: {outputs_sum=}')
