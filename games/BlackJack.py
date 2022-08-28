### Author: Joshua Anderson
### Date: 8/28/22
### gitlab: gitlab.com/janderson2024
### Written for the CardLib library

import CardLib

BLACKJACK_RULES = {
    1: (1, 11),
    2: (2),
    3: (3),
    4: (4),
    5: (5),
    6: (6),
    7: (7),
    8: (8),
    9: (9),
    10: (10),
    11: (10),
    12: (10),
    13: (10)
}

class BlackJack:

    def __init__(self):
        self.deck = CardLib.DrawPile()
        self.fill_and_shuffle()


    def fill_and_shuffle(self):
        self.deck.rem_all_cards()
        self.deck = CardLib.fill_deck_standard_52(self.deck)
        self.deck.shuffle()

    def get_biggest_score(self, cards):
        card_vals = [card.value for card in cards]
        possible_scores = CardLib.calculate_all_possible_scores(BLACKJACK_RULES, card_vals)

        filtered_scores = [score for score in possible_scores if score <= 21]

        if len(filtered_scores) == 0:
            return min(possible_scores)
        else:
            return max(filtered_scores)

    def get_ai_turn(self, player):
        biggest_score = self.get_biggest_score(player.hand)

        if biggest_score == 21:
            print("The dealer got a blackJack!", player.hand)
            return biggest_score

        while biggest_score < 17:
            print("Dealer has these cards:", player.hand, "and this score:", biggest_score)
            player.add_card_to_hand(self.deck.pop_card())
            biggest_score = self.get_biggest_score(player.hand)
            print("--------------------")

        print("Dealer has these cards:", player.hand, "and this score:", biggest_score)
        print("--------------------")
        return biggest_score

    def get_user_turn(self, player):
        biggest_score = self.get_biggest_score(player.hand)

        if biggest_score == 21:
            print("You got a black jack!", player.hand)
            print("--------------------")
            return biggest_score

        while biggest_score <= 21:
            print("You have these cards:", player.hand, "and this score:", biggest_score)
            action, _ = CardLib.get_user_input(["hit","stand","exit"], "Your turn: ")

            if action == "hit":
                player.add_card_to_hand(self.deck.pop_card())
                biggest_score = self.get_biggest_score(player.hand)

            if action == "stand":
                return biggest_score

            if action == "exit":
                print("Thanks for playing!")
                exit()
            print("--------------------")

        print("You have these cards:", player.hand, "and this score:", biggest_score)
        print("--------------------")
        return biggest_score

def main_loop(game, player_list):
    playing = True
    while playing:
        game.deck, player_list = CardLib.deal_to_players(game.deck, player_list, 2)

        #Player turn first
        player_score = game.get_user_turn(player_list[0])
        if player_score > 21:
            #player busted!
            print("Player busted! (",player_score,") Dealer wins!")
        else:
            #Dealer turn next
            dealer_score = game.get_ai_turn(player_list[1])
            if dealer_score > 21:
                #dealer busted!
                print("Dealer busted! (",dealer_score,") Player wins!")
            else:
                print("Player had a score of:", player_score, "and Dealer had a score of:", dealer_score)
                #check highest score
                if player_score > dealer_score:
                    print("Player wins!")
                elif dealer_score > player_score:
                    print("Dealer wins!")
                else:
                    print("It was a tie!")


        #setup the game for next round
        game.fill_and_shuffle()
        for player in player_list:
            player.clear_hand()

        #asks the user to play the game again
        print("--------------------")
        action, _ = CardLib.get_user_input(["yes", "no"], "Do you want to play again?")
        if action == "no":
            playing = False

    #only prints once the user is done playing
    print("Thank you for playing!")


def start_game():
    game = BlackJack()

    print("Lets play BlackJack!")
    print("--------------------")

    player_list = [CardLib.Player("Player"), CardLib.Player("Dealer", is_ai=True)]

    main_loop(game, player_list)