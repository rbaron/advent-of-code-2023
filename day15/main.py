from __future__ import annotations
import fileinput
from dataclasses import dataclass

strs = "".join(fileinput.input()).split(",")


def hash(s):
    curr = 0
    for c in s:
        curr = (17 * (ord(c) + curr)) % 256
    return curr


# Pt 1.
print(sum(hash(i) for i in strs))


# (op, key, value | None)
def mk_instr(s):
    if s[-1] == "-":
        return ("rm", s[:-1], None)
    return ("add",) + tuple(s.split("="))


instrs = [mk_instr(s) for s in strs]
# print(instrs)


@dataclass
class Entry:
    key: str
    val: str
    next: Entry


boxes = {}


def rm(k):
    box = boxes.get(hash(k))
    if box and box.key == k:
        boxes[hash(k)] = box.next
        return

    while box is not None:
        if box.next and box.next.key == k:
            box.next = box.next.next
            return
        box = box.next


def add(k, v):
    box = boxes.get(hash(k))
    if box is None:
        boxes[hash(k)] = Entry(k, v, None)
        return
    elif box.key == k:
        box.val = v
        return

    while box is not None:
        if box.next is None:
            # Add
            box.next = Entry(k, v, None)
            return
        elif box.next.key == k:
            # Update
            box.next.val = v
            return
        box = box.next


for op, k, v in instrs:
    if op == "rm":
        rm(k)
    elif op == "add":
        add(k, v)

res = 0
for b, entry in boxes.items():
    i = 0
    while entry is not None:
        res += (b + 1) * (i + 1) * int(entry.val)
        i += 1
        entry = entry.next

print(res)
