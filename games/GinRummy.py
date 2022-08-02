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
        return CardMatrix(player.hand.card_list).check_win()
        
class CardMatrix:
    deck_matrix = np.array([
        #    A      2      3      4      5      6      7      8      9      10     J      Q      K      
            [False, False, False, False, False, False, False, False, False, False, False, False, False], # Diamonds
            [False, False, False, False, False, False, False, False, False, False, False, False, False], # Hearts
            [False, False, False, False, False, False, False, False, False, False, False, False, False], # Clubs
            [False, False, False, False, False, False, False, False, False, False, False, False, False]  # Spades
    ])

    def __init__(self, card_list):
        for card in card_list:
            self.deck_matrix[card.suit_val - 1][card.value - 1] = True
        
    def check_win(self):
        matches = 0
        
        # gets number of nonzero items in each column, then makes that into a list of the numbered column if it has over 2 non zeros
        rank_count = np.count_nonzero(self.deck_matrix, axis=0)
        # makes sure there is a match
        if any([item for item in rank_count if item > 2]):
            # adds number of found cards to matches
            matches += sum([item for item in rank_count if item > 2])
            indicies = np.array([[index for index, item in enumerate(rank_count) if item > 2]])
            # gets indicies of each set of cards over 3 then resets those found matches to False in deck_matrix
            np.put_along_axis(self.deck_matrix, indicies, [False], axis=1)

        straight_count = 0
        
        for suit in range(4):
            for rank in range(13):
                # keeps loop from counting already found cards
                if straight_count != 0:
                    straight_count -= 1
                    continue
                # if the next three cards are true
                if all(self.deck_matrix[suit].take(range(rank, rank + 3), mode='wrap')) == 1:
                    straight_count = 3
                    # change found values to false
                    np.put(self.deck_matrix[suit], [range(rank, rank + 3)], [False], mode='wrap')
                    # if the fourth card is true
                    if self.deck_matrix[suit][(rank + 3) % 13] == True:
                        straight_count += 1
                        self.deck_matrix[suit][(rank + 3) % 13] = False

        return True if np.all(self.deck_matrix == False) else False
        

def start_game():
    game = GinRummy()
    game.rules()
    print(f"Have fun and type 'help' if you need to reread these rules at any time!")
    while True:
        for player in game.player_list:

            # arr = np.array([[1, 2, 3, 4, 5], [5, 4, 3, 2, 1]])
            # print(arr[1])
            # arr[1][1] = 3
            # print(arr[1])
            # newArr = arr[0].take(range(1, 7), mode='wrap')
            # print(newArr)
            # newArr = arr[1].take(range(1, 7), mode='wrap')
            # print(newArr)

            
            # game.check_win2([cl.Card(1,1), cl.Card(2,1), cl.Card(3,1), cl.Card(1,3), cl.Card(2,3), cl.Card(3,3)])

            player.clear_hand()
            player.add_card_to_hand(cl.Card(1,1))
            player.add_card_to_hand(cl.Card(2,1))
            player.add_card_to_hand(cl.Card(3,1))
            player.add_card_to_hand(cl.Card(2,2))
            player.add_card_to_hand(cl.Card(2,3))
            player.add_card_to_hand(cl.Card(2,4))
            player.add_card_to_hand(cl.Card(2,5))

            game.player_turn(player)
            if game.check_win(player):
                print(f"you won!")
                exit()
