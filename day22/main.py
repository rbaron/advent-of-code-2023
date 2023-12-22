from collections import Counter, defaultdict, deque
import fileinput


def parse_blks():
    def parse_line(line):
        bs = line.strip().split("~")
        return tuple(tuple([int(c.strip()) for c in b.split(",")]) for b in bs)

    # Sort by low_z.
    return list(
        sorted(tuple(map(parse_line, fileinput.input())), key=lambda k: k[0][-1])
    )


def intersect_xy(blk1, blk2):
    (lox1, loy1, _), (hix1, hiy1, _) = blk1
    (lox2, loy2, _), (hix2, hiy2, _) = blk2

    def intersect_seg(a1, b1, a2, b2):
        return max(a1, a2) <= min(b1, b2)

    return intersect_seg(lox1, hix1, lox2, hix2) and intersect_seg(
        loy1, hiy1, loy2, hiy2
    )


def settle(blks):
    final_blks = []
    below = defaultdict(set)
    above = defaultdict(set)
    # Assumes sorted lo, hi.
    for i, blk in enumerate(blks):
        blks_intersect_xy_blw = [b for b in final_blks if intersect_xy(blk, b)]

        (lox, loy, loz), (hix, hiy, hiz) = blk
        if not blks_intersect_xy_blw:
            final_blks.append(((lox, loy, 1), (hix, hiy, hiz - loz + 1)))
            continue

        highest_z = max(z for _, (_, _, z) in blks_intersect_xy_blw)
        blk = (lox, loy, highest_z + 1), (hix, hiy, highest_z + hiz - loz + 1)
        blks_intersect_xy_blw = [
            b for b in blks_intersect_xy_blw if b[1][-1] == highest_z
        ]
        for b in blks_intersect_xy_blw:
            above[b].add(blk)
            below[blk].add(b)

        final_blks.append(blk)

    return final_blks, above, below


def chain(blk, above, below):
    q = deque((blk,))
    destroyed = set()
    while q:
        b = q.popleft()
        if len(below[b] - destroyed) == 0 or b == blk:
            destroyed.add(b)
            q.extend(above[b])
    return len(destroyed)


blks, above, below = settle(parse_blks())

# Pt 1.
print(sum(1 for blk in blks if all(len(below[abv_blk]) > 1 for abv_blk in above[blk])))

# Pt 2.
print(sum(chain(blk, above, below) - 1 for blk in blks))
