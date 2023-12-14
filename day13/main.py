import fileinput


blks = [
    [l.strip() for l in blk.split("\n")]
    for blk in "".join(fileinput.input()).split("\n\n")
]


def ref_point(blk, required_diffs=0):
    H = len(blk)
    for i in range(0, H - 1):
        max_h = min(i + 1, H - i - 1)
        if (
            sum(
                a != b for j in range(max_h) for a, b in zip(blk[i - j], blk[i + 1 + j])
            )
            == required_diffs
        ):
            return i + 1
    return 0


def score(blk, required_diffs=0):
    return 100 * ref_point(blk, required_diffs) + ref_point(
        list(zip(*blk)), required_diffs
    )

# Pt 1.
print(sum(score(b) for b in blks))

# Pt 2.
print(sum(score(b, required_diffs=1) for b in blks))
