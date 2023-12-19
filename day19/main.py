import fileinput
import re
import operator


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
        return [int(n) for n in re.findall(r"\d+", p)]

    return dict(rule for wf in wfs.split("\n") for rule in parse_wf(wf.strip())), [
        parse_part(p) for p in parts.split("\n")
    ]


def apply_rule(part, name, rules):
    if name in ["A0", "R0"]:
        return name
    cat, op, v, nxt_if, nxt_else = rules[name]
    if cat is None:
        return apply_rule(part, nxt_if, rules)
    idx = {c: i for i, c in enumerate("xmas")}[cat]
    nxt = (
        nxt_if
        if (operator.gt if op == ">" else operator.lt)(part[idx], v)
        else nxt_else
    )
    return apply_rule(part, nxt, rules)


rules, parts = parse()
print(rules)

# Pt 1.
print(sum(c for p in parts for c in p if apply_rule(p, "in0", rules) == "A0"))

# print([apply_rule(p, "in0", rules) for p in parts[:1]])
