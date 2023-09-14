from collections import namedtuple
from random import shuffle



Card = namedtuple('Card', ['rank', 'suit'])


VALUE_DICT = {'A': 11, 
            '2': 2, 
            '3': 3, 
            '4': 4, 
            '5': 5, 
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'J': 10,
            'Q': 10,
            'K': 10,
            }



class Deck:
    

    def __init__(self):
        self._ranks = list("A23456789") + ["10"] + list("JQK")
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


    def __str__(self):
        cards_str = '[' + ', '.join([card.__repr__() for card in self.cards]) + ']'
        return cards_str


    def pop(self):
        return self.cards.pop()


    def shuffle(self):
        shuffle(self.cards)



class Player:


    def __init__(self):
        self.cards = []


    def __str__(self):
        cards_str = '[' + ', '.join([card.__repr__() for card in self.cards]) + ']'
        return cards_str


    def init_draw(self, deck: Deck):
        self.cards.append(deck.pop())
        self.cards.append(deck.pop())


    def draw(self, deck: Deck):
        '''draw one card from deck to Player'''
        card = deck.pop()
        self.cards.append(card)
        return card


    def get_score(self):
        ranks = [card.rank for card in self.cards]
        value = sum([VALUE_DICT[rank] for rank in ranks])
        if value > 21 and 'A' in ranks:
            # print('A occurrences', ranks.count('A'))
            value -= 10

        return value   



class Dealer:


    def __init__(self):
        self.cards = []


    def __str__(self):
        cards_str = '[' + ', '.join([card.__repr__() for card in self.cards]) + ']'
        return cards_str
    
    
    def init_draw(self, deck: Deck):
        self.cards.append(deck.pop())
        self.cards.append(deck.pop())


    def draw(self, deck: Deck):
        # Dealer draw card until self.total_point >= 17
        while self.get_score() < 17:
            self.cards.append(deck.pop())
            print(self.cards)
            print(self.get_score())


    def get_score(self):
        ranks = [card.rank for card in self.cards]
        value = sum([VALUE_DICT[rank] for rank in ranks])
        if value > 21 and 'A' in ranks:
            print('A occurrences', ranks.count('A'))
            value -= 10

        return value

