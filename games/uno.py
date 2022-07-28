import CardLib
from random import randint


class UnoCard(CardLib.Card):
    colors = ["Red", "Yellow", "Green", "Blue", "Black"]

    def __init__(self, color, value, has_action=False, action=None):
        self.color = self.colors[color]
        self.value = value
        self.has_action = has_action
        self.action = action

    def change_color(self, new_color):
        self.color = new_color

    def __str__(self):
        if self.color == "Black":
            return "[" + self.action + "]"
        else:
            return "[" + self.color[0:1] + str(self.value) + "]"

    def __eq__(self, other):
        if isinstance(other, UnoCard):
            return self.color == other.color and self.value == other.value
        return False


class Uno:
    DEAL_COUNT = 7
    PLAYER_COUNT = 4

    direction = 1

    def __init__(self):
        self.setup_decks()

    def setup_decks(self):
        self.stock = CardLib.Draw([])
        self.stock = self.setup_uno_deck(self.stock)
        self.stock.shuffle()

        self.discard = CardLib.Discard([])
        self.discard.add_card(self.stock.pop_card())
        while self.discard.get_top_card().has_action:
            self.stock.add_card(self.discard.get_top_card())
            self.discard.rem_all_cards()
            self.stock.shuffle()
            self.discard.add_card(self.stock.pop_card())

    def setup_uno_deck(self, draw_pile):
        # color cards
        for color in range(4):
            draw_pile.add_card(UnoCard(color, 0))  # zeros
            for time in range(2):
                for value in range(1, 10):
                    draw_pile.add_card(UnoCard(color, value))  # num cards

                # action cards
                draw_pile.add_card(UnoCard(color, "+2", has_action=True, action="+2"))
                draw_pile.add_card(UnoCard(color, "rev", has_action=True, action="rev"))
                draw_pile.add_card(UnoCard(color, "skp", has_action=True, action="skp"))

        # black cards
        for val in range(8):
            if val % 2:
                draw_pile.add_card(UnoCard(4, "wld", has_action=True, action="wld"))
            else:
                draw_pile.add_card(UnoCard(4, "+4", has_action=True, action="+4"))
        return draw_pile

    def draw_card(self):
        if len(self.stock) == 0:
            top_card = self.discard.get_top_card()
            self.discard.shuffle()
            self.stock.add_cards(self.discard.get_card_list())

            self.discard.rem_all_cards()
            self.discard.add_card(top_card)

        return self.stock.pop_card()

    def is_card_valid(self, card):
        if card.color == "Black":
            return True

        top_card = self.discard.get_top_card()

        if card.color == top_card.color:
            return True
        if card.value == top_card.value:
            return True

        return False

    def check_player_win(self, player):
        return player.get_amount_of_cards() == 0

    def on_round_won(self, player):
        player.round_winner()

        self.setup_decks()
        self.direction = 1

    def on_card_played(self, card, player):
        skipped = False
        cards_to_add = 0

        if card.has_action:
            if card.action in ["skp", "+2", "+4"]:
                skipped = True
            if card.action == "+2":
                cards_to_add = 2
            if card.action == "+4":
                cards_to_add = 4

            if card.action == "rev":
                self.direction *= -1

            if card.color == "Black":
                if player.is_ai:
                    new_color = card.colors[randint(0, 3)]
                else:
                    new_color, _ = CardLib.get_user_input(card.colors[:-1], "Pick the new color")

                card.change_color(new_color)

        self.discard.add_card(card)
        return (skipped, cards_to_add)

    def get_valid_cards(self, player):
        return player.hand.get_all_valid_cards(self.is_card_valid)

    def get_ai_turn(self, player):
        valid_cards = self.get_valid_cards(player)
        if len(valid_cards) == 0:
            drew_card = self.draw_card()
            player.add_card_to_hand(drew_card)

            if not self.is_card_valid(drew_card):
                return None

            valid_cards = self.get_valid_cards(player)

        card_num = randint(0, len(valid_cards) - 1)
        card_to_play = valid_cards.get_card_at(card_num)

        player.hand.rem_card(card_to_play)

        return card_to_play

    def get_user_turn(self, player):
        valid_cards = self.get_valid_cards(player)
        print("--------------------")
        print("The last discard was: ", self.discard.get_top_card())

        played_valid = False
        while not played_valid:
            action, card_num = CardLib.get_user_input(["play", "hint", "draw", "exit"],
                                                      "Your Cards: " + str(player.hand))

            if action == "play":
                possible_card_nums = [str(num) for num in range(1, len(player.hand) + 1)]

                if card_num is None or card_num not in possible_card_nums:
                    card_num, _ = CardLib.get_user_input(possible_card_nums, "Pick a card num to play")

                picked_card = player.hand.get_card_at(int(card_num) - 1)

                if valid_cards.contains(picked_card):
                    player.hand.rem_card(picked_card)
                    played_valid = True
                    return picked_card
                else:
                    print("That card doesn't follow the game rules!")

            if action == "hint":
                if len(valid_cards) > 0:
                    print("Hint: you can play these: ", str(valid_cards))
                else:
                    print("Hint: you need to draw")

            if action == "draw":
                drew_card = self.draw_card()
                print("You drew a ", str(drew_card))

                if self.is_card_valid(drew_card):
                    action, _ = CardLib.get_user_input(["play", "keep"], "Do you want to play or keep this card?")

                    if action == "play":
                        played_valid = True
                        return drew_card

                player.add_card_to_hand(drew_card)
                played_valid = True
                return None

            if action == "exit":
                print("Thanks for playing!")
                exit()

    def on_player_turn(self, player):
        if player.is_ai:
            played_card = self.get_ai_turn(player)
        else:
            played_card = self.get_user_turn(player)

        return played_card


def main_loop(game, player_list):
    playing = True
    while playing:
        game.stock, player_list = CardLib.deal_to_players(game.stock, player_list, game.DEAL_COUNT)

        current_player = 0

        playing_round = True

        while playing_round:
            player = player_list[current_player]
            skipped = False
            cards_to_add = 0

            played_card = game.on_player_turn(player)

            if played_card is not None:
                print(player.label, "played: ", played_card)
                skipped, cards_to_add = game.on_card_played(played_card, player)
                if player.get_amount_of_cards() == 1:
                    print(player.label, ": UNO!")
            else:
                print(player.label, ": drew!")

            if game.check_player_win(player):
                playing_round = False
                print(player.label, "has won!")

                game.on_round_won(player)
                for player in player_list:
                    player.clear_hand()

            else:
                current_player = (current_player + game.direction) % 4

                player = player_list[current_player]
                if cards_to_add > 0:
                    has_s = " card!" if cards_to_add == 1 else " cards!"
                    print(player.label, ": had to pick up ", str(cards_to_add), has_s)
                    for _ in range(cards_to_add):
                        player.add_card_to_hand(game.draw_card())
                    current_player = (current_player + game.direction) % 4
                elif skipped:
                    print(player.label, ": got skipped!")
                    current_player = (current_player + game.direction) % 4

        action, _ = CardLib.get_user_input(["yes", "no"], "Do you want to play again?")

        if action is "no":
            playing = False

    print("Thank you for playing!")


def start_game():
    CardLib.print_test()

    game = Uno()
    print("Lets Play Uno!")

    player_list = [CardLib.Player("Player")]

    for num in range(1, game.PLAYER_COUNT):
        player_list.append(CardLib.Player("AI #" + str(num), is_ai=True))

    main_loop(game, player_list)
