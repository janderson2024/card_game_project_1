import CardLib as cl
import random
import time
import numpy as np

class GinRummy():
    PLAYER_COUNT = 4
    DEAL_COUNT = 7
    PLAY_OPTIONS = {'help': None, 'take card': None, 'exit': None, 'skip': None, 'draw': None}

    shown_card = None
    player_list = []

    def __init__(self, player_number=1):
        self.deck = cl.fill_deck_standard_52(cl.Draw())
        self.deck.shuffle()

        for x in range(1, player_number + 1):
            self.player_list.append(cl.Player(f"Player{x}"))
        for x in range(1, self.PLAYER_COUNT - player_number + 1):
            self.player_list.append(cl.Player(f"AI{x}", True))

        cl.deal_to_players(self.deck, self.player_list, self.DEAL_COUNT)
        self.shown_card = self.deck.card_list.pop()

    # Functions called directly by player input

    def exit_program(self, player=None):
        exit()

    PLAY_OPTIONS['exit'] = exit_program

    def rules(self, player=None):
        print(f"Welcome to Gin Rummy!")
        print(
            f"The rules are simple, you have 7 cards and all of them have to be used in either a grouping of same "
            f"rank, or in a straight of the same suit")
        print(
            f"You must have at least 3 Cards in each grouping, the typical winning hand will have some combination of:")
        print(f"Three of one rank, four of one rank, three in a straight, or four in a straight")
        print(
            f"Cards can only be used in one grouping, and it is possible to have a 7 card straight (but very unlikely)")
        print(
            f"An example winning hand would be: 1) [J\u2666], 2) [Q\u2666], 3) [K\u2666], 4) [3\u2666], 5) [3\u2665], "
            f"6) [3\u2663], 7) [3\u2660] \n")

        self.player_turn(player) if player is not None else None

    PLAY_OPTIONS['help'] = rules

    def skip_turn(self, player):
        return

    PLAY_OPTIONS['skip'] = skip_turn

    def draw_card(self, player):
        player.add_card_to_hand(self.deck.pop_card())
        print(player)
        print("Choose a card to remove:")
        player_in = int(input(">>"))
        self.remove_card(player, player_in)

    PLAY_OPTIONS['draw'] = draw_card

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
        if not player.is_ai:
            print(player)
            print("Choose a card to remove:")
            player_in = int(input(">>"))
            self.remove_card(player, player_in)
        else:
            new_shown_card = player.play_card()
            print(f"{player.label} picked up {picked_up_card} and put down {new_shown_card}")
            self.shown_card = new_shown_card

    PLAY_OPTIONS['take card'] = pick_up_card

    # Helper functions

    def sort_hand(self, player):
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
        for user in self.player_list:
            self.deck.card_list = [card for card in self.deck.card_list if card not in user.hand.card_list]
        self.deck.shuffle()
        self.shown_card = self.deck.card_list.pop()
        print("Reshuffled a new deck!")

    def rem_rank_matches(self, cards):
        card_list = []
        for card in cards:
            card_list.append((card, card.value))

        for card in card_list:
            counter = 0
            checker = card[1]
            for item in card_list:
                counter += item.count(checker)
            if counter > 2:
                card_list = [tempcard for tempcard in card_list if tempcard[1] != checker]
                return self.rem_rank_matches([card_pair[0] for card_pair in card_list])
        return [card_pair[0] for card_pair in card_list]

    def rem_straight_matches(self, card_list):
        card_list = sorted(card_list, key=lambda card: (0 - card.value, card.suit), reverse=True)
        start = False
        counter = 1
        for num, card in enumerate(card_list):
            if num + 1 < len(card_list) and card.value + 1 == card_list[num + 1].value and card.suit == card_list[
               num + 1].suit:
                if not start:
                    start = True
                    start_num = num
                counter += 1
            elif counter > 2:
                return self.rem_straight_matches(card_list[0:start_num] + card_list[num + 1:len(card_list)])
            else:
                start = False
                counter = 1
        return card_list

    def ai_turn(self, player):
        # assign weight to each possible option ex: picking up a 3 has a weight of 2 when 2 3s are in hand already
        return

    # Called directly by main loop

    def player_turn(self, player):
        if not self.deck.card_list:
            self.reshuffle_deck()

        if not player.is_ai:
            time.sleep(1)
            print(f"\n{player.label}'s turn:")
            time.sleep(1)
            print(f"\nDeck: {self.shown_card}")
            time.sleep(1)
            player_input = self.get_choice(f"\n{self.sort_hand(player)}", self.PLAY_OPTIONS)
            self.PLAY_OPTIONS[player_input](self, player)
        else:
            time.sleep(1)
            self.pick_up_card(player)

    def check_win2(self, player):
        card_list = player.hand.card_list
        card_list = self.rem_straight_matches(card_list)
        card_list = self.rem_rank_matches(card_list)
        return True if not card_list else False

    def check_win(self, player):
        matrix = CardMatrix(player.hand.card_list)
        matrix.assign_values()
        return matrix.check_win()

# for dropping a card: 
# use checkwin to keep cards in matching from being discarded
# use the remaining cards to determine which to drop

