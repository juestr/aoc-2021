#!/usr/bin/env python3

from collections import Counter
import re

with open('aoc05_input.txt') as f:
    a5 = f.read().splitlines()


pattern = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)')
lines = [[int(x) for x in pattern.fullmatch(l).groups()] for l in a5]
hvlines = [l for l in lines if l[0] == l[2] or l[1] == l[3]]

def line_points(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    d = max(abs(dx), abs(dy))
    return ((x1 + dx//d*i, y1 + dy//d*i) for i in range(d+1))

ctr = Counter(point for line in hvlines for point in line_points(*line))
danger_points = sum(1 for point, count in ctr.items() if count > 1)

print(f'Part 1: {danger_points=}')


ctr2 = Counter(point for line in lines for point in line_points(*line))
danger_points2 = sum(1 for point, count in ctr2.items() if count > 1)

print(f'Part 2: {danger_points2=}')
