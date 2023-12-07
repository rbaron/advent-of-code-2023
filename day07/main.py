import fileinput
from collections import Counter
from enum import IntEnum

STRENGTH = {card: s for s, card in enumerate("AKQJT98765432")}


class HandType(IntEnum):
    FIVE_OF_A_KIND = 0
    FOUR_OF_A_KIND = 1
    FULL_HOUSE = 2
    THREE_OF_A_KIND = 3
    TWO_PAIR = 4
    ONE_PAIR = 5
    HIGH_CARD = 6


def maybe_replace_joker(hand):
    j_counts = sum(1 for c in hand if c == "J")

    if j_counts == 0:
        return hand
    elif j_counts == 5:
        return "AAAAA"

    counts_wo_j = sorted(
        ((count, card) for card, count in Counter(c for c in hand if c != "J").items()),
        reverse=True,
    )

    # Map Jokers to the card with the (highest count, highest strength).
    counts_wo_j_with_strength = list(
        sorted((-count, STRENGTH[card], card) for count, card in counts_wo_j)
    )

    _, _, replacement = next(iter(counts_wo_j_with_strength))
    return "".join(c if c != "J" else replacement for c in hand)


def hand_type(hand, replace_joker=False):
    if replace_joker:
        hand = maybe_replace_joker(hand)

    c = tuple(sorted(Counter(hand).values(), reverse=True))
    match c:
        case (5,):
            return HandType.FIVE_OF_A_KIND
        case (4, 1):
            return HandType.FOUR_OF_A_KIND
        case (3, 2):
            return HandType.FULL_HOUSE
        case (3, 1, 1):
            return HandType.THREE_OF_A_KIND
        case (2, 2, 1):
            return HandType.TWO_PAIR
        case (2, 1, 1, 1):
            return HandType.ONE_PAIR
        case (1, 1, 1, 1, 1):
            return HandType.HIGH_CARD
    raise ValueError(c)


# Returns a tuple that can be compared by hand strength and is capable of breaking ties.
def hand_type_and_strengths(hand, replace_joker=False):
    return (hand_type(hand, replace_joker),) + tuple(STRENGTH[c] for c in hand)


hands_bids = tuple(
    tuple(part for part in line.strip().split(" ")) for line in fileinput.input()
)

# Pt 1.
ranked = sorted(hands_bids, key=lambda kv: hand_type_and_strengths(kv[0]), reverse=True)
print(sum(((r + 1) * int(bid) for r, (_, bid) in enumerate(ranked))))

# Pt 2.
STRENGTH = {card: s for s, card in enumerate("AKQT98765432J")}
ranked = sorted(
    hands_bids,
    key=lambda kv: hand_type_and_strengths(kv[0], replace_joker=True),
    reverse=True,
)
print(sum(((r + 1) * int(bid) for r, (_, bid) in enumerate(ranked))))
