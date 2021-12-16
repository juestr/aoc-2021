#!/usr/bin/env python3

from functools import reduce
from statistics import median


with open('aoc10_input.txt') as f:
    a10 = f.read().splitlines()
#print(a10)


brackets = dict(zip('([{<', ')]}>'))
scores_unexpected = dict(zip(')]}>', (3, 57, 1197, 25137)))

def validate(s):
    stack = []
    for b in s:
        if b in brackets:
            stack.append(b)
        elif stack and b == brackets[stack[-1]]:
            stack.pop()
        else:
            return 'unexpected', b
    return ('incomplete', stack) if stack else 'correct'

def score_unexpected(s):
    match validate(s):
        case 'unexpected', b:   return scores_unexpected[b]
        case _:                 return 0

score = sum(map(score_unexpected, a10))
print(f'Part1: {score=}')


scores_missing = dict(zip(')]}>', (1, 2, 3, 4)))

def score_missing(s):
    match validate(s):
        case 'incomplete', stack:
            missing = [scores_missing[brackets[b]] for b in reversed(stack)]
            return reduce(lambda acc, x: acc*5 + x, missing, 0)
        case _:
            return 0

score = median(filter(None, map(score_missing, a10)))
print(f'Part2: {score=}')
