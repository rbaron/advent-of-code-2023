import fileinput
from math import sqrt, ceil
from functools import prod

# records = [(7, 9), (15, 40), (30, 200)]
records = [(48, 255), (87, 1288), (69, 1117), (81, 1623)]

# Pt 1.
p = 1
for t, d in records:
    s = 0
    for t_p in range(t):
        # Second degree equation.
        total_dist = (t - t_p) * t_p
        # print(f"{t=} {d=} {t_p=}: {total_dist=}")
        s += total_dist > d
    p *= s

# Pt 2.
# records = [(71530, 940200)]
records = [(48876981, 255128811171623)]

[(t0, d0)] = records
a = -1
b = t0
c = -d0 + 1

delta = b**2 - 4 * a * c
x1 = (-b + sqrt(delta)) / (2 * a)
x2 = (-b - sqrt(delta)) / (2 * a)

print(ceil(x2) - ceil(x1))
