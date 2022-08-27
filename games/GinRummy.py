import time
import sys, os
import numpy as np
from tqdm import tqdm
import CardLib as cl


class GinRummy():
    DEAL_COUNT = 7

    def __init__(self, player_number=1, players=4):
        self.play_options = {'help': self.exit_program, 'take card': self.pick_up_card, 'exit': self.exit_program,
                             'skip': self.skip_turn, 'draw': self.draw_card}
        self.player_list = []
        self.deck = cl.fill_deck_standard_52(cl.Draw())
        self.deck.shuffle()

        for x in range(1, player_number + 1):
            self.player_list.append(cl.Player(f"Player{x}"))
        for x in range(1, players - player_number + 1):
            self.player_list.append(cl.Player(f"AI{x}", True))

        cl.deal_to_players(self.deck, self.player_list, self.DEAL_COUNT)
        self.shown_card = self.deck.card_list.pop()

    # Functions called directly by player input

    @staticmethod
    def exit_program(player=None):
        exit()

    def rules(self, player=None):
        print("\nWelcome to Gin Rummy!")
        print(
            "The rules are simple, you have 7 cards and all of them have to be used in either a grouping of same "
            "rank, or in a straight of the same suit")
        print(
            "You must have at least 3 Cards in each grouping, the typical winning hand will have some combination of:")
        print("Three of one rank, four of one rank, three in a straight, or four in a straight")
        print(
            "Cards can only be used in one grouping, and it is possible to have a 7 card straight (but very unlikely)")
        print(
            "An example winning hand would be: 1) [J\u2666], 2) [Q\u2666], 3) [K\u2666], 4) [3\u2666], 5) [3\u2665], "
            "6) [3\u2663], 7) [3\u2660] \n")

        if player is not None:
            self.player_turn(player)

    def skip_turn(self, player):
        return

    def draw_card(self, player):
        player.add_card_to_hand(self.deck.pop_card())
        print(player)
        print("Choose a card to remove:")
        player_in = int(input(">>"))
        self.remove_card(player, player_in)

    def remove_card(self, player, player_in):
        if player_in in range(1, player.get_amount_of_cards() + 1):
            self.shown_card = player.play_card(player_in - 1)
            print(f"Your new hand:\n{self.sort_hand(player)}\n")
        else:
            print("That was not a valid option, try again!")
            return self.remove_card(player)

    def pick_up_card(self, player):
        picked_up_card = self.shown_card
        player.add_card_to_hand(picked_up_card)

        print(player)
        print("Choose a card to remove:")
        player_in = int(input(">>"))
        self.remove_card(player, player_in)

    # Helper functions

    @staticmethod
    def sort_hand(player):
        player.hand.sort_by_suit()
        player.hand.card_list.reverse()
        return player

    def get_choice(self, header, options):
        print(header)
        print([str(option) for option in options])
        player_in = input(">>")
        if player_in in options:
            return player_in
        print("That was not a valid option, try again!")
        return self.get_choice(header, options)

    def reshuffle_deck(self):
        self.deck = cl.fill_deck_standard_52(cl.Draw())
        for user in self.player_list:
            self.deck.card_list = [card for card in self.deck.card_list if card not in user.hand.card_list]
        self.deck.shuffle()
        self.shown_card = self.deck.card_list.pop()
        print("Reshuffled a new deck!")

    def ai_turn(self, player):
        matrix = CardMatrix(player.hand.card_list)

        hand_values = matrix.assign_hand_values()

        matrix.assign_deck_values()
        shown_val = matrix.deck_matrix[self.shown_card.suit_val - 1][self.shown_card.value - 1]

        if min(hand_values) < shown_val:
            # if the shown card is better than what is in hand
            picked_up_card = self.shown_card
            player.add_card_to_hand(picked_up_card)

            # remove lowest card in hand and update shown card
            new_shown_card = player.play_card(hand_values.index(min(hand_values)))
            self.shown_card = new_shown_card
            print(f"{player.label} picked up {picked_up_card} and put down {new_shown_card}")
            del matrix
        else:
            # draw card
            drawn_card = self.deck.pop_card()
            player.add_card_to_hand(drawn_card)

            # gets hand values of new hand
            hand_matrix = CardMatrix(player.hand.card_list)
            temp_hand_values = hand_matrix.assign_hand_values()
            del hand_matrix

            # removes lowest value card
            new_shown_card = player.play_card(temp_hand_values.index(min(temp_hand_values)))
            self.shown_card = new_shown_card
            print(f"{player.label} drew {drawn_card} and put down {new_shown_card}")

    # Called directly by main loop

    def player_turn(self, player, simulate=False):
        if not self.deck.card_list:
            self.reshuffle_deck()

        if not player.is_ai:
            time.sleep(1)
            print(f"\n{player.label}'s turn:")
            time.sleep(1)
            print(f"\nDeck: {self.shown_card}")
            time.sleep(1)
            player_input = self.get_choice(f"\n{self.sort_hand(player)}", self.play_options)
            self.play_options[player_input](player)
        else:
            if simulate == False:
                time.sleep(1)
            self.ai_turn(player)

    @staticmethod
    def check_win(player):
        matrix = CardMatrix(player.hand.card_list)
        return matrix.check_win()


