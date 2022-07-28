import CardLib
from random import randint
import time


class ThirtyOne:
    DEAL_COUNT = 3
    PLAYER_COUNT = 5
    round_counter = 1

    def __init__(self):
        self.setup_decks()

    def setup_decks(self):
        self.stock = CardLib.Draw([])
        self.stock = CardLib.fill_deck_standard_52(self.stock)
        self.stock.shuffle()
        self.discard = CardLib.Discard([])
        self.discard.add_card(self.stock.pop_card())

    def draw_card(self, widow):
        return widow.hand.pop_card()

    def check_player_win(self, player):

        scores = self.calculate_suit_score(player)
        current_score = max(scores[1:5])
        score_index = scores.index(current_score)
        max_suit = CardLib.Card.suits[score_index]
        if current_score == 31:
            return True
        else:
            return False

    def on_round_won(self, player):
        player.round_winner()

        self.setup_decks()

    def on_card_played(self, card):
        self.discard.add_card(card)

    def get_AI_turn(self, player, widow):
        select_widow = randint(1, 3)
        drew_card = widow.hand.card_list[select_widow - 1]
        del widow.hand.card_list[select_widow - 1]
        player.add_card_to_hand(drew_card)
        select_card = randint(1, 3)

        place_card = player.hand.get_card_at(int(select_card) - 1)
        del player.hand.card_list[select_card - 1]
        widow.add_card_to_hand(place_card)

        return drew_card

    def calculate_suit_score(self, player):
        suit_scores = [None, 0, 0, 0, 0]
        for card in player.hand.card_list:
            if card.rank in ['J', 'Q', 'K']:
                value = 10
            elif card.rank == 'A':
                value = 11
            else:
                value = int(card.rank)

            if card.suit == '\u2666':
                suit_scores[1] += value
            elif card.suit == '\u2665':
                suit_scores[2] += value
            elif card.suit == '\u2663':
                suit_scores[3] += value
            elif card.suit == '\u2660':
                suit_scores[4] += value
        return suit_scores

    def get_user_turn(self, player, widow):

        print("┌────────────────────────────────────────────────┐")
        player_label = f" {player.label} - Round {self.round_counter} - Rounds Won: {player.win_count} "
        print(f"│{player_label:48}│")
        print("└────────────────────────────────────────────────┘")
        time.sleep(1)
        print(str(widow))
        time.sleep(1)
        print("--------------------------------------------------")

        played_valid = False
        while not played_valid:
            scores = self.calculate_suit_score(player)
            current_score = max(scores[1:5])
            score_index = scores.index(current_score)
            max_suit = CardLib.Card.suits[score_index]

            action, card_num = CardLib.get_user_input(["draw", "hint", "knock", "end"],
                                                      "Your Cards: " + str(player.hand) + f"\nCurrent Score: "
                                                                                          f"{current_score}{max_suit}")
            if action == "hint":
                print('Your current suit scores are:')
                if scores[1] != 0:
                    print(f'  \u2666: {scores[1]}')
                if scores[2] != 0:
                    print(f'  \u2665: {scores[2]}')
                if scores[3] != 0:
                    print(f'  \u2663: {scores[3]}')
                if scores[4] != 0:
                    print(f'  \u2660: {scores[4]}')

            if action == "draw":
                print(str(widow))
                widow_action, select_widow = CardLib.get_user_input(["1", "2", "3"],
                                                                    "Which card would you like from the widow?")
                select_widow = int(widow_action)
                drew_card = widow.hand.card_list[select_widow - 1]
                del widow.hand.card_list[select_widow - 1]

                print("Drew : ", drew_card)
                print("Your Cards: " + str(player.hand))

                select_action, select_card = CardLib.get_user_input(["1", "2", "3"],
                                                                    "Which card would you like to place "
                                                                    "back into the widow?")
                select_card = int(select_action)
                place_card = player.hand.get_card_at(select_card - 1)
                player.add_card_to_hand(drew_card)
                del player.hand.card_list[select_card - 1]
                widow.add_card_to_hand(place_card)

                return drew_card

            if action == "knock":
                return "knock"

            if action == "end":
                print("Thanks for playing!")
                exit()

    def on_player_turn(self, player, widow):
        if player.is_ai:
            played_card = self.get_AI_turn(player, widow)
        else:
            played_card = self.get_user_turn(player, widow)

        return played_card


