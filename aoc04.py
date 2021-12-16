#!/usr/bin/env python3

from functools import reduce
from itertools import chain, zip_longest


with open('aoc04_input.txt') as f:
    a04iter = iter(f.read().splitlines())

numbers = [int(s) for s in next(a04iter).split(',')]
boards = [[list(map(int, l.split())) for l in b[1:]]
    for b in zip_longest(*(a04iter,) * 6)]


def is_win(board, numbers):
    return any(numbers >= set(lines) for lines in chain(board, zip(*board)))

def win_score(board):
    for step in range(1, len(numbers)):
        marked = set(numbers[:step])
        if is_win(board, marked):
            u = sum(set(chain.from_iterable(board)) - marked)
            n = numbers[step-1]
            return step, u * n

scores = list(map(win_score, boards))
_, first_score = min(scores)

print(f'Part 1: {first_score=}')


_, last_score = max(scores)

print(f'Part 2: {last_score=}')
