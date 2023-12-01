import fileinput

lines = list(fileinput.input())
first_last = lambda l: int("".join((l[0], l[-1])))

# Pt 1.
print(sum(first_last([c for c in l if "0" <= c <= "9"]) for l in lines))

# Pt 2.
SUBS = {
    s: str(i)
    for i, s in enumerate(
        ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
    )
}


def subs(line):
    out = []
    for i, c in enumerate(line):
        if "0" <= c <= "9":
            out.append(c)
        for k, v in SUBS.items():
            if k == line[i : i + len(k)]:
                out.append(v)
    return out


print(sum(first_last(subs(l)) for l in lines))
