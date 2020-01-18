from typing import Iterable
from rank import Rank
from collections import defaultdict


def find_high_card(ranks: Iterable[Rank]):
    max_rank = 0
    for r in ranks:
        if r.value > max_rank:
            max_rank = r
    return Rank(max_rank)


def find_four_of_a_kind(ranks: Iterable[Rank]):
    rank_occupancies = defaultdict()
    for r in ranks:
        if not (r in rank_occupancies):
            rank_occupancies[r] = 0
        rank_occupancies[r] += 1
        if rank_occupancies[r] == 4:
            return r
    return None
