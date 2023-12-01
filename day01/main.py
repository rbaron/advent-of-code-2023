import fileinput

lines = list(fileinput.input())
first_last = lambda l: int("".join((l[0], l[-1])))

# Pt 1.
print(sum(first_last([c for c in l if "0" <= c <= "9"]) for l in lines))

# Pt 2.
VALS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def subs(line):
    out = []
    for i, c in enumerate(line):
        if "0" <= c <= "9":
            out.append(c)
        for k, v in VALS.items():
            if k == line[i : i + len(k)]:
                out.append(str(v))
    return out


print(sum(first_last(subs(l)) for l in lines))
