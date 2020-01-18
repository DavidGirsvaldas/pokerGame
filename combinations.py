from typing import Iterable
from rank import Rank


def find_high_card(ace: Iterable[Rank]):
    max_rank = 0
    for e in ace:
        if e.value > max_rank:
            max_rank = e
    return Rank(max_rank)
