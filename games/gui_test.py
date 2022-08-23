import CardLib
from random import randint
import time

def main_loop(game, player_list):
    playing = True
    while playing:


        playing_round = True

        test_card_list = CardLib.CardList(x=10, y=400)
        test_card = CardLib.Card(2, 7, x=50, y=50)
        test_card2 = CardLib.Card(3, 13, x=130, y=50)
        test_card3 = CardLib.Card(1, 3, x=200, y=50)
        test_card4 = CardLib.Card(0, 15, x=280, y=50)

        test_card_list.add_card(test_card)
        test_card_list.add_card(test_card2)
        test_card_list.add_card(test_card3)
        test_card_list.add_card(test_card4)

        CardLib.gui.add_obj_to_be_drawn(test_card_list)

        test_discard = CardLib.Discard(x=50, y=50)
        test_discard.shuffle()

        test_draw = CardLib.DrawPile(x=500,y=500)
        test_draw = CardLib.fill_deck_standard_52(test_draw)



        CardLib.gui.add_obj_to_be_drawn(test_card_list)
        CardLib.gui.add_obj_to_be_drawn(test_discard)
        CardLib.gui.add_obj_to_be_drawn(test_draw)

        test_label = CardLib.gui.GuiLabel(0,0,"Hello World")
        CardLib.gui.add_obj_to_be_drawn(test_label)

        test_button = CardLib.gui.GuiButton(300,300,"Click Me")
        CardLib.gui.add_obj_to_be_drawn(test_button)

        while playing_round:
            obj = CardLib.gui.get_gui_user_input([card for card in test_card_list] + [test_button])
            if obj is test_button:
                print("Clicked!")
            else:
                test_card_list.rem_card(obj)
                test_discard.add_card(obj)

            CardLib.gui.redraw()


            #x, y = CardLib.gui.get_gui_user_input()
            #test_card = CardLib.Card(2, 7, x=x, y=y)
            #if randint(0, 10) > 5:
            #    test_card.set_display()
            #    print("flipped")

            #CardLib.gui.add_obj_to_be_drawn(test_card)
            #CardLib.gui.redraw()

            #if randint(0,10) > 5:
                #CardLib.gui.remove_all_obj()
            #time.sleep(3) #acts like AI turn
            #print("Done with sleep")


            
            

        action, _ = CardLib.get_user_input(["yes", "no"], "Do you want to play again?")

        if action == "no":
            playing = False

    print("Thank you for playing!")


def start_game():

    print("GUI TEST")
    CardLib.gui.start_gui("GUI test screen", 700, 700)
    print(CardLib.gui)

    player_list = [CardLib.Player("Player")]

    game = None

    player_list = None

    main_loop(game, player_list)