#!/usr/bin/env python3

from collections import deque

with open('aoc06_input.txt') as f:
    a6 = f.read().split(',')

start = [int(f) for f in a6]
fish = deque(map(start.count, range(9)))

def step_days(n):
    for i in range(n):
        fish.rotate(-1)
        fish[6] += fish[8]

step_days(80)
print(f'Part 1: fish={sum(fish)}')

step_days(256-80)
print(f'Part 2: fish={sum(fish)}')
