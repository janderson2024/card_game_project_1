import random
from User_Input import getUserInput

from card_list.Hand import Hand

class Player:
    def __init__(self, label, is_ai=False):
        self.is_ai = is_ai
        self.hand = Hand([])
        self.label = label
        self.win_count = 0

    def __str__(self):
        return self.label + ': ' + str(self.hand)
        
    def get_label(self):
        return self.label

    def get_win_count(self):
        return self.win_count

    def round_winner(self):
        self.win_count = self.win_count + 1

    def get_amount_of_cards(self):
        return len(self.hand)

    def add_card_to_hand(self, card):
        self.hand.add_card(card)

    def add_cards_to_hand(self, cards):
        for card in cards:
            self.add_card(card)

    def ai_plays_card(self, valid_cards):
        card_num = random.randint(0, len(valid_cards)-1)
        card_to_play = valid_cards.get_card_list()[card_num]
        print(self.label, " played: ", card_to_play)
        self.hand.rem_card(card_to_play)
        return card_to_play

    def play_card(self, game):
        valid_cards = self.hand.get_all_valid_cards(game.is_card_valid)
        
        if self.is_ai:
            while len(valid_cards) == 0:
                drew_card = game.draw_card()
                if drew_card is None:
                    return None
                self.add_card_to_hand(drew_card)
                valid_cards = self.hand.get_all_valid_cards(game.is_card_valid)
            return self.ai_plays_card(valid_cards)
        else:
            print("-------------------")
            print("The last discard is: ", game.discard.get_top_card())

            played_valid = False
            while not played_valid:
                action, card_num =getUserInput(["play", "hint", "draw", "skip", "end"], "What would you like to do?\nCards: " + str(self.hand))

                if action == "play":
                    possible_card_nums = [str(num) for num in range(1, len(self.hand)+1)]
                    if card_num is None or card_num not in possible_card_nums:
                        card_num, _ = getUserInput(possible_card_nums, "Pick a card num to play")

                    poss_card = self.hand.get_card_list()[int(card_num)-1]
                    if poss_card in valid_cards.get_card_list():
                        self.hand.rem_card(poss_card)
                        print(self.label, " played: ", poss_card)
                        played_valid = True
                        return poss_card
                    else:
                        print("That card doesn't follow the game rules!")
                if action == "hint":
                    if(len(valid_cards) > 0):
                        print("Hint: you can play these: ", str(valid_cards))
                    else:
                        print("Hint: you need to draw")
                if action == "draw":
                    drew_card = game.draw_card()
                    if drew_card is None:
                        print("The Draw pile is Empty! Cannot draw new card")
                    else:
                        self.add_card_to_hand(drew_card)
                        valid_cards = self.hand.get_all_valid_cards(game.is_card_valid)
                        print("Drew : ", drew_card)
                if action == "skip":
                    print(self.label, " skipped!")
                    return None
                if action  == "end":
                    print("Thanks for playing!")
                    exit()




        return None

    def clear_hand(self):
        self.hand.rem_all_cards()




    #test code :
    # user = Player("Player 1")
    # user.add_cards([Card(1,1), Card(1,2), Card(1,3)])
    # print(user)
    # print(user.play_card(1))
    # print(user)

    # ai1 = Player("AI1", True)
    # ai1.add_cards([Card(1,1), Card(1,2), Card(1,3), Card(1,4), Card(1,5), Card(1,6)])
    # print(ai1)
    # ai1.play_card()
    # print(ai1)