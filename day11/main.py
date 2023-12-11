import fileinput
import itertools


def transpose(rows):
    return ["".join(r) for r in zip(*rows)]


def read_galaxies(expansion_factor):
    def expand(rows):
        for r in rows:
            if all(c == "." for c in r):
                yield r
            yield r

    def find_empty_idx(rows):
        for i, r in enumerate(rows):
            if all(c == "." for c in r):
                yield i

    G = [l.strip() for l in fileinput.input()]
    empty_rows = set(find_empty_idx(G))
    empty_cols = set(find_empty_idx(transpose(G)))
    add_row = 0
    for y, row in enumerate(G):
        add_col = 0
        if y in empty_rows:
            add_row += expansion_factor - 1
        for x, c in enumerate(row):
            if x in empty_cols:
                add_col += expansion_factor - 1
            if c == "#":
                yield (y + add_row, x + add_col)


def sum_dists(expansion_factor):
    G = list(read_galaxies(expansion_factor))
    return sum(
        abs(y1 - y2) + abs(x1 - x2)
        for (y1, x1), (y2, x2) in itertools.combinations(G, r=2)
    )


# Pt 1.
print(sum_dists(expansion_factor=2))

# Pt 2.
print(sum_dists(expansion_factor=1_000_000))
