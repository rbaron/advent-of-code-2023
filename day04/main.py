import fileinput
import re

PATT = re.compile(r"^Card .+: (.+) \| (.+)$")


numbers = [
    tuple(set(map(int, g.split())) for g in PATT.match(l).groups())
    for l in fileinput.input()
]

# Pt 1.
print(sum(1 << (len(h & w) - 1) if h & w else 0 for h, w in numbers))

# Pt 2.
pile = {(n + 1): 1 for n in range(len(numbers))}
remains = {(n + 1): 0 for n in range(len(numbers))}
while any(pile.values()):
    n, counts = next(iter((n, c) for n, c in pile.items() if c > 0))
    pile[n] = 0
    remains[n] += counts
    h, w = numbers[n - 1]
    for card_n in range(n + 1, min(n + 1 + len(h & w), (len(numbers) + 1))):
        pile[card_n] += counts


print(sum(remains.values()))
