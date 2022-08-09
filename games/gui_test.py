import CardLib
from random import randint
import time

class test_draw:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = 20
		self.height = 40
		self.color = (255,0,0)

		self.rect = CardLib.gui.create_rect(self.x, self.y, self.width, self.height)

	def draw(self):
		CardLib.gui.draw_rect(self.color, self.rect)



def main_loop(game, player_list):
    playing = True
    while playing:


        playing_round = True

        test_card_list = CardLib.CardList(x=10, y=400)
        CardLib.gui.add_obj_to_be_drawn(test_card_list)

        while playing_round:
            x, y = CardLib.gui.get_gui_user_input()
            test_card = CardLib.Card(2, 7, x=x, y=y)

            test_card_list.add_card(test_card)
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
    CardLib.gui.start_gui("GUI test screen")
    print(CardLib.gui)

    player_list = [CardLib.Player("Player")]

    game = None

    player_list = None

    main_loop(game, player_list)