import fileinput
import re
import operator


def parse():
    wfs, parts = "".join(fileinput.input()).split("\n\n")

    def parse_wf(wf):
        PATT = re.compile(r"(\w+)\{(.+)}")
        name, rs = PATT.match(wf).groups()

        def parse_rule(r):
            RULE_PATT = re.compile(r"(\w)([<>])(\d+):(\w+)")
            if ":" in r:
                cat, op, v, nxt = RULE_PATT.match(r).groups()
                return (cat, op, int(v), nxt)
            else:
                return (None, None, None, r)

        return name, [parse_rule(r) for r in rs.split(",")]

    def parse_part(p):
        return [int(n) for n in re.findall(r"\d+", p)]

    return dict(parse_wf(wf.strip()) for wf in wfs.split("\n")), [
        parse_part(p) for p in parts.split("\n")
    ]


def apply_rule(part, rule):
    cat, op, v, nxt = rule
    if cat is None:
        return nxt
    idx = {c: i for i, c in enumerate("xmas")}[cat]
    return nxt if (operator.gt if op == ">" else operator.lt)(part[idx], v) else False


def apply_rules(part, rules):
    for r in rules:
        if res := apply_rule(part, r):
            return res


def apply(part, wfs, name):
    res = apply_rules(part, wfs[name])
    if res in "AR":
        return res
    return apply(part, wfs, res)


wfs, parts = parse()
# print(wfs, parts)

print(sum(c for p in parts for c in p if apply(p, wfs, "in") == "A"))
# print([apply(p, wfs, "in") for p in parts])
