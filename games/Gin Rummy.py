import CardLib

class GinRummy():
    PLAYER_COUNT = 4
    DEAL_COUNT = 7
    deck = CardLib.CardList()

    def __init__(self):
        CardLib.fill_deck_standard_52(self.deck)