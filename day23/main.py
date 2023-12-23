from collections import defaultdict, deque
import fileinput


def parse():
    return {
        (y, x): c
        for y, l in enumerate(fileinput.input())
        for x, c in enumerate(l.strip())
    }


def bfs(grid, ymax, xmax, goal):
    # (y, x), dist, seen
    q = deque([((0, 1), 0, frozenset())])
    max_dist = 0
    while q:
        # node = pos, *_ = (y, x), dist = q.pop()
        node = (y, x), *_ = pos, dist, seen = q.pop()
        if pos == goal:
            max_dist = max(max_dist, dist)
            continue
        if not (0 <= y <= ymax and 0 <= x <= xmax) or grid[pos] == "#" or pos in seen:
            continue
        # seen.add(node)

        if grid[pos] == ".":
            q.extend(
                ((y + dy, x + dx), dist + 1, seen | {pos})
                for dy, dx in ((-1, 0), (0, 1), (1, 0), (0, -1))
            )
        elif grid[pos] == ">":
            q.append(((y, x + 1), dist + 1, seen | {pos}))
        elif grid[pos] == "<":
            q.append(((y, x - 1), dist + 1, seen | {pos}))
        elif grid[pos] == "v":
            q.append(((y + 1, x), dist + 1, seen | {pos}))
    return max_dist


def bfs2(grid, goal):
    # (y, x), dist, seen
    q = deque([((0, 1), 0, frozenset())])
    max_dist = 0
    while q:
        node = (y, x), *_ = pos, dist, seen = q.pop()
        if pos == goal:
            max_dist = max(max_dist, dist)
            continue
        if not (0 <= y <= ymax and 0 <= x <= xmax) or grid[pos] == "#" or pos in seen:
            continue
        q.extend((n, dist + d, seen | {pos}) for (n, d) in grid[pos])
    return max_dist


def compress(grid, start, ymax, xmax):
    # pos, from
    seen = set()
    # pos, from, dist
    q = deque([(start, start, 0)])
    transitions = defaultdict(list)

    def neighbors(pos):
        y, x = pos
        return [
            (y + dy, x + dx)
            for dy, dx in ((-1, 0), (0, 1), (1, 0), (0, -1))
            if grid.get(((y + dy), (x + dx)), "#") in ".<>v"
        ]

    while q:
        pos, from_, dist = q.popleft()
        node = (pos, from_)

        if pos == (ymax, xmax - 1):
            # print("GOAL", from_)
            transitions[from_].append((pos, dist))
            continue

        if node in seen:
            continue
        seen.add(node)

        ns = neighbors(pos)
        if len(ns) <= 2:
            q.extend((n, from_, dist + 1) for n in ns)
        # We have a junction.
        elif len(ns) >= 3:
            transitions[from_].append((pos, dist))
            q.extend((n, pos, 1) for n in ns)

    return transitions


G = parse()
ymax, xmax = map(max, zip(*G))

# Pt 1.
print(bfs(G, ymax, xmax, goal=(ymax, xmax - 1)))

# Pt 2.
G = compress(G, (0, 1), ymax, xmax)
print(bfs2(G, goal=(ymax, xmax - 1)))
