from typing import Protocol
from .models import Deck, Player, Dealer



class View(Protocol):
    def some_fun(self):
        ...



class Presenter:


    def __init__(self, view: View):
        self.view = view(self)


    def init_game(self):
        self.deck = Deck()
        self.deck.shuffle()
        print('deck initiated')
        self.player = Player()
        print('player initiated')
        self.dealer = Dealer()
        print('dealer initiated')

        # reset widgets
        self.view.btn_hit['state'] = 'enable'
        self.view.btn_double_down['state'] = 'enable'
        self.view.btn_stand['state'] = 'enable'
        self.view.btn_surrender['state'] = 'enable'
        self.view.listbox_player_cards.delete(0, -1)
        self.view.listbox_dealer_cards.delete(0, -1)

        # dealer and player each draw 2 cards
        self.dealer.init_draw(self.deck)
        self.player.init_draw(self.deck)
        self.view.update_listbox_cards(self.dealer.cards, self.player.cards)
        self.view.update_label_score(self.dealer.get_score(), self.player.get_score())

        # check if player blackjack at start
        if self.player.get_score() == 21:
            self.view.messagebox_round_blackjack(self.player.get_score(), self.dealer.get_score())


    def handle_hit(self, event=None) -> None:
        self.player.draw(self.deck)
        self.view.update_listbox_cards(self.dealer.cards, self.player.cards)
        self.view.update_label_score(self.dealer.get_score(), self.player.get_score())

        self.view.btn_double_down['state'] = 'disabled'
        self.view.btn_surrender['state'] = 'disabled'

        player_score = self.player.get_score()
        if player_score > 21:
            self.view.messagebox_round_bust(self.player.get_score(), self.dealer.get_score())
            self.view.btn_hit['state'] = 'disabled'
            self.view.btn_double_down['state'] = 'disabled'
            self.view.btn_stand['state'] = 'disabled'
            self.view.btn_surrender['state'] = 'disabled'
        elif player_score == 21:
            self.view.messagebox_round_blackjack(self.player.get_score(), self.dealer.get_score())
            self.view.btn_hit['state'] = 'disabled'
            self.view.btn_double_down['state'] = 'disabled'
            self.view.btn_stand['state'] = 'disabled'
            self.view.btn_surrender['state'] = 'disabled'
        elif player_score < 21:
            pass
         
        
    def handle_double_down(self, event=None) -> None:
        self.player.draw(self.deck)
        self.player.draw(self.deck)
        self.view.update_listbox_cards(self.dealer.cards, self.player.cards)
        self.view.update_label_score(self.dealer.get_score(), self.player.get_score())

        self.view.btn_hit['state'] = 'disabled'
        self.view.btn_double_down['state'] = 'disabled'
        self.view.btn_stand['state'] = 'disabled'
        self.view.btn_surrender['state'] = 'disabled'

        # player logic
        if self.player.get_score() > 21:
            self.view.messagebox_round_bust(self.player.get_score(), self.dealer.get_score())
        elif self.player.get_score() == 21:
            self.view.messagebox_round_blackjack(self.player.get_score(), self.dealer.get_score())
        elif self.player.get_score() < 21:
            # dealer logic
            self.dealer.draw(self.deck)
            self.view.update_listbox_cards(self.dealer.cards, self.player.cards)
            if self.dealer.get_score() > 21:
                self.view.messagebox_round_dealer_bust(self.player.get_score(), self.dealer.get_score())
            elif self.dealer.get_score() <= 21:
                self.score_checker_end()


    def handle_stand(self, event=None) -> None:
        self.view.btn_hit['state'] = 'disabled'
        self.view.btn_double_down['state'] = 'disabled'
        self.view.btn_stand['state'] = 'disabled'
        self.view.btn_surrender['state'] = 'disabled'

        # dealer logic
        self.dealer.draw(self.deck)
        self.view.update_listbox_cards(self.dealer.cards, self.player.cards)

        if self.dealer.get_score() > 21:
            self.view.messagebox_round_dealer_bust(self.player.get_score(), self.dealer.get_score())
        elif self.dealer.get_score() <= 21:
            self.score_checker_end()


    def handle_surrender(self, event=None) -> None:
        self.view.btn_hit['state'] = 'disabled'
        self.view.btn_double_down['state'] = 'disabled'
        self.view.btn_stand['state'] = 'disabled'
        self.view.btn_surrender['state'] = 'disabled'

        self.view.messagebox_round_surrender()


    def score_checker_end(self) -> None:
        '''after all drawing completed, this is the final score checker'''
        player_score = self.player.get_score()
        dealer_score = self.dealer.get_score()
        self.view.update_label_score(dealer_score=dealer_score, player_score=player_score)

        if player_score == dealer_score:
            self.view.messagebox_round_draw(self.player.get_score(), self.dealer.get_score())
        elif player_score > dealer_score:
            self.view.messagebox_round_win(self.player.get_score(), self.dealer.get_score())
        elif player_score < dealer_score:
            self.view.messagebox_round_lose(self.player.get_score(), self.dealer.get_score())


    def run(self) -> None:
        self.view.mainloop()