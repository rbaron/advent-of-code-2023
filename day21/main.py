import fileinput
from collections import Counter, defaultdict, deque


def lookup(grid, y, x, ymax, xmax):
    # k mod len
    y = y % (ymax + 1)
    x = x % (xmax + 1)
    return grid[(y, x)]


def walk(grid, steps):
    (sy, sx), *_ = [(y, x) for (y, x), v in grid.items() if v == "S"]
    ymax, xmax = map(max, zip(*grid.keys()))
    q = deque([(sy, sx, steps)])
    seen = set()
    while q:
        y, x, steps = q.popleft()
        if steps < 0 or lookup(grid, y, x, ymax, xmax) == "#" or (y, x, steps) in seen:
            continue
        seen.add((y, x, steps))
        q.extend(
            (y + dy, x + dx, steps - 1) for dy, dx in ((-1, 0), (0, 1), (1, 0), (0, -1))
        )

    # ty, tx = 5, 5
    # for y in range(-ty * (ymax + 1), ty * (ymax + 1)):
    #     for x in range(-tx * (xmax + 1), tx * (xmax + 1)):
    #         print(
    #             # "O" if (y, x, 0) in seen else grid[(y % (ymax + 1), x % (xmax + 1))],
    #             "S" if (y, x) == (sy, sx) else "O" if (y, x, 0) in seen else " ",
    #             end="",
    #         )
    #     print()
    return sum(1 for y, x, steps in seen if steps == 0)


G = {
    (y, x): c
    for y, line in enumerate(fileinput.input())
    for x, c in enumerate(line.strip())
}

# Pt 1.
print(walk(G, steps=64))

# Pt 2.
# [(0, 3738), (1, 33270), (2, 92194)]
steps = [(i, walk(G, steps=65 + i * 131)) for i in range(3)]

# fit steps(x) = 3738 + 14836x + 14696x^2
# Eval steps((26501365 - 65) / 131)
x = (26501365 - 65) // 131
print(3738 + 14836 * x + 14696 * x**2)