# ISSUE: when cards are lined up like
# 0 1 1 1 0
# 0 1 0 0 0
# 0 1 0 0 0
# 0 1 0 0 0

# they get valued at: 
# 6 1 1 1 6
# 0 1 0 0 0
# 0 1 0 0 0
# 0 6 0 0 0

# should be valued at something like: 
# 5 1 1 1 6
# 0 1 0 0 0
# 0 1 0 0 0
# 0 6 0 0 0

class CardMatrix:

    def __init__(self, card_list):
        self.cards = card_list
        self.deck_matrix = np.array([
        #    A  2  3  4  5  6  7  8  9  10 J  Q  K      
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Diamonds
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Hearts
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Clubs
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Spades
        ])
        for card in self.cards:
            self.deck_matrix[card.suit_val - 1][card.value - 1] = -1   


    def assign_values(self):
        # need to check for straights to assign correct values
        for card in self.cards:
            # idea: choose card, then check to the right to see if there is another
            # if there is up the added value by x, repeat until open spot and ramp it up so 4 in a row counts for a lot 

            # idea 2: electric boogaloo
            # look for straights of 3 and add value to cards immediatly around it to make straights of 4 more valuable

            for num in (-2, -1, 0, 2, 3, 4):
                if self.deck_matrix[card.suit_val - 1][(card.value - num) % 13] != -1:
                    self.deck_matrix[card.suit_val - 1][(card.value - num) % 13] += 2


        # rank matches

        for rank in range(13):

            column = self.deck_matrix[:, rank]
            num_cards = len([num for num in column if num == -1])
            
            for suit in range(4):
                if self.deck_matrix[suit][rank] != -1:
                    # add less if its already been modified, make sure card to complete 3 is less than card to complete 4
                    if self.deck_matrix[suit][rank] > 0:
                        self.deck_matrix[suit][rank] += num_cards
                    else:
                        self.deck_matrix[suit][rank] += (num_cards * 2)


    def check_win(self):
        found_cards = 0
        

        # Rank matches

        # gets number of -1s in each column
        rank_count = np.count_nonzero(self.deck_matrix == -1, axis=0)

        # makes sure there is a match
        if any([item for item in rank_count if item > 2]):

            # adds number of found cards
            found_cards += sum([item for item in rank_count if item > 2])

            # gets column of found cards, then sets them back to 0 to prevent double counting
            indicies = np.array([[index for index, item in enumerate(rank_count) if item > 2]])
            np.put_along_axis(self.deck_matrix, indicies, [0], axis=1)


        # Straight matches

        straight_count = 0

        for suit in range(4):
            for rank in range(13):

                # keeps loop from counting already found cards
                if straight_count != 0:
                    straight_count -= 1
                    continue

                # checking for 7 card straight
                seven_cards = set(self.deck_matrix[suit].take(range(rank, rank + 7), mode='wrap'))
                if len(seven_cards) == 1 and -1 in seven_cards:
                    return True

                # checking for 3 card straight
                three_cards = set(self.deck_matrix[suit].take(range(rank, rank + 3), mode='wrap'))
                if len(three_cards) == 1 and -1 in three_cards:
                    straight_count = 3
                    found_cards += 3

                    # check the 4th card
                    if self.deck_matrix[suit][(rank + 3) % 13] == -1:
                        straight_count += 1
                        found_cards += 1
                    
        return True if found_cards == 7 else False
        

def start_game():
    game = GinRummy()
    game.rules()
    print(f"Have fun and type 'help' if you need to reread these rules at any time!")
    while True:
        for player in game.player_list:
            # arr = np.array([-1, -1, -1, -1, -1])
            # print(arr)
            # set_arr = set(arr)
            # print(set_arr)
            # if len(set_arr) == 1 and -1 in set_arr:
            #     print("POGGERS")

            # arr[1][1] = 3
            # print(arr[1])
            # newArr = arr[0].take(range(1, 7), mode='wrap')
            # print(newArr)
            # newArr = arr[1].take(range(1, 7), mode='wrap')
            # print(newArr)

            
            # game.check_win2([cl.Card(1,1), cl.Card(2,1), cl.Card(3,1), cl.Card(1,3), cl.Card(2,3), cl.Card(3,3)])

            # player.clear_hand()
            # player.add_card_to_hand(cl.Card(1,1))
            # player.add_card_to_hand(cl.Card(2,1))
            # player.add_card_to_hand(cl.Card(3,1))
            # player.add_card_to_hand(cl.Card(4,2))
            # player.add_card_to_hand(cl.Card(4,3))
            # player.add_card_to_hand(cl.Card(3,3))
            # player.add_card_to_hand(cl.Card(2,12))

            player.clear_hand()
            player.add_card_to_hand(cl.Card(1,1))
            player.add_card_to_hand(cl.Card(1,2))
            player.add_card_to_hand(cl.Card(1,3))
            player.add_card_to_hand(cl.Card(1,4))
            player.add_card_to_hand(cl.Card(2,4))
            player.add_card_to_hand(cl.Card(3,4))
            player.add_card_to_hand(cl.Card(4,4))

            game.player_turn(player)
            if game.check_win(player):
                print(f"you won!")
                exit()
