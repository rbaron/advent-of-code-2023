import fileinput
import itertools

seqs = [[int(n) for n in l.strip().split(" ")] for l in fileinput.input()]


def deriv(seq):
    return [b - a for a, b in itertools.pairwise(seq)]


def fill(seq):
    if not any(seq):
        return 0
    return seq[-1] + fill(deriv(seq))


print(sum(fill(s) for s in seqs))

print(sum(fill(s[::-1]) for s in seqs))
