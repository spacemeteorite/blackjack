from typing import Protocol
from .models import Deck, Player, Dealer, VALUE_DICT



class View(Protocol):
    def some_fun(self):
        ...



class Presenter:


    def __init__(self, view: View):
        self.view = view(self)
        self.view.disable_options()
        self.player_money = 10000 # give player 10000 at start
        self.view.variables['player_money'].set(self.player_money)


    def init_game(self):
        self.deck = Deck()
        self.deck.shuffle() # constant shuffle machine
        self.player = Player()
        self.dealer = Dealer()
        self.bet = 100 # initial bet money for a round

        # subtract money from player_money as bet
        self.change_player_money( - self.bet)

        # reset widgets
        self.view.btn_hit['state'] = 'enable'
        self.view.btn_double_down['state'] = 'enable'
        self.view.btn_stand['state'] = 'enable'
        self.view.btn_surrender['state'] = 'enable'

        # dealer and player each draw 2 cards
        self.dealer.init_draw(self.deck)
        self.player.init_draw(self.deck)
        self.view.init_listbox_dealer_cards(self.dealer.cards[0])

        self.view.update_listbox_player_cards(self.player.cards)
        self.view.update_label_player_score(self.player.get_score())

        self.view.update_label_dealer_score(VALUE_DICT[self.dealer.cards[0].rank]) # only show value of dealer's first card


        # check if player blackjack at start
        if self.player.get_score() == 21:
            self.view.messagebox_round_blackjack(self.player.get_score(), self.dealer.get_score())
            self.change_player_money(2*self.bet)

    def handle_hit(self, event=None) -> None:
        self.player.draw(self.deck)
        self.view.update_listbox_player_cards(self.player.cards)
        self.view.update_label_player_score(self.player.get_score())


        self.view.btn_double_down['state'] = 'disabled'
        # self.view.btn_surrender['state'] = 'disabled'

        player_score = self.player.get_score()
        if player_score > 21:
            self.view.messagebox_round_bust(self.player.get_score(), self.dealer.get_score())
            self.view.disable_options()
            self.view.update_listbox_cards(self.dealer.cards, self.player.cards)
            self.view.update_label_score(self.dealer.get_score(), self.player.get_score())
        elif player_score == 21:
            self.view.messagebox_round_blackjack(self.player.get_score(), self.dealer.get_score())
            self.view.disable_options()
            self.view.update_listbox_cards(self.dealer.cards, self.player.cards)
            self.view.update_label_score(self.dealer.get_score(), self.player.get_score())
            self.change_player_money(2 * self.bet)
        elif player_score < 21:
            pass
         
        
    def handle_double_down(self, event=None) -> None:
        self.player.draw(self.deck)
        self.player.draw(self.deck)
        self.view.update_listbox_player_cards(self.player.cards)
        self.view.update_listbox_dealer_cards(self.dealer.cards)
        self.view.update_label_score(self.dealer.get_score(), self.player.get_score())
        self.view.disable_options()

        self.change_player_money( - self.bet) # you need to add another bet for double down

        # player logic
        if self.player.get_score() > 21:
            self.view.messagebox_round_bust(self.player.get_score(), self.dealer.get_score())
        elif self.player.get_score() == 21:
            self.view.messagebox_round_blackjack(self.player.get_score(), self.dealer.get_score())
            self.change_player_money(4 * self.bet)
        elif self.player.get_score() < 21:
            self.dealer_logic()


    def handle_stand(self, event=None) -> None:
        self.view.disable_options()
        # dealer logic
        self.dealer_logic()


    def handle_surrender(self, event=None) -> None:
        self.view.disable_options()
        self.change_player_money(round(self.bet / 2)) # get half bet back if surrender
        self.view.messagebox_round_surrender()


    def dealer_logic(self, flag_double_down = False) -> None:
        '''after all drawing completed, this is the final score checker'''
        self.dealer.draw(self.deck)
        self.view.update_listbox_cards(self.dealer.cards, self.player.cards)
        if self.dealer.get_score() > 21:
            self.view.messagebox_round_dealer_bust(self.player.get_score(), self.dealer.get_score())
        elif self.dealer.get_score() <= 21:
            player_score = self.player.get_score()
            dealer_score = self.dealer.get_score()
            self.view.update_label_score(dealer_score=dealer_score, player_score=player_score)

            if player_score == dealer_score:
                self.view.messagebox_round_draw(self.player.get_score(), self.dealer.get_score())
                self.change_player_money(2 * self.bet) if flag_double_down else self.change_player_money(self.bet) # get bet back if draw
            elif player_score > dealer_score:
                self.view.messagebox_round_win(self.player.get_score(), self.dealer.get_score())
                self.change_player_money(4 * self.bet) if flag_double_down else self.change_player_money(2 * self.bet) # win double bet if double down, or win one bet if not double down.
            elif player_score < dealer_score:
                self.view.messagebox_round_lose(self.player.get_score(), self.dealer.get_score())


    def change_player_money(self, money_change: int) -> None:
        self.player_money += money_change
        self.view.variables['player_money'].set(self.player_money)


    def run(self) -> None:
        self.view.mainloop()