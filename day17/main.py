import fileinput
import heapq
from collections import Counter, defaultdict, deque


# BFS, too slow for real input.
def min_path(grid):
    H, W = len(grid), len(grid[0])

    # y x cost path
    q = deque([(0, 0, 0, "")])
    seen = {}

    min_e = float("+inf")
    while q:
        y, x, cost, path = q.popleft()

        if len(path) > 0 and Counter(path[-4:]).most_common()[0][1] > 3:
            continue

        if y == H - 1 and x == W - 1:
            print("FOUND!!")

        if seen.get((y, x), float("+inf")) < cost:
            continue
        seen[(y, x)] = cost

        for dy, dx, dr in ((0, -1, "<"), (1, 0, "v"), (0, 1, ">"), (-1, 0, "^")):
            ny, nx = y + dy, x + dx
            if not (0 <= ny < H and 0 <= nx < W):
                continue
            q.append((ny, nx, cost + grid[ny][nx], path + dr))
    return seen[(H - 1, W - 1)]


OPPOSITE_DIR = {
    "v": "^",
    ">": "<",
    "<": ">",
    "^": "v",
}


def dijkstra(grid, min_steps, max_steps):
    H, W = len(grid), len(grid[0])

    # y, x, count-in-direction, direction.
    start_0, start_1 = (0, 0, 0, ">"), (0, 0, 0, "v")
    seen = set()
    dist = {
        start_0: 0,
        start_1: 0,
    }
    # cost, node.
    q = [(0, start_0), (0, start_1)]
    while q:
        # print(q)
        cost, node = cost, (y, x, count, dir) = heapq.heappop(q)
        if y == H - 1 and x == W - 1:
            return dist[node]
        if node in seen:
            continue
        seen.add(node)
        for dy, dx, dr in ((0, -1, "<"), (1, 0, "v"), (0, 1, ">"), (-1, 0, "^")):
            if dr == OPPOSITE_DIR[dir]:
                continue

            ny, nx = y + dy, x + dx
            if not (0 <= ny < H and 0 <= nx < W):
                continue
            if dr != dir and count >= min_steps:
                neighbor = (ny, nx, 1, dr)
            elif dr == dir and count < max_steps:
                neighbor = (ny, nx, count + 1, dir)
            else:
                continue
            tentative_dist = dist[node] + grid[ny][nx]
            if tentative_dist < dist.get(neighbor, float("inf")):
                dist[neighbor] = tentative_dist
                heapq.heappush(q, (tentative_dist, neighbor))


grid = [[int(c) for c in l.strip()] for l in fileinput.input()]

# Pt 1.
print(dijkstra(grid, min_steps=0, max_steps=3))

# Pt 2.
print(dijkstra(grid, min_steps=4, max_steps=10))
