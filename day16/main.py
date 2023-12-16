import fileinput
from collections import deque


def next_pos(y, x, d, grid):
    c = grid[y][x]
    if d == ">":
        if c in ".-":
            yield (y, x + 1, d)
        if c in "\\|":
            yield (y + 1, x, "v")
        if c in "/|":
            yield (y - 1, x, "^")
    elif d == "v":
        if c in ".|":
            yield (y + 1, x, d)
        if c in "\\-":
            yield (y, x + 1, ">")
        if c in "/-":
            yield (y, x - 1, "<")
    elif d == "<":
        if c in ".-":
            yield (y, x - 1, d)
        if c in "\\|":
            yield (y - 1, x, "^")
        if c in "/|":
            yield (y + 1, x, "v")
    elif d == "^":
        if c in ".|":
            yield (y - 1, x, d)
        if c in "\\-":
            yield (y, x - 1, "<")
        if c in "/-":
            yield (y, x + 1, ">")


def cast(y, x, d, grid):
    H, W = len(grid), len(grid[0])
    q = deque([(y, x, d)])
    seen = set()
    while q:
        entry = y, x, d = q.popleft()
        if not (0 <= y < H and 0 <= x < W):
            continue
        if entry in seen:
            continue
        seen.add(entry)

        q.extend(next_pos(y, x, d, grid))

    return len({(y, x) for y, x, _ in seen})


G = [l.strip() for l in fileinput.input()]

# Pt 1.
print(cast(0, 0, ">", G))


def gen_pos0(grid):
    H, W = len(grid), len(grid[0])
    yield from ((0, x, "v") for x in range(W))
    yield from ((H - 1, x, "^") for x in range(W))
    yield from ((y, 0, ">") for y in range(H))
    yield from ((y, W - 1, "<") for y in range(H))


# Pt 2.
print(max(cast(y, x, d, G) for y, x, d in gen_pos0(G)))
