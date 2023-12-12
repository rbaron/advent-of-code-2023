import fileinput
from functools import cache


def parse():
    out = []
    for r in fileinput.input():
        assignments, counts = r.strip().split(" ")
        out.append((assignments, tuple(map(int, counts.split(",")))))
    return out


rows = parse()


@cache
def count_valid_assignments(row, counts, in_=False):
    if not row:
        return 1 if ((not counts) or counts == (0,)) else 0

    head, *tail = row
    tail = tuple(tail)

    # Inside damaged group.
    if in_:
        res = 0
        if head in ".?" and counts and counts[0] == 0:
            res += count_valid_assignments(tail, counts[1:], in_=False)
        if head in "#?" and counts and counts[0] > 0:
            res += count_valid_assignments(
                tail, (counts[0] - 1,) + counts[1:], in_=True
            )
        return res
    # Outside damaged group.
    else:
        res = 0
        if head in ".?":
            res += count_valid_assignments(tail, counts, in_=False)
        if head in "#?" and counts and counts[0] > 0:
            res += count_valid_assignments(
                tail, (counts[0] - 1,) + counts[1:], in_=True
            )
        return res


# Pt 1.
print(sum(count_valid_assignments(a, c) for a, c in rows))

# Pt 2.
N = 5
rows = [("?".join(a for _ in range(N)), c * N) for a, c in rows]
print(sum(count_valid_assignments(a, c) for a, c in rows))