class CardMatrix:

    def __init__(self, card_list):
        self.cards = card_list
        self.deck_matrix = np.array([
            #    A  2  3  4  5  6  7  8  9  10 J  Q  K
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Diamonds
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Hearts
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Clubs
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Spades
        ])
        for card in self.cards:
            self.deck_matrix[card.suit_val - 1][card.value - 1] = -1

    def assign_deck_values(self):
        for card in self.cards:
            for num in (-2, -1, 0, 2, 3, 4):
                if self.deck_matrix[card.suit_val - 1][(card.value - num) % 13] != -1:
                    self.deck_matrix[card.suit_val - 1][(card.value - num) % 13] += 2

        # rank matches
        for rank in range(13):

            column = self.deck_matrix[:, rank]
            num_cards = len([num for num in column if num == -1])

            for suit in range(4):
                if self.deck_matrix[suit][rank] != -1:

                    # add less if its been modified, make sure card to complete 3 is less than card to complete 4
                    if self.deck_matrix[suit][rank] > 0:
                        self.deck_matrix[suit][rank] += num_cards
                    else:
                        self.deck_matrix[suit][rank] += (num_cards * 2)

    def assign_hand_values(self):
        matrix = CardMatrix(self.cards)
        hand_values = []

        # remove cards one by one and assigns a value to them based on the cards around them
        for card in matrix.cards:
            matrix.deck_matrix[card.suit_val - 1][card.value - 1] = 0
            matrix.assign_deck_values()
            hand_values.append(matrix.deck_matrix[card.suit_val - 1][card.value - 1] + 1)
            matrix.deck_matrix[card.suit_val - 1][card.value - 1] = -1
        del matrix

        # resets matrix with new values
        self.deck_matrix.fill(0)
        for index, card in enumerate(self.cards):
            self.deck_matrix[card.suit_val - 1][card.value - 1] = hand_values[index]

        return hand_values

    def check_win(self):
        found_cards = 0

        # Rank matches

        # gets number of -1s in each column
        rank_count = np.count_nonzero(self.deck_matrix == -1, axis=0)
        pairs = [count for count in rank_count if count > 2]

        if any(pairs):
            # adds number of found cards
            found_cards += sum(pairs)

            # gets column of found cards, then sets them back to 0 to prevent double counting
            indicies = np.array([[index for index, count in enumerate(rank_count) if count > 2]])
            np.put_along_axis(self.deck_matrix, indicies, [0], axis=1)

        # Straight matches

        straight_count = 0

        for suit in range(4):
            for rank in range(13):

                # keeps loop from counting already found cards
                if straight_count != 0:
                    straight_count -= 1
                    continue

                seven_cards = set(self.deck_matrix[suit].take(range(rank, rank + 7), mode='wrap'))
                if len(seven_cards) == 1 and -1 in seven_cards:
                    return True

                three_cards = set(self.deck_matrix[suit].take(range(rank, rank + 3), mode='wrap'))
                if len(three_cards) == 1 and -1 in three_cards:
                    straight_count = 3
                    found_cards += 3

                    # edge case of if it goes K A 2 3
                    if self.deck_matrix[suit][(rank - 1) % 13] == -1:
                        found_cards += 1
                        self.deck_matrix[suit][rank: (rank + 3) % 13] = [0, 0, 0]
                        self.deck_matrix[suit][(rank - 1) % 13] = 0

                    # check the 4th card for straight
                    if self.deck_matrix[suit][(rank + 3) % 13] == -1:
                        straight_count += 1
                        found_cards += 1

        return True if found_cards == 7 else False


def block_print():
    sys.stdout = open(os.devnull, 'w')


def enable_print():
    sys.stdout = sys.__stdout__


def test_ai(runs):
    turns = []
    ais = 4
    stuck_turns = 1000

    block_print()
    for run in tqdm(range(runs)):
        game = GinRummy(0, ais)
        win = False
        checker = 0
        turn_count = 0
        while not win:
            checker += 1
            turn_count += 1
            for player in game.player_list:
                game.player_turn(player, True)
                if game.check_win(player):
                    print(f"{player.label} won!")
                    turns.append(turn_count)
                    win = True
                    break
            if checker > stuck_turns:
                enable_print()
                print(f"AI got stuck on game {run}")
                win = True
                block_print()
    enable_print()

    print(f"After {runs} runs, the average amount of turns it took for one of {ais} ais to win was: "
          f"{sum(turns) / len(turns)}")


def ai_input():
    ai_runs = input('>>')
    if ai_runs.isdigit() and int(ai_runs) > 0:
        test_ai(int(ai_runs))
        exit()
    print('please enter a valid number')
    return ai_input()


def player_input():
    players = input('>>')
    if players.isdigit():
        players = int(players)
        if players >= 1 and players <= 4:
            return GinRummy(players)
        if players == 0:
            print('enter number of simulated ai runs')
            ai_input()
    else:
        print('enter valid number of players')
    return player_input()


def start_game():
    print('enter number of players 0-4')
    game = player_input()
    game.rules()
    print("Have fun and type 'help' if you need to reread these rules at any time!")
    while True:
        for player in game.player_list:
            game.player_turn(player)
            if game.check_win(player):
                print(f"{player.label} won!")
                exit()