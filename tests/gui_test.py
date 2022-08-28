#CODE TO GO BACK UP A LAYER TO USE CARDLIB
import sys
sys.path.insert(0, '..')

##CURRENTLY BROKEN DUE TO IMAGES.... idk maybe figure it out later. I'm tired

import CardLib
from random import randint
import time

def main_loop(game, player_list):
    playing = True
    while playing:


        playing_round = True

        test_card_list = CardLib.CardList(x=200, y=400)
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
        test_draw.card_list = test_draw.card_list[:5]

        test_player = CardLib.Player("Test Player", True, x=300,y=50)
        CardLib.gui.add_obj_to_be_drawn(test_player)
        test_player.add_card_to_hand(test_draw.pop_card())




        CardLib.gui.add_obj_to_be_drawn(test_card_list)
        CardLib.gui.add_obj_to_be_drawn(test_discard)
        CardLib.gui.add_obj_to_be_drawn(test_draw)

        test_label = CardLib.gui.GuiLabel("Hello World", x=0, y=0)
        CardLib.gui.add_obj_to_be_drawn(test_label)

        test_button = CardLib.gui.GuiButton("Click Me", x=300, y=300)
        CardLib.gui.add_obj_to_be_drawn(test_button)
        test_button2 = CardLib.gui.GuiButton("Click Me2", x=320, y=320)
        CardLib.gui.add_obj_to_be_drawn(test_button2)

        while playing_round:
            selectable_objects = [card for card in test_card_list] + [test_button, test_button2] + [test_player]
            if len(test_draw) > 0:
                selectable_objects += [test_draw]

            obj = CardLib.gui.get_gui_user_input(selectable_objects)
            if obj is test_button:
                test_player.is_ai = not test_player.is_ai
            elif obj is test_draw:
                test_player.add_card_to_hand(test_draw.pop_card())
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

if __name__ == '__main__':
    start_game()