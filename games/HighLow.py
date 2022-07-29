import CardLib
#from random import randint


class HighLow():

    def set_up_pack(self):
        oPack = CardLib.Draw([])  # creates an object pack
        CardLib.fill_deck_standard_52(oPack, ace_high=True)
        oPack.shuffle()
        return oPack

    def card(self):
        return self.set_up_pack().pop_card()

    def points(self, player_name):
        oPlayer1 = CardLib.Player(player_name)
        oPlayer1.round_winner()
        oPoints = oPlayer1.get_win_count()
        print(str(oPlayer1) + " has " + str(oPoints) + " points")


def main_loop(game, player_name):
    # print(game.set_up_pack())
    print(player_name)
    #oPlayer1 = CardLib.Player(player_name)

    oCard1 = game.card()
    oCard2 = game.card()
    print(oCard1)
    print("will the next card be high or low?")
    user_input = input("Choose h or l >> ")

    if oCard2 < oCard1:
        print(str(oCard2) + " is smaller than " + str(oCard1))
        if user_input == "l":
            print("you chose correctly")
            game.points(player_name)

        else:
            print("you chose wrong!")
    else:
        print(str(oCard2) + " is larger than " + str(oCard1))
        if user_input == "h":
            print("you chose correctly")
            game.points(player_name)
        else:
            print("you chose wrong!")

    pass


def start_game():
    CardLib.print_test()

    game = HighLow()
    # print(game.set_up_pack())
    print("Lets Play High Low!! ")

    player_name = "Chris"
    main_loop(game, player_name)
