import CardLib as cl

# from games.GinRummy import GinRummy
# game = GinRummy(1)
# game.start_game()

# TODO: make rules so cards are unplayable, make ai work and play random valid cards, determine winner of the game

class GinRummy():
    PLAYER_COUNT = 4
    DEAL_COUNT = 7
    PLAY_OPTIONS = {'help': None, 'take card': None, 'exit': None, 'draw': None}
    
    player_list = []

    def __init__(self, player_number=1):
        self.deck = cl.fill_deck_standard_52(cl.Draw())
        self.deck.shuffle()

        for x in range(1, player_number + 1):
            self.player_list.append(cl.Player(f"Player{x}"))
        for x in range(1, self.PLAYER_COUNT - player_number + 1):
            self.player_list.append(cl.Player(f"AI{x}"))

        cl.deal_to_players(self.deck, self.player_list, self.DEAL_COUNT)


    def rules(self, player=None):
        print(f"Welcome to Gin Rummy!")
        print(f"The rules are simple, you have 7 cards and all of them have to be used in either a grouping of same rank, or in a straight of the same suit")
        print(f"You must have at least 3 Cards in each grouping, the typical winning hand will have some combination of:")
        print(f"Three of one rank, four of one rank, three in a straight, or four in a straight")
        print(f"Cards can only be used in one grouping, and it is possible to have a 7 card straight (but very unlikely)")
        print(f"An example winning hand would be: 1) [J\u2666], 2) [Q\u2666], 3) [K\u2666], 4) [3\u2666], 5) [3\u2665], 6) [3\u2663], 7) [3\u2660] \n")
        self.player_turn(player) if player != None else None
    PLAY_OPTIONS['help'] = rules

    def pick_up_card(self, player):
        player.add_card_to_hand(self.deck.pop_card())
        print(player)
        print("Choose a card to remove:")
        player_in = int(input(">>"))
        if player_in in range(1, player.get_amount_of_cards() + 1):
            player.play_card(player_in - 1)
            print(f"Your new hand:\n{self.sort_hand(player)}\n")
        else:
            print("That was not a valid option, try again!")
            self.pick_up_card(player)
    PLAY_OPTIONS['take card'] = pick_up_card

    def draw_card(self, player):
        self.deck.pop_card()
        print(f"Deck: {self.deck.card_list[-1]}\n")
        print(f"{self.sort_hand(player)}\n")
        print("Your turn:")
        print([str(option) for option in self.PLAY_OPTIONS if option != "draw"])
        player_in = input(">>")
        self.PLAY_OPTIONS[player_in](self, player)
    PLAY_OPTIONS['draw'] = draw_card


    def exit_program(self, player=None):
        exit()
    PLAY_OPTIONS['exit'] = exit_program

    def sort_hand(self, player):
        player.hand.sort_suit()
        player.hand.card_list.reverse()
        return player

    def get_choice(self, header):
        print(header)
        print([str(option) for option in self.PLAY_OPTIONS])
        player_in = input(">>")
        if player_in in self.PLAY_OPTIONS:
            return player_in
        print("That was not a valid option, try again!")
        self.get_choice(header)

    def player_turn(self, player):
        print(f"Deck: {self.deck.card_list[-1]}\n")
        print(f"{self.sort_hand(player)}\n")
        player_in = self.get_choice("Your turn:")
        self.PLAY_OPTIONS[player_in](self, player)

    def check_win(self, player):
        card_list = []
        for card in player.hand.card_list:
            card_list.append((card, card.rank))
        print([f"{str(tempcard[0])}, {str(tempcard[1])}" for tempcard in card_list])

        
        for card in card_list:
            counter = 0
            checker = card[1]
            for item in card_list:
                counter += item.count(checker)
            if counter > 2:
                card_list = [tempcard for tempcard in card_list if tempcard[1] != checker]

        # remainder of cards are ones used for straights
        card_list.sort()
        number = 0
        for card in card_list:
            if number == 0:
                number = int(card[1])
            elif str(number + 1) == card[1]:
                    number += 1
            else:
                return False
        return True
        # print([f"{str(tempcard[0])}, {str(tempcard[1])}" for tempcard in card_list])


def start_game():
    game = GinRummy()
    game.rules()
    print(f"Have fun and type 'help' if you need to reread these rules at any time! \n")
    while True:
        for player in game.player_list:
            player.clear_hand()
            player.add_card_to_hand(cl.Card(1,1))
            player.add_card_to_hand(cl.Card(2,1))
            player.add_card_to_hand(cl.Card(3,1))
            player.add_card_to_hand(cl.Card(4,1))
            player.add_card_to_hand(cl.Card(2,3))
            player.add_card_to_hand(cl.Card(2,4))
            player.add_card_to_hand(cl.Card(2,5))
            game.player_turn(player)
            if game.check_win(player):
                print(f"you won!")
                exit()
            