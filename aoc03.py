#!/usr/bin/env python3

import operator

with open('aoc03_input.txt') as f:
    a3 = f.read().splitlines()

mco = [x.count('1') > x.count('0') for x in zip(*a3)]
gamma = sum(x * (1<<i) for i, x in enumerate(reversed(mco)))
epsilon = sum((1-x) * (1<<i) for i, x in enumerate(reversed(mco)))
power = gamma * epsilon

print(f'Part 1: {power=}')


def filter_down(op):
    xs = a3
    for i in range(len(a3[0])):
        bit = '1' if op(sum(1 for x in xs if x[i] == '1'), len(xs)/2) else '0'
        xs = [x for x in xs if x[i] == bit]
        if len(xs) == 1:
            return int(xs[0], 2)

oxy = filter_down(operator.ge)
co2 = filter_down(operator.lt)
lifesupport = oxy * co2

print(f'Part 2: {lifesupport=}')
