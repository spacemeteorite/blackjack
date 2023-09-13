from collections import namedtuple
from random import shuffle

Card = namedtuple('Card', ['rank', 'suit'])


class Deck:
    def __init__(self):
        self._ranks = list("A23456789") + ["10"] + list("JQK")
        print(self._ranks)
        self._suits = "diamonds clubs hearts spades".split()
        self.cards = [Card(rank, suit)
                      for rank in self._ranks
                      for suit in self._suits]

    def __getitem__(self, item: int):
        return self.cards[item]

    def __setitem__(self, key, value):
        self.cards[key] = value

    def __len__(self):
        return len(self.cards)

