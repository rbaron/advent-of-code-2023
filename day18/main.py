from collections import deque
import fileinput
import itertools
import re


def parse():
    PATT = re.compile(r"(.) (\d+) \(#(.+)\)")
    for l in fileinput.input():
        dir, n, color = PATT.match(l).groups()
        yield dir, int(n), color


def mkgrid(instrs):
    grid = {}
    y = x = 0

    # for dir, n, color in instrs:
    for dir, n, _ in instrs:
        match dir:
            case "U":
                for _ in range(n):
                    grid[(y, x)] = "#"
                    y += 1
            case "R":
                for _ in range(n):
                    grid[(y, x)] = "#"
                    x += 1
            case "D":
                for _ in range(n):
                    grid[(y, x)] = "#"
                    y -= 1
            case "L":
                for _ in range(n):
                    grid[(y, x)] = "#"
                    x -= 1
    return grid


def fill(grid):
    # Pick an internal point.
    q = deque([(-1, 1)])
    while q:
        p = y, x = q.pop()
        if grid.get(p) == "#":
            continue
        grid[p] = "#"
        q.extend([(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)])
    return grid


# Pt 1.
instrs = list(parse())
grid = fill(mkgrid(instrs))
print(sum(1 for v in grid.values() if v == "#"))


def mkvertices(instrs):
    y = x = 0
    for _, _, color in instrs:
        dir = "RDLU"[int(color[-1])]
        n = int(color[:-1], base=16)
        yield y, x
        match dir:
            case "U":
                y += n
            case "R":
                x += n
            case "D":
                y -= n
            case "L":
                x -= n


def count_border(vertices):
    return sum(
        abs(yb - ya if xa == xb else xb - xa)
        for (ya, xa), (yb, xb) in itertools.pairwise(vertices + vertices[:1])
    )


# Shoelace trapezoidal formula -- https://en.wikipedia.org/wiki/Shoelace_formula.
def poly_area(vertices):
    # Area may be negative depending on the direction of iteration.
    return abs(
        sum(
            (y1 + y2) * (x1 - x2)
            for (y1, x1), (y2, x2) in itertools.pairwise(vertices + vertices[:1])
        )
        // 2
    )


def inner_area(vertices, perimeter):
    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    return poly_area(vertices) - perimeter // 2 + 1


# Pt 2.
vertices = list(mkvertices(instrs))
perim = count_border(vertices)
print(inner_area(vertices, perim) + perim)
