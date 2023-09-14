import tkinter as tk
from tkinter import ttk
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
        self.btn_hit = ttk.Button(self.frame_options, text='Hit')
        self.btn_double_down = ttk.Button(self.frame_options, text='Double Down')
        self.btn_stand = ttk.Button(self.frame_options, text='Stand')
        self.btn_surrender = ttk.Button(self.frame_options, text='Surrender')

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

        self.frame_player.grid(row=2, column=0, rowspan=1, columnspan=1)
        self.label_player.grid()
        self.listbox_player_cards.grid()
        self.label_player_score.grid()

        self.frame_deck.grid(row=0, column=1, rowspan=3, columnspan=1)

        # event binding
        self.btn_hit.bind("<Button-1>", presenter.handle_hit)
        self.btn_stand.bind("<Button-1>", presenter.handle_stand)
        self.btn_double_down.bind("<Button-1>", presenter.handle_double_down)
        self.btn_surrender.bind("<Button-1>", presenter.handle_surrender)


if __name__ == "__main__":
    app = App()
    app.mainloop()