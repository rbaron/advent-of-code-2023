import fileinput
import itertools

seqs = [[int(n) for n in l.strip().split(" ")] for l in fileinput.input()]


def deriv(seq):
    return [b - a for a, b in itertools.pairwise(seq)]


def fill(seq):
    if not any(seq):
        return (0, 0)
    last_dx, sum_ = fill(deriv(seq))
    new_val = seq[-1] + last_dx
    return new_val, sum_ + new_val


print(sum(fill(s)[0] for s in seqs))

print(sum(fill(list(reversed(s)))[0] for s in seqs))
