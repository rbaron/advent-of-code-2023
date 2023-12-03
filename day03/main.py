import fileinput
import itertools
from math import prod


def read_line(line):
    x = 0
    x_start = 0
    state = "out"
    while x < len(line):
        c = line[x]
        if c == ".":
            if state == "in":
                yield from ((i, x_start, line[x_start:x]) for i in range(x_start, x))
                state = "out"
        elif c.isnumeric():
            if state == "out":
                x_start = x
                state = "in"
        else:
            if state == "in":
                yield from ((i, x_start, line[x_start:x]) for i in range(x_start, x))
                state = "out"
            yield (x, x, c)
        x += 1
    if state == "in":
        yield from ((i, x_start, line[x_start:x]) for i in range(x_start, x))


grid = {
    # position: (identifier, value)
    (y, x): ((y, i), c)
    for y, line in enumerate(fileinput.input())
    for x, i, c in read_line(line.strip())
}


def neighbors(y, x):
    yield from (
        (y + dy, x + dx)
        for dy, dx in itertools.product((-1, 0, 1), repeat=2)
        if not (dx == dy == 0)
    )


# Pt 1.
uniques = set(
    (i, int(c))
    for (y, x), ((j, i), c) in grid.items()
    for n in neighbors(y, x)
    if not grid.get(n, (0, "1"))[-1].isnumeric()
)
print(sum(n for _, n in uniques))

# Pt 2.
parts_by_symbol = {
    (i, j, c): set(
        grid[n] for n in neighbors(y, x) if grid.get(n, (0, "."))[-1].isnumeric()
    )
    for (y, x), ((j, i), c) in grid.items()
    if c == "*"
}

print(parts_by_symbol)
print(
    sum(
        prod(int(v) for i, v in parts)
        for parts in parts_by_symbol.values()
        if len(parts) == 2
    )
)
