from blackjack.models import Deck, Player, Dealer
from blackjack.view import App
from blackjack.presenter import Presenter



mypresenter = Presenter(App)
mypresenter.run()