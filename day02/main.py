import fileinput
import re
from math import prod


def parse_line(l):
    g, sets = l.strip().split(": ")
    return int(g.split(" ")[-1]), tuple(
        dict(reversed(cube.split(" ")) for cube in s.split(", "))
        for s in sets.split("; ")
    )


games = list(map(parse_line, fileinput.input()))

# Pt 1.
avail = {"red": 12, "green": 13, "blue": 14}
print(
    sum(
        g
        for g, sets in games
        if all(all(int(n) <= avail[color] for color, n in s.items()) for s in sets)
    )
)


def min_color(sets):
    min_cubes = {"red": 0, "blue": 0, "green": 0}
    for s in sets:
        for color, n in s.items():
            min_cubes[color] = max(min_cubes[color], int(n))
    return min_cubes


# Pt 2.
print(sum(prod(n for n in min_color(sets).values()) for _, sets in games))
