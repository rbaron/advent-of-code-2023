import fileinput
import itertools
import sys

sys.setrecursionlimit(1000000)


def parse():
    dirs, nodes = "".join(fileinput.input()).split("\n\n")
    return [0 if d == "L" else 1 for d in dirs], {
        l[0:3]: (l[7:10], l[12:15]) for l in nodes.split("\n")
    }


dirs, nodes = parse()


def dist_to_zzz(node, next_dir_idx):
    if node == "ZZZ":
        return 0
    dir_ = dirs[next_dir_idx % len(dirs)]
    return 1 + dist_to_zzz(nodes[node][dir_], next_dir_idx + 1)


# Pt 1.
print(dist_to_zzz("AAA", 0))


def positions(node, next_dir_idx, curr_dist):
    yield (node, curr_dist)
    dir_ = dirs[next_dir_idx % len(dirs)]
    yield from positions(nodes[node][dir_], next_dir_idx + 1, curr_dist + 1)


def find_period(node):
    dst_by_node = {}
    for n, dst in positions(node, 0, 0):
        # Assumption: only one node ending in Z in each path.
        if n[-1] == "Z" and n in dst_by_node:
            return dst_by_node[n], dst - dst_by_node[n]
        dst_by_node[n] = dst


"""
We can find the period (Pi) and initial repetition point (t0i) for each starting point:


11A -------|----------|----------|----------|- ...
11B ---|-------|-------|-------|-------|------ ...
11C -----|---|---|---|---|---|---|---|---|---| ...
...

When do the |s align on all paths?

For a single pair of (P0, t00) and (P1, t01), the alignment will happen
every time that the equation is satisfied for a pair of integers a, b:

t00 + a * P0 = t10 + b * P1

Rearranging:

a*P0 - b*P1 = t10 - t00

We want the earliest of those, the smallest a, b that satisfy the equation.

If we had the simpler equation:

a*P0 = b*P1

Then 

a*P0 = b*P1 = L = Least Common Multiple (LCM) of P0, P1

We could find L using the Euclidian GCD algo:

L = (a*b) / GCD(a, b)

For the actual equation, we need the Extended Euclidean Algorithm. As per wiki:

[... ] the extended Euclidean algorithm is an extension to the Euclidean algorithm, and computes,
in addition to the greatest common divisor (gcd) of integers a and b, also the coefficients of
Bézout's identity, which are integers x and y such that:

a*x + b*y = gcd(a, b) = g

Which kinda sounds like what we need:

a*P0 - b*P1 = t10 - t00 

If we assume (t10 - t00) is a multiple of gcd:

a*P0 - b*P1 = k*g = t10 - t00

=> k = (t10 - t00) / g

"""

# This takes too long, needs speeding up.
t0_periods = [find_period(n) for n in nodes if n[-1] == "A"]
# print(t0_periods)
# t0_periods = [
#     (18961, 18961),
#     (12169, 12169),
#     (17263, 17263),
#     (13301, 13301),
#     (14999, 14999),
#     (16697, 16697),
# ]


# Borrowed from https://www.geeksforgeeks.org/python-program-for-basic-and-extended-euclidean-algorithms-2/
def gcde(a, b):
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = gcde(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


(P, t), *t0_periods = t0_periods
for Pi, ti in t0_periods:
    # Borrowed from https://math.stackexchange.com/a/3864593
    g, a, b = gcde(P, Pi)
    z = (t - ti) // g
    P = P // g * Pi
    t = a - b * z * P

# Pt 2.
print(P)
