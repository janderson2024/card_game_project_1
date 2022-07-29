import CardLib
#from random import randint


class TenCards():
    pass


def main_loop(game, player_list):
    pass


def start_game():
    CardLib.print_test()

    oPack = CardLib.Draw([]) # creates an object pack
    CardLib.fill_deck_standard_52(oPack, ace_high=True)
    # print(pack)

    oPack.shuffle()
    print(oPack)

    oCard = oPack.pop_card() #
    print("------")
    print(oCard)
    oCard2 = oPack.pop_card()
    #print(oCard2)

    print("will the next card be high or low?")
    user_input = input("Choose h or l >>")

    if oCard2 < oCard:
        print(str(oCard2) + "is smaller than " + str(oCard))
        if user_input == "l":
            print("you chose correctly")
        else:
            print("you chose wrong!")
    else:
        print(str(oCard2) + "is larger than " + str(oCard))
        if user_input == "h":
            print("you chose correctly")
        else:
            print("you chose wrong!")


    #oUser_input = CardLib.get_user_input(["play", "hint", "draw", "skip", "end"],
     #                                    "Your Cards: " + str(player.hand))

    game = TenCards()
    print("Lets Play 10 Card's!")

#    main_loop(game, player_list)
