import CardLib
from random import randint

DEAL_COUNT = 3
PLAYER_COUNT = 4


class ThirtyOne:
    DEAL_COUNT = 3
    PLAYER_COUNT = 4

    def __init__(self):
        self.setup_decks()

    def setup_decks(self):
        self.stock = CardLib.Draw([])
        self.stock = CardLib.fill_deck_standard_52(self.stock)
        self.stock.shuffle()

        self.discard = CardLib.Discard([])
        self.discard.add_card(self.stock.pop_card())


def main_loop(game, player_list):
    playing = True
    while playing:
        print("What would you like to do?")


def start_game():
    CardLib.print_test()
    game = ThirtyOne()
    print("Lets Play Crazy 8's!")

    player_list = [CardLib.Player("Player")]

    for num in range(1, game.PLAYER_COUNT):
        player_list.append(CardLib.Player("AI #" +str(num), is_ai=True))

    main_loop(game, player_list)