def main_loop(game, player_list):
    playing = True
    while playing:
        for player in player_list:
            player.clear_hand()
        game.stock, player_list = CardLib.deal_to_players(game.stock, player_list, game.DEAL_COUNT)
        widow = player_list[4]
        widow.label = 'Widow Cards'
        del player_list[-1]

        current_player = 0
        terminal = -1

        playing_round = True

        while playing_round:
            time.sleep(0.5)
            if current_player != terminal:
                player = player_list[current_player]
                played_card = game.on_player_turn(player, widow)

                if played_card == 'knock':
                    terminal = current_player

                elif played_card is not None:
                    game.on_card_played(played_card)
                    print(player.label, "drew", played_card, "from the widow")
                    time.sleep(0.5)

                if game.check_player_win(player):
                    playing_round = False
                    print(player.label, "has won the hand with 31!")

                    game.on_round_won(player)
                    player_list.append(CardLib.Player("widow", is_ai=True))
                    for player in player_list:
                        player.clear_hand()

                else:
                    current_player = (current_player + 1) % 4
            else:
                player_scores = []
                print("--------------------------------------------------")
                for player in player_list:
                    print_str = f"{player.label}:"
                    for card in player.hand.card_list:
                        print_str += f" {str(card)}"
                    print(print_str, end=' - ')
                    scores = game.calculate_suit_score(player)
                    current_score = max(scores[1:5])
                    score_index = scores.index(current_score)
                    max_suit = CardLib.Card.suits[score_index]
                    player_scores.append(current_score)
                    print(f'Score: {current_score}{max_suit}')
                win_index = player_scores.index(max(player_scores))
                print("--------------------------------------------------")
                print(f"{player_list[win_index].label} won the hand with {player_scores[win_index]}!")
                game.on_round_won(player_list[win_index])
                time.sleep(3)
                game.round_counter += 1

                if player_list[win_index].win_count == 5:
                    print(f"{player_list[win_index].label} Won the game!")
                    print("They were the first to win 5 rounds!")
                    playing_round = False
                    playing = False
                else:
                    playing_round = False
                    player_list.append(CardLib.Player("widow", is_ai=True))

    action, _ = CardLib.get_user_input(["yes", "no"], "Do you want to play again?")

    if action in ["yes"]:
        player_list.append(CardLib.Player("widow", is_ai=True))
        game.round_counter = 1
        for player in player_list:
            player.win_count = 0
        game.playing = True
        game.playing_round = True
        main_loop(game, player_list)
    else:
        game.playing = False

        print("Thank you for playing!")


def start_game():
    game = ThirtyOne()
    print("  _______ _    _ _      _            ____              ")
    print(" |__   __| |  | (_)    | |          / __ \\             ")
    print("    | |  | |__| |_ _ __| |_ _   _  | |  | |_ __   ___  ")
    print("    | |  |  __  | | '__| __| | | | | |  | | '_ \\ / _ \\ ")
    print("    | |  | |  | | | |  | |_| |_| | | |__| | | | |  __/ ")
    print("    |_|  |_|  |_|_|_|   \\__|\\__, |  \\____/|_| |_|\\___| ")
    print("                             __/ |                     ")
    print("                            |___/                      ")
    print("Lets Play Thirty One!")
    player_list = [CardLib.Player("Player")]

    for num in range(1, game.PLAYER_COUNT):
        player_list.append(CardLib.Player("AI #" + str(num), is_ai=True))

    main_loop(game, player_list)
