import tkinter as tk
from tkinter import ttk, messagebox
from typing import Protocol



class Presenter(Protocol):
    def handle_hit(self, event: tk.Event) -> None:
        '''handle player hit event'''
        ...
    def handle_stand(self, event: tk.Event) -> None:
        '''handle player stand event'''
        ...
    def handle_double_down(self, event: tk.Event) -> None:
        '''handle player double down event'''
        ...
    def handle_surrender(self, event: tk.Event) -> None:
        '''handle player surrender event'''
        ...


class App(tk.Tk):
    def __init__(self, presenter: Presenter):
        super().__init__()

        # variables
        self.variables = {
            'dealer_score': tk.IntVar(),
            'player_score': tk.IntVar(),
        }


        # window configuration
        self.title('dude')

        # widgets creation
        self.frame_table = ttk.Frame(self, relief='solid', borderwidth=5, width=500, height=500)

        self.frame_dealer = ttk.Frame(self.frame_table, relief='solid', borderwidth=5, width=300, height=200)
        self.label_dealer = ttk.Label(self.frame_dealer, text='Dealer')
        self.listbox_dealer_cards = tk.Listbox(self.frame_dealer)
        self.label_dealer_score = ttk.Label(self.frame_dealer, textvariable=self.variables['dealer_score'])

        self.frame_options = ttk.Frame(self.frame_table, relief='solid', borderwidth=5, width=300, height=100)
        self.btn_hit = ttk.Button(self.frame_options, text='Hit', command=presenter.handle_hit)
        self.btn_double_down = ttk.Button(self.frame_options, text='Double Down', command=presenter.handle_double_down)
        self.btn_stand = ttk.Button(self.frame_options, text='Stand', command=presenter.handle_stand)
        self.btn_surrender = ttk.Button(self.frame_options, text='Surrender', command=presenter.handle_surrender)
        self.btn_new_round = ttk.Button(self.frame_options, text="Start New", command=presenter.init_game)

        self.frame_player = ttk.Frame(self.frame_table, relief='solid', borderwidth=5, width=300, height=200)
        self.label_player = ttk.Label(self.frame_player, text='Player')
        self.listbox_player_cards = tk.Listbox(self.frame_player)
        self.label_player_score = ttk.Label(self.frame_player, textvariable=self.variables['player_score'])

        self.frame_deck = ttk.Frame(self.frame_table, relief='solid', borderwidth=5, width=100, height=500)

        # grid layout
        self.frame_table.grid()

        self.frame_dealer.grid(row=0, column=0, rowspan=1, columnspan=1)
        self.label_dealer.grid()
        self.listbox_dealer_cards.grid()
        self.label_dealer_score.grid()

        self.frame_options.grid(row=1, column=0, rowspan=1, columnspan=1)
        self.btn_hit.grid(row=0, column=0)
        self.btn_double_down.grid(row=0, column=1)
        self.btn_stand.grid(row=0, column=2)
        self.btn_surrender.grid(row=0, column=3)
        self.btn_new_round.grid(row=0, column=4)

        self.frame_player.grid(row=2, column=0, rowspan=1, columnspan=1)
        self.label_player.grid()
        self.listbox_player_cards.grid()
        self.label_player_score.grid()

        self.frame_deck.grid(row=0, column=1, rowspan=3, columnspan=1)

        # event binding (if you disable a button, bind will still work... so you better use command instead of bind)
        # self.btn_hit.bind("<Button-1>", presenter.handle_hit)
        # self.btn_stand.bind("<Button-1>", presenter.handle_stand)
        # self.btn_double_down.bind("<Button-1>", presenter.handle_double_down)
        # self.btn_surrender.bind("<Button-1>", presenter.handle_surrender)


    def update_label_score(self, dealer_score: int, player_score: int) -> None:
        self.variables['dealer_score'].set(dealer_score)
        self.variables['player_score'].set(player_score)


    def update_listbox_cards(self, dealer_cards: list, player_cards: list) -> None:
        '''dealer_cards format: [Card('rank', 'suit'), ...]'''
        self.listbox_dealer_cards.delete(0, tk.END)
        self.listbox_player_cards.delete(0, tk.END)
        for dealer_card in dealer_cards:
            self.listbox_dealer_cards.insert(0, str(dealer_card))
        for player_card in player_cards:
            self.listbox_player_cards.insert(0, str(player_card))




    def messagebox_round_win(self, player_score, dealer_score):
        '''round end with draw, no one wins'''
        messagebox.showinfo('win', f'you win!\nplayer:{player_score} dealer:{dealer_score}')


    def messagebox_round_lose(self, player_score, dealer_score):
        '''player lose'''
        messagebox.showinfo('lose', f'lose all bet\nplayer:{player_score} dealer:{dealer_score}')


    def messagebox_round_draw(self, player_score, dealer_score):
        '''round end with draw, no one wins'''
        messagebox.showinfo('draw', f'no one wins!\nplayer:{player_score} dealer:{dealer_score}')


    def messagebox_round_blackjack(self, player_score, dealer_score):
        '''player blackjack, win the game'''
        messagebox.showinfo('blackjack!', f'you win\nplayer:{player_score} dealer:{dealer_score}')


    def messagebox_round_bust(self, player_score, dealer_score):
        '''player bust, lose the game'''
        messagebox.showinfo('bust!', f'you lose\nplayer:{player_score} dealer:{dealer_score}')


    def messagebox_round_dealer_bust(self, player_score, dealer_score):
        '''dealer bust, you win the game'''
        messagebox.showinfo('dealer bust!', f'you win!\nplayer:{player_score} dealer:{dealer_score}')


    def messagebox_round_surrender(self):
        messagebox.showinfo('surrender', 'player surrender, get half bet back.')


if __name__ == "__main__":
    app = App()
    app.mainloop()