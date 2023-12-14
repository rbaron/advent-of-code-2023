import fileinput

G = [list(f.strip()) for f in fileinput.input()]
N = len(G)


def tilt_north(G):
    for x in range(N):
        nxt = 0
        for y in range(N):
            match G[y][x]:
                case ".":
                    pass
                case "O":
                    if nxt == y:
                        nxt += 1
                        continue
                    G[nxt][x] = "O"
                    G[y][x] = "."
                    nxt += 1
                case "#":
                    nxt = y + 1
    return G


def load(G):
    return sum(N - y for y, row in enumerate(G) for x, c in enumerate(row) if c == "O")


# Pt 1.
print(load(tilt_north(G)))


def rot90(G):
    T = zip(*G)
    return [list(reversed(r)) for r in T]


def run_once_cycle(G):
    for _ in range(4):
        G = rot90(tilt_north(G))
    return G


M = 1_000_000_000


def to_hashable(G):
    return tuple(tuple(r) for r in G)


def find_rep(G):
    cache = {}
    i = 0
    while i < M:
        Gh = to_hashable(G)
        if Gh in cache:
            """
            0                                    100
               7   17   27   37   47 .... 97
            """
            cycle_len = i - cache[Gh]
            nc = (M - i) // cycle_len
            i += nc * cycle_len
        cache[Gh] = i
        G = run_once_cycle(G)
        i += 1
    return G


# Pt 2.
print(load(find_rep(G)))
