import collections
import fileinput
import itertools
import z3


def parse():
    def parse_line(l):
        return tuple(tuple(map(int, v.split(","))) for v in l.strip().split(" @ "))

    return tuple(map(parse_line, fileinput.input()))


# Returns (a, b) for eq ax + b.
def to_xy_line_eq(hail):
    (px, py, _), (vx, vy, _) = hail
    a = vy / vx
    return a, py - a * px


# Given 2 xy lines, return (x, y) of their intersect.
def intersection_xy(h1, h2):
    (a1, b1), (a2, b2) = to_xy_line_eq(h1), to_xy_line_eq(h2)
    # Parallel.
    if a1 == a2 and b1 != b2:
        return float("inf"), float("inf"), "paral"
    elif a1 == a2 and b1 == b2:
        return 0, 0, "coinc"
    x = (b2 - b1) / (a1 - a2)
    y = a1 * x + b1
    ((_, y10, _), (_, v1y, _)), ((_, y20, _), (_, v2y, _)) = h1, h2

    def same_sign(n0, n1):
        return n0 * n1 >= 0

    return (
        (x, y, "ok")
        if same_sign(y - y10, v1y) and same_sign(y - y20, v2y)
        else (float("inf"), float("inf"), "past")
    )


def all_intersections(hails):
    return (intersection_xy(h1, h2) for h1, h2 in itertools.combinations(hails, r=2))


def solve(hails):
    xt, yt, zt, vtx, vty, vtz = z3.Ints("xt yt zt vtx vty vtz")
    tc0, tc1, tc2 = z3.Ints("tc0 tc1 tc2")
    tcs = [tc0, tc1, tc2]
    # eqs = []
    solver = z3.Solver()
    for i, ((x0, y0, z0), (vx, vy, vz)) in enumerate(hails[:3]):
        solver.add(xt + vtx * tcs[i] == x0 + vx * tcs[i])
        solver.add(yt + vty * tcs[i] == y0 + vy * tcs[i])
        solver.add(zt + vtz * tcs[i] == z0 + vz * tcs[i])
    solver.check()
    model = solver.model()

    def sol(var):
        return model[var].as_long()

    return (sol(xt), sol(yt), sol(zt)), (sol(vtx), sol(vty), sol(vtz))


hails = parse()
xy_lines = [to_xy_line_eq(h) for h in hails]

# Pt 1.
# LEAST, MOST = 7, 27
LEAST, MOST = 200000000000000, 400000000000000
print(
    sum(
        1
        for (x, y, reason) in all_intersections(hails)
        if (LEAST <= x <= MOST and LEAST <= y <= MOST) or reason == "coinc"
    )
)

# Pt 2.
pos, _ = solve(hails)
print(sum(pos))
