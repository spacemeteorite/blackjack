import tkinter as tk
from tkinter import ttk, messagebox
from typing import Protocol
from .widgets import LabeledInfo


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
            'player_money': tk.IntVar(),
            'current_bet': tk.IntVar(),
            'potential_bonus': tk.IntVar(),
        }


        # window configuration
        self.title('blackjack')
        self.resizable(width=True, height=False)

        # widgets creation
        self.frame_table = ttk.LabelFrame(self, text='TABLE', relief='solid', borderwidth=5)

        self.frame_dealer = ttk.Frame(self.frame_table, relief='solid', borderwidth=5)
        self.label_dealer = ttk.Label(self.frame_dealer, text='Dealer')
        self.listbox_dealer_cards = tk.Listbox(self.frame_dealer)
        self.label_dealer_score = LabeledInfo(self.frame_dealer, label_text='Dealer Score: ', textvariable=self.variables['dealer_score'])

        self.frame_options = ttk.Frame(self.frame_table, relief='solid', borderwidth=5)
        self.btn_hit = ttk.Button(self.frame_options, text='Hit', command=presenter.handle_hit)
        self.btn_double_down = ttk.Button(self.frame_options, text='Double Down', command=presenter.handle_double_down)
        self.btn_stand = ttk.Button(self.frame_options, text='Stand', command=presenter.handle_stand)
        self.btn_surrender = ttk.Button(self.frame_options, text='Surrender', command=presenter.handle_surrender)
        self.btn_new_round = ttk.Button(self.frame_options, text="Start New", command=presenter.init_game)

        self.frame_player = ttk.Frame(self.frame_table, relief='solid', borderwidth=5)
        self.label_player = ttk.Label(self.frame_player, text='Player')
        self.listbox_player_cards = tk.Listbox(self.frame_player)
        self.label_player_score = LabeledInfo(self.frame_player, label_text='Player Score: ', textvariable=self.variables['player_score'])


        self.frame_info = ttk.LabelFrame(self, text='INFO', relief='solid', borderwidth=5)
        self.label_player_money = LabeledInfo(self.frame_info, label_text='money: ', textvariable=self.variables['player_money'])
        self.label_current_bet = LabeledInfo(self.frame_info, label_text='current bet: ', textvariable=self.variables['current_bet'])
        self.label_potential_bonus = LabeledInfo(self.frame_info, label_text='potential bonus: ', textvariable=self.variables['potential_bonus'])
        self.tutorial_str = """
100$ for one bet, surrender 
to get 50$ back, double down 
you need another 100$ bet,
but win twice back.
"""
        self.label_tutorial = ttk.Label(self.frame_info, text=self.tutorial_str)

        # grid column configure
        self.columnconfigure(0, weight=1)
        self.frame_table.columnconfigure(0, weight=1)
        self.frame_dealer.columnconfigure(0, weight=1)
        self.frame_player.columnconfigure(0, weight=1)
        for i in range(5):
            self.frame_options.columnconfigure(i, weight=1)

        # grid layout
        self.frame_table.grid(sticky='wnes')

        self.frame_dealer.grid(row=0, sticky='wnes')
        self.label_dealer.grid()
        self.listbox_dealer_cards.grid(sticky='we', padx=20)
        self.label_dealer_score.grid()

        self.frame_options.grid(row=1, sticky='wnes')
        self.btn_hit.grid(row=0, column=0)
        self.btn_double_down.grid(row=0, column=1)
        self.btn_stand.grid(row=0, column=2)
        self.btn_surrender.grid(row=0, column=3)
        self.btn_new_round.grid(row=0, column=4)

        self.frame_player.grid(row=2, sticky='wnes')
        self.label_player.grid()
        self.listbox_player_cards.grid(sticky='we', padx=20)
        self.label_player_score.grid()

        self.frame_info.grid(row=0, column=1,sticky='wnes')
        self.label_player_money.grid(row=0, pady=10)
        self.label_current_bet.grid(row=1, pady=10)
        self.label_potential_bonus.grid(row=2, pady=10)
        self.label_tutorial.grid(row=3)

        # event binding (if you disable a button, bind will still work... so you better use command instead of bind)
        # self.btn_hit.bind("<Button-1>", presenter.handle_hit)
        # self.btn_stand.bind("<Button-1>", presenter.handle_stand)
        # self.btn_double_down.bind("<Button-1>", presenter.handle_double_down)
        # self.btn_surrender.bind("<Button-1>", presenter.handle_surrender)


    def init_listbox_dealer_cards(self, faceup_card):
        '''
        faceup_card = Card('rank', 'suit')
        according to blackjack rule, the first card of dealer is face up,
        and the second card of dealer is face down. 
        '''

        self.listbox_dealer_cards.delete(0, tk.END)
        self.listbox_dealer_cards.insert(0, str(faceup_card))
        self.listbox_dealer_cards.insert(0, '<face-down-card>')


    def disable_options(self):
        '''
        disable all options except "new_round"
        '''
        self.btn_hit['state'] = 'disabled'
        self.btn_double_down['state'] = 'disabled'
        self.btn_stand['state'] = 'disabled'
        self.btn_surrender['state'] = 'disabled'


    def update_label_score(self, dealer_score: int, player_score: int) -> None:
        self.variables['dealer_score'].set(dealer_score)
        self.variables['player_score'].set(player_score)


    def update_label_dealer_score(self, dealer_score: int) -> None:
        self.variables['dealer_score'].set(dealer_score)


    def update_label_player_score(self, player_score: int) -> None:
        self.variables['player_score'].set(player_score)


    def update_listbox_cards(self, dealer_cards: list, player_cards: list) -> None:
        '''dealer_cards format: [Card('rank', 'suit'), ...]'''
        self.listbox_dealer_cards.delete(0, tk.END)
        self.listbox_player_cards.delete(0, tk.END)
        for dealer_card in dealer_cards:
            self.listbox_dealer_cards.insert(0, str(dealer_card))
        for player_card in player_cards:
            self.listbox_player_cards.insert(0, str(player_card))


    def update_listbox_player_cards(self, player_cards: list) -> None:
        '''player_cards: [Card('rank', 'suit') ,...]'''
        self.listbox_player_cards.delete(0, tk.END)
        for player_card in player_cards:
            self.listbox_player_cards.insert(0, str(player_card))


    def update_listbox_dealer_cards(self, dealer_cards: list) -> None:
        '''dealer_cards: [Card('rank', 'suit') ,...]'''
        self.listbox_dealer_cards.delete(0, tk.END)
        for dealer_card in dealer_cards:
            self.listbox_dealer_cards.insert(0, str(dealer_card))


    def messagebox_round_end(self, result: str, dealer_score, player_score, total_bet=0, money_change=0):
        info_str = f"""
-- <{result}> --
dealer: {dealer_score}
player: {player_score}
total bet: {total_bet}
money change: {money_change}
"""
        messagebox.showinfo('result', info_str)


if __name__ == "__main__":
    app = App()
    app.mainloop()