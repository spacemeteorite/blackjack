from typing import Protocol
from .models import Deck, Player, Dealer, VALUE_DICT
from .view import App



class Presenter:


    def __init__(self, view: App):
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
        self.flag_double_down = False # flag for double down checking at end

        # subtract money from player_money as bet
        self.player_money -= self.bet
        self.update_screen()

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
            self.view.disable_options()
            self.player_win('blackjack') # game end with blackjack


    def handle_hit(self, event=None) -> None:
        self.player.draw(self.deck)
        self.view.update_listbox_player_cards(self.player.cards)
        self.view.update_label_player_score(self.player.get_score())


        self.view.btn_double_down['state'] = 'disabled'
        # self.view.btn_surrender['state'] = 'disabled'

        self.player_hit_logic() 
        

    def handle_double_down(self, event=None) -> None:
        self.flag_double_down = True
        self.player.draw(self.deck)
        self.view.update_listbox_player_cards(self.player.cards)
        self.view.update_listbox_dealer_cards(self.dealer.cards)
        self.view.update_label_score(self.dealer.get_score(), self.player.get_score())
        self.view.disable_options()

        self.player_money -= self.bet # you need to add another bet for double down
        self.bet *= 2
        self.update_screen()

        self.player_double_down_logic()


    def handle_stand(self, event=None) -> None:
        self.view.disable_options()
        # dealer logic
        self.dealer_logic()


    def handle_surrender(self, event=None) -> None:
        self.view.disable_options()
        self.update_screen()
        self.player_surrender()


    def player_hit_logic(self) -> None:
        # player hit logic
        player_score = self.player.get_score()

        if player_score > 21:
            self.view.disable_options()
            self.player_lose('bust')
        elif player_score == 21:
            self.view.disable_options()
            self.player_win('blackjack')
        elif player_score < 21:
            pass


    def player_double_down_logic(self) -> None:
        # player logic
        player_score = self.player.get_score()
        if player_score > 21:
            self.player_lose('bust')
        elif player_score == 21:
            self.player_win('blackjack')
        elif player_score < 21:
            self.dealer_logic()


    def dealer_logic(self) -> None:
        '''after all drawing completed, this is the final score checker'''
        self.dealer.draw(self.deck)

        player_score = self.player.get_score()
        dealer_score = self.dealer.get_score()
        self.view.update_listbox_cards(self.dealer.cards, self.player.cards)
        self.view.update_label_score(dealer_score=dealer_score, player_score=player_score)

        if dealer_score > 21:
            self.player_win('dealer bust')
        elif dealer_score == 21:
            self.player_lose('dealer blackjack')
        elif dealer_score < 21:
            if player_score == dealer_score:
                self.player_draw('player score = dealer score')
            elif player_score > dealer_score:
                self.player_win('player score > dealer score')
            elif player_score < dealer_score:
                self.player_lose('player score < dealer score')

        self.update_screen()


    def player_surrender(self, result='surrender') -> None:
        self.player_money += round(self.bet / 2)
        self.update_screen()
        self.view.messagebox_round_end(result, 
                                       self.dealer.get_score(), 
                                       self.player.get_score(),
                                       self.bet,
                                       -round(self.bet/2))


    def player_win(self, result='win') -> None:
        self.player_money += 2*self.bet
        self.update_screen()
        self.view.messagebox_round_end(result, 
                                       self.dealer.get_score(), 
                                       self.player.get_score(),
                                       self.bet,
                                       self.bet)


    def player_draw(self, result='draw') -> None:
        self.player_money += self.bet
        self.update_screen()
        self.view.messagebox_round_end(result, 
                                       self.dealer.get_score(), 
                                       self.player.get_score(),
                                       self.bet,
                                       0)


    def player_lose(self, result='lose') -> None:
        self.update_screen()
        self.view.messagebox_round_end(result, 
                                       self.dealer.get_score(), 
                                       self.player.get_score(),
                                       self.bet,
                                       -self.bet)


    def update_screen(self) -> None:
        self.view.variables['player_money'].set(self.player_money)
        self.view.variables['current_bet'].set(self.bet)
        self.view.variables['potential_bonus'].set(self.bet * 2)
        self.view.update_listbox_cards(self.dealer.cards, self.player.cards)
        self.view.update_label_score(self.dealer.get_score(), self.player.get_score())


    def run(self) -> None:
        self.view.mainloop()