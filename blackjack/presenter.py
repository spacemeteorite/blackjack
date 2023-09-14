from typing import Protocol


class View:
    def some_fun(self):
        ...


class Dealer:
    def some_func(self):
        ...


class Player:
    def some_func(self):
        ...

class Deck:
    def some_func(self):
        ...

class Presenter:


    def __init__(self, view: View, deck: Deck, player: Player, dealer: Dealer):
        self.view = view(self)
        self.deck = deck()
        self.deck.shuffle()
        print('deck initiated')
        self.player = player()
        print('player initiated')
        self.dealer = dealer()
        print('dealer initiated')


    def handle_hit(self, event=None) -> None:
        card = self.player.draw(self.deck)
        self.view.listbox_player_cards.insert(0, str(card))
        self.update_var_score()

    def handle_double_down(self, event=None) -> None:
        card_1 = self.player.draw(self.deck)
        card_2 = self.player.draw(self.deck)
        self.view.listbox_player_cards.insert(0, str(card_1))
        self.view.listbox_player_cards.insert(0, str(card_2))
        self.update_var_score()


    def handle_stand(self, event=None) -> None:
        pass


    def handle_surrender(self, event=None) -> None:
        pass


    def update_var_score(self) -> None:
        self.view.variables['dealer_score'].set(self.dealer.score())
        self.view.variables['player_score'].set(self.player.score())


    def run(self) -> None:
        self.view.mainloop()