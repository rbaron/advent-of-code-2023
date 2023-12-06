"""

seed:
    soil,
    [ range1 range2]
],

from:
    to,
    [range1, range2, ...]

range := dst0, src0, len

"""
import fileinput
import re


def parse_map(blk):
    lines = blk.split("\n")
    HDR = re.compile(r"(\w+)-to-(\w+) map:")
    from_, to = HDR.match(lines[0]).groups()
    return from_, {
        "to": to,
        "ranges": [tuple(int(n) for n in l.strip().split(" ")) for l in lines[1:]],
    }


def lookup(n, from_):
    map = maps[from_]
    for dst, src, len in map["ranges"]:
        if src <= n <= src + len:
            return dst + n - src
    return n


def find_loc(n):
    type_ = "seed"
    while type_ != "location":
        n = lookup(n, type_)
        type_ = maps[type_]["to"]
    return n


blks = "".join(fileinput.input()).split("\n\n")
seeds = [int(n) for n in blks[0].split(":")[1].strip().split(" ")]
maps = dict(parse_map(b) for b in blks[1:])

# Pt 1.
print(min(find_loc(s) for s in seeds))


# Pt 2.
def gen_f_ranges(ranges):
    ranges = sorted(ranges, key=lambda r: r[1])
    _, first_src, _ = ranges[0]
    yield ((float("-inf"), first_src - 1, lambda n: n))
    # Assume ranges are contiguous (seems to be from eyeballing the input).
    for d, s, l in ranges:
        yield (s, s + l - 1, lambda n: d - s + n)
    _, last_src, last_len = ranges[-1]
    yield ((last_src + last_len, float("+inf"), lambda n: n))


seeds = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]

queue = [("seed", a, a + b) for a, b in seeds]
min_loc = float("+inf")
while queue:
    from_, a, b = queue.pop()

    if from_ == "location":
        min_loc = min(min_loc, a)
        continue

    m = maps[from_]
    for ra, rb, f in gen_f_ranges(m["ranges"]):
        ia = max(a, ra)
        ib = min(b, rb)
        if ia <= ib:
            queue.append((m["to"], f(ia), f(ib)))

print(min_loc)
