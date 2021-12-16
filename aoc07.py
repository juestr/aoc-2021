#!/usr/bin/env python3

with open('aoc07_input.txt') as f:
    a7 = f.read().split(',')


crabs = [int(c) for c in a7]
crabs_range = range(min(crabs), max(crabs)+1)

def fuel(x):
    return sum(abs(x-c) for c in crabs)

x = min(map(fuel, crabs_range))
print(f'Part 1: {x=}')


def fuel2(x):
    return sum((d:=abs(x-c)) * (d+1) // 2 for c in crabs)

x2 = min(map(fuel2, crabs_range))
print(f'Part 2: {x2=}')
