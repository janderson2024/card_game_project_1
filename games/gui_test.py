import CardLib
from random import randint

class test_draw:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = 20
		self.height = 40
		self.color = (255,0,0)

		self.rect = CardLib.Gui.create_rect(self.x, self.y, self.width, self.height)

	def draw(self):
		CardLib.Gui.draw_rect(self.color, self.rect)



def main_loop(game, player_list):
    playing = True
    while playing:


        playing_round = True
        while playing_round:

            x, y = CardLib.GUI.get_gui_user_input()
            test = test_draw(x, y)
            CardLib.Gui.add_obj_to_be_drawn(test)
            CardLib.Gui.redraw()

            

        action, _ = CardLib.get_user_input(["yes", "no"], "Do you want to play again?")

        if action == "no":
            playing = False

    print("Thank you for playing!")


def start_game():

    print("GUI TEST")
    CardLib.Gui.start_gui("GUI test screen")
    print(CardLib.Gui)

    player_list = [CardLib.Player("Player")]

    game = None

    player_list = None

    main_loop(game, player_list)