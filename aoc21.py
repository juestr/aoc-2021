#!/usr/bin/env python3

from collections import Counter
from itertools import cycle, product
import sys

Day21 = (1, 6)
start1, start2 = Day21 if len(sys.argv) == 1 else map(int, sys.argv[1:3])


def turn(pos, score, rolls, die):
    newpos = (pos + next(die) + next(die) + next(die)) % 10
    return newpos, score + newpos + 1, rolls + 3

pos1, pos2 = start1 - 1, start2 - 1
score1 = score2 = rolls = 0
die100 = cycle(range(1, 101))

while True:
    pos1, score1, rolls = turn(pos1, score1, rolls, die100)
    if score1 >= 1000: break
    pos2, score2, rolls = turn(pos2, score2, rolls, die100)
    if score2 >= 1000: break

result = min(score1, score2) * rolls

print(f'Part 1: {result=}')


def splitgame(pos1, score1, pos2, score2, player1,
        throws=Counter(sum(throws) for throws in product(range(1, 4), repeat=3))):
    for steps, count in throws.items():
        if player1:
            newpos1 = (pos1 + steps) % 10
            yield (newpos1, score1 + newpos1 + 1, pos2, score2), count
        else:
            newpos2 = (pos2 + steps) % 10
            yield (pos1, score1, newpos2, score2 + newpos2 + 1), count

wins1 = wins2 = 0
games = Counter([(start1 - 1, 0, start2 - 1, 0)])
player1 = True

while games:
    newgames = Counter()
    for game, count1 in games.items():
        for (pos1, score1, pos2, score2), count2 in splitgame(*game, player1):
            count = count1 * count2
            match score1 >= 21, score2 >= 21:
                case True, _:   wins1 += count
                case _, True:   wins2 += count
                case _:         newgames[(pos1, score1, pos2, score2)] += count
    games = newgames
    player1 = not player1

result = max(wins1, wins2)

print(f'Part 2: {result=}')
