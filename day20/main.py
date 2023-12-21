from collections import deque
from math import prod
import fileinput
import re

OFF = LO = 0
ON = HI = 1


def parse():
    PATT = re.compile(r"(\W)?(\w+) -> (.+)")

    def parse_mod(line):
        typ, name, children = PATT.match(line).groups()
        return name, {
            "type": typ or "BR",
            "children": [c.strip() for c in children.split(",")],
            "state": OFF if typ == "%" else ({} if typ == "&" else None),
        }

    mods = dict(parse_mod(l.strip()) for l in fileinput.input())
    for mod_name, mod in mods.items():
        for child in mod["children"]:
            # Output.
            if child not in mods:
                continue
            cmod = mods[child]
            if cmod["type"] == "&":
                cmod["state"][mod_name] = LO
    return mods


def print_state(mods):
    # ns = "zl xf qn xn th qx db vc gf".split()
    # ns = "th zl xf qn xn".split()
    ns = "qx".split()
    # ns = mods.keys()

    def con_state(name, state):
        return f'{name}: {",".join(map(str, state.values()))}'

    def state(name):
        mod = mods[name]
        if mod["type"] == "&":
            return con_state(name, mod["state"])
        return f'{name}: {mod["state"]}'

    print("; ".join(state(n) for n in ns))


def propagate(push_times, mods):
    # signal, to, from
    counts = {LO: 0, HI: 0}
    for n_pushes in range(push_times):
        q = deque([(LO, "broadcaster", "button")])
        # print_state(mods)
        # print("push")
        while q:
            signal, to, from_ = q.popleft()
            counts[signal] += 1

            # if signal == LO and to == "rx":
            #     return mods, counts, n_pushes + 1
            # if to == "rx":
            #     print(mods["th"]["state"])

            for n in "zl xf qn xn".split():
                if to == n and all(s == LO for s in mods[n]["state"].values()):
                    print("ok!,", n, n_pushes + 1)
                    # print_state(mods)

            # Unnamed
            if to not in mods:
                continue

            mod = mods[to]
            # print(signal, to, from_)

            if mod["type"] == "BR":
                q.extend((signal, c, "broadcaster") for c in mod["children"])
            elif mod["type"] == "%" and signal == LO:
                q.extend(
                    (HI if mod["state"] == OFF else LO, c, to) for c in mod["children"]
                )
                mod["state"] = not mod["state"]
            elif mod["type"] == "&":
                mod["state"][from_] = signal
                if all(i == HI for i in mod["state"].values()):
                    q.extend((LO, c, to) for c in mod["children"])
                else:
                    q.extend((HI, c, to) for c in mod["children"])
        # print(mods)
        # print()

    return mods, counts, n_pushes + 1


def to_dot(mods):
    with open("graph.dot", "w") as f:
        f.write("digraph G {\n")
        for name, attrs in mods.items():
            f.write(f'{name} [label="{attrs["type"] + name}"];\n')
            for child in attrs["children"]:
                f.write(f"{name} -> {child};\n")
        f.write("}\n")


mods = parse()
# print(mods)

# mods, counts, pushes = propagate(1000, mods)
# print(prod(counts.values()))

mods, counts, pushes = propagate(10000000000000000000000000, mods)
print(pushes)

# to_dot(mods)

# 555799119414 too low
# 220325231288870 too low
# 224046542165867 correct!
