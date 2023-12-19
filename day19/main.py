import fileinput
import re
import operator
from math import prod


def parse():
    wfs, parts = "".join(fileinput.input()).split("\n\n")

    def parse_wf(wf):
        PATT = re.compile(r"(\w+)\{(.+)}")
        name, rs = PATT.match(wf).groups()

        # Each rule is (category, < or >, value, next if true, next if false)
        def parse_rule(i, r):
            RULE_PATT = re.compile(r"(\w)([<>])(\d+):(\w+)")
            if ":" in r:
                cat, op, v, nxt = RULE_PATT.match(r).groups()
                return (f"{name}{i}", (cat, op, int(v), f"{nxt}0", f"{name}{i + 1}"))
            else:
                return (f"{name}{i}", (None, None, None, f"{r}0", None))

        return [parse_rule(i, r) for i, r in enumerate(rs.split(","))]

    def parse_part(p):
        return {cat: int(n) for cat, n in zip("xmas", re.findall(r"\d+", p))}

    return dict(rule for wf in wfs.split("\n") for rule in parse_wf(wf.strip())), [
        parse_part(p) for p in parts.split("\n")
    ]


def apply_rule(part, name, rules):
    if name in ["A0", "R0"]:
        return name
    cat, op, v, nxt_if, nxt_else = rules[name]
    if cat is None:
        return apply_rule(part, nxt_if, rules)
    nxt = (
        nxt_if
        if (operator.gt if op == ">" else operator.lt)(part[cat], v)
        else nxt_else
    )
    return apply_rule(part, nxt, rules)


rules, parts = parse()

# Pt 1.
print(sum(c for p in parts for c in p.values() if apply_rule(p, "in0", rules) == "A0"))


def combinations_in_range(part):
    def seg_len(a, b):
        return b - a + 1

    return prod(seg_len(a, b) for a, b in part.values())


# Each `part` category is now a range [a, b] (inclusive).
def count_combinations(part, name, rules):
    if name == "A0":
        return combinations_in_range(part)
    elif name == "R0":
        return 0

    # Empty segments.
    if any(b < a for a, b in part.values()):
        return 0

    cat, op, val, nxt_if, nxt_else = rules[name]

    # If unconditional branching, go there.
    if cat is None:
        return count_combinations(part, nxt_if, rules)

    # Otherwise we have a if-else rule and may need to split one of the segments of part.
    sega, segb = part[cat]

    # Does `val` split `seg`?
    if sega <= val <= segb:
        if op == "<":
            d1 = {cat: (sega, val - 1)}
            d2 = {cat: (val, segb)}
            return count_combinations(
                dict(part, **d1), nxt_if, rules
            ) + count_combinations(dict(part, **d2), nxt_else, rules)
        elif op == ">":
            d1 = {cat: (val + 1, segb)}
            d2 = {cat: (sega, val)}
            return count_combinations(
                dict(part, **d1), nxt_if, rules
            ) + count_combinations(dict(part, **d2), nxt_else, rules)
    elif val < sega:
        if op == "<":
            return count_combinations(part, nxt_if, rules)
    elif val > sega:
        if op == ">":
            return count_combinations(part, nxt_if, rules)
    return 0


part = {
    "x": (1, 4000),
    "m": (1, 4000),
    "a": (1, 4000),
    "s": (1, 4000),
}

# Pt 2.
print(count_combinations(part, "in0", rules))
