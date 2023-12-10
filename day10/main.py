from collections import deque
from collections import Counter
import fileinput

grid = {
    (y, x): c
    for y, row in enumerate(fileinput.input())
    for x, c in enumerate(row.strip())
}


def neighbors(y, x, c):
    match c:
        case "|":
            return ((y - 1, x), (y + 1, x))
        case "-":
            return ((y, x - 1), (y, x + 1))
        case "J":
            return ((y, x - 1), (y - 1, x))
        case "7":
            return ((y, x - 1), (y + 1, x))
        case "L":
            return ((y - 1, x), (y, x + 1))
        case "F":
            return ((y + 1, x), (y, x + 1))
        case "S":
            # Return the first viable path.
            return [
                (y + dy, x + dx)
                for dy, dx in [(-1, 0), (0, 1), (1, 0), (0, -1)]
                if grid.get((y + dy, x + dx), ".") != "."
            ][:1]
    raise ValueError(c)


def find_loop():
    [s] = [(sy, sx)] = [(y, x) for (y, x), c in grid.items() if c == "S"]
    seen = set()
    q = deque([(s, 0, set([s]))])
    while q:
        p, d, path = (y, x), d, path = q.popleft()
        if grid[p] == "S" and d > 2:
            return d // 2, path

        seen.add(p)
        for n in neighbors(y, x, grid[p]):
            if n not in seen or grid[n] == "S":
                q.append((n, d + 1, path | set([n])))


dist, loop = find_loop()

# Pt 1.
print(dist)

ys, xs = zip(*loop)
sum_in = 0
for y in range(min(ys) - 1, max(ys) + 2):
    for x in range(min(xs) - 1, max(xs) + 2):
        if (y, x) in loop:
            continue

        c = grid.get((y, x), ".")

        # Counts crossings diagonally (easy corner cases).
        yi, xi = y, x
        crossings = 0
        while yi <= max(ys) + 1 and xi <= max(xs) + 1:
            if (yi, xi) in loop and grid.get((yi, xi), ".") not in "7L":
                crossings += 1
            xi += 1
            yi += 1
        sum_in += 1 if crossings % 2 else 0

print(sum_in)
