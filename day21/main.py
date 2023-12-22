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

    # (y, x, steps) = set of tiles in which we've been in this coord.
    tiles_by_coord = defaultdict(set)
    while q:
        y, x, steps = q.popleft()
        # if steps < 0 or grid.get((y, x), "#") == "#" or (y, x, steps) in seen:
        if steps < 0 or lookup(grid, y, x, ymax, xmax) == "#" or (y, x, steps) in seen:
            continue
        seen.add((y, x, steps))
        # tiles_by_coord[(y, x, steps)].add((0, 0))

        q.extend(
            (y + dy, x + dx, steps - 1) for dy, dx in ((-1, 0), (0, 1), (1, 0), (0, -1))
        )
        # for dy, dx in ((-1, 0), (0, 1), (1, 0), (0, -1)):
        #     ny, nx = y + dy, x + dx
        #     dty, ny = divmod(ny, ymax + 1)
        #     dtx, nx = divmod(nx, xmax + 1)
        #     for ty, tx in tiles_by_coord[(y, x, steps)]:
        #         tiles_by_coord[(ny, nx, steps - 1)].add((ty + dty, tx + dtx))
        #     else:
        #         tiles_by_coord[(ny, nx, steps - 1)].add((0 + dty, 0 + dtx))
        #     q.append((ny, nx, steps - 1))

    # ty, tx = 5, 5
    # for y in range(-ty * (ymax + 1), ty * (ymax + 1)):
    #     for x in range(-tx * (xmax + 1), tx * (xmax + 1)):
    #         print(
    #             # "O" if (y, x, 0) in seen else grid[(y % (ymax + 1), x % (xmax + 1))],
    #             "S" if (y, x) == (sy, sx) else "O" if (y, x, 0) in seen else " ",
    #             end="",
    #         )
    #         # print(
    #         #     len(tiles_by_coord[(y, x, 0)]) if (y, x, 0) in seen else grid[(y, x)],
    #         #     end="",
    #         # )
    #     print()
    # return sum(1 for y, x, steps in seen if steps == 0)
    # return sum(len(tiles_by_coord[(y, x, 0)]) for y, x, steps in seen if steps == 0)

    # Number of Os in S line.
    # return sum(y for y, x, steps in seen if steps == 0 and y == sy - 1)
    return Counter(y for y, x, steps in seen if steps == 0)


G = {
    (y, x): c
    for y, line in enumerate(fileinput.input())
    for x, c in enumerate(line.strip())
}

# Pt 1.
# print(walk(G, steps=64))

# print(walk(G, steps=64))
# print(walk(G, steps=26501365))

# 1594
# print(walk(G, steps=50))

# print(walk(G, steps=120))

# for steps in range(16, 100, 2):
#     print(steps, ",", walk(G, steps))
#     # print(walk(G, steps))
MAX_STEP = 50
count_by_step = {steps: walk(G, steps) for steps in range(16, MAX_STEP + 1, 2)}
print(count_by_step)

print(",".join(map(str, count_by_step.keys())))
for y in range(-MAX_STEP, MAX_STEP + 1):
    for step, counter in count_by_step.items():
        print(f"{counter.get(y, 0)},", end="")
    print()

# for steps in range(64, 200, 10):
#     print(steps, ",", walk(G, steps))

# for steps in range(10, 500, 10):
#     print(steps, ",", walk(G, steps))

# lookup(G, -1, -7, 10, 10)
