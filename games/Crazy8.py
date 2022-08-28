### Author: Joshua Anderson
### Date: 7/19/22
### gitlab: gitlab.com/janderson2024
### Written for the CardLib library

import CardLib
from random import randint
import time


class Crazy8:
    DEAL_COUNT = 5
    PLAYER_COUNT = 4

    def __init__(self):
        self.stock = CardLib.DrawPile([], x=30, y=50)
        self.discard = CardLib.Discard([], x=300, y=300)

        self.stock_label = CardLib.gui.GuiLabel("Draw Pile", x=5, y=0)
        self.discard_label = CardLib.gui.GuiLabel("Discard", x=280, y=260)
        self.player_skip = CardLib.gui.GuiButton(" Skip! ", x=600, y=550)

        self._setup_decks()

    def _setup_decks(self):
        self.stock.rem_all_cards()
        self.stock = CardLib.fill_deck_standard_52(self.stock)
        self.stock.shuffle()

        self.discard.rem_all_cards()
        self.discard.add_card(self.stock.pop_card())

    def add_all_game_gui(self, player_list):
        CardLib.gui.add_obj_to_be_drawn(self.stock)
        CardLib.gui.add_obj_to_be_drawn(self.discard)

        CardLib.gui.add_obj_to_be_drawn(self.stock_label)
        CardLib.gui.add_obj_to_be_drawn(self.discard_label)

        CardLib.gui.add_obj_to_be_drawn(self.player_skip)

        for player in player_list:
            CardLib.gui.add_obj_to_be_drawn(player)

    def is_card_valid(self, card):
        top_card = self.discard.get_top_card()
        return card.rank == "8" or (card.suit == top_card.suit or card.rank == top_card.rank)

    def check_player_win(self, player):
        return player.get_amount_of_cards() == 0

    def on_round_won(self, player=None):
        if player:
            player.round_winner()
        CardLib.gui.remove_all_obj()
        self._setup_decks()

    def on_card_played(self, card):
        self.discard.add_card(card)
        CardLib.gui.redraw()

    def get_valid_cards(self, player):
        return player.hand.get_all_valid_cards(self.is_card_valid)

    def get_ai_turn(self, player):
        valid_cards = self.get_valid_cards(player)
        while len(valid_cards) == 0:

            if len(self.stock) == 0:
                return None
            player.add_card_to_hand(self.stock.pop_card())
            valid_cards = self.get_valid_cards(player)
            CardLib.gui.redraw()
            time.sleep(0.3)

        card_num = randint(0, len(valid_cards) - 1)
        card_to_play = valid_cards.get_card_at(card_num)

        player.hand.rem_card(card_to_play)

        return card_to_play

    def get_all_valid_gui(self, player):
        valid_choices = [self.player_skip]
        
        if len(self.stock):
            valid_choices += [self.stock]

        valid_choices += self.get_valid_cards(player)

        #print(valid_choices)
        return valid_choices

    def get_user_turn(self, player):
        valid_choices = self.get_all_valid_gui(player)

        played_valid = False
        while not played_valid:

            obj = CardLib.gui.get_gui_user_input(valid_choices)

            if obj is self.stock:
                #draw
                player.hand.add_card(self.stock.pop_card())
                valid_choices = self.get_all_valid_gui(player)

            elif obj is self.player_skip:
                played_valid = True
                return None

            else:
                player.hand.rem_card(obj)
                played_valid = True
                return obj

            CardLib.gui.redraw()

    def on_player_turn(self, player):
        if player.is_ai:
            played_card = self.get_ai_turn(player)
        else:
            played_card = self.get_user_turn(player)

        return played_card

def play_again(winner_label):
    play_again_prompt = CardLib.gui.GuiLabel("Do you want to play again?", x=150, y=260)
    yes = CardLib.gui.GuiButton(" yes ", x=210, y=400)
    no = CardLib.gui.GuiButton(" no ", x=400, y=400)

    CardLib.gui.add_obj_to_be_drawn(winner_label)
    CardLib.gui.add_obj_to_be_drawn(play_again_prompt)
    CardLib.gui.add_obj_to_be_drawn(yes)
    CardLib.gui.add_obj_to_be_drawn(no)

    selectable_objects = [yes,no]
    obj = CardLib.gui.get_gui_user_input(selectable_objects)
    CardLib.gui.remove_all_obj()

    return obj is yes

def main_loop(game, player_list):
    playing = True
    while playing:
        game.add_all_game_gui(player_list)
        game.stock, player_list = CardLib.deal_to_players(game.stock, player_list, game.DEAL_COUNT)
        CardLib.gui.redraw()

        player_turn_icon = CardLib.gui.GuiLabel("*")
        CardLib.gui.add_obj_to_be_drawn(player_turn_icon)

        current_player = 0

        playing_round = True

        skip_count = 0
        while playing_round:
            player = player_list[current_player]

            #this icon code is jank. Do not judge
            icon_x = player.gui_label.gui_obj.x + player.gui_label.gui_obj.width + 15
            player_turn_icon.gui_obj.move(icon_x, player.gui_obj.y+5)
            CardLib.gui.redraw()

            played_card = game.on_player_turn(player)

            if played_card is not None:
                skip_count = 0
                game.on_card_played(played_card)
                #print(player.label, " played: ", played_card)
            else:
                print(player.label, " skipped!")
                skip_count += 1

                if skip_count > 16:
                    playing_round = False
                    won_label = CardLib.gui.GuiLabel("Draw", x=300, y=180)   
                    game.on_round_won()

            if game.check_player_win(player):
                CardLib.gui.redraw()
                playing_round = False
                won_label = CardLib.gui.GuiLabel(player.label + " has won!", x=240, y=180)

                game.on_round_won(player)
                
            else:
                current_player = (current_player + 1) % len(player_list)
                CardLib.gui.redraw()
                time.sleep(0.5)


        CardLib.gui.redraw()
        for player in player_list:
                player.clear_hand()

        playing = play_again(won_label)

    print("Thank you for playing!")

def display_rules():
    header = CardLib.gui.GuiLabel("Crazy 8 rules:", x=240, y=20)
    CardLib.gui.add_obj_to_be_drawn(header)

    rules = [
        ("Each player is dealt 5 cards", 130, 100),
        ("On the player's turn:", 20, 170), 
        ("The player must play a valid card, or skip.", 40, 210),
        ("A valid card:", 40, 280),
        ("matches the rank or suit of the discard", 55, 310),
        ("or the card is an 8!", 55, 340),
        ("If the player doesn't have a valid card:", 40, 400), 
        ("they must draw til they get one", 55, 430),
        ("or they must skip if the draw pile is empty.", 55, 460),
        ("Winner is the first to play all of their cards!", 40, 550)
    ]

    for rule in rules:
        line = CardLib.gui.GuiLabel(rule[0], x=rule[1], y=rule[2])
        CardLib.gui.add_obj_to_be_drawn(line)

    confirm = CardLib.gui.GuiButton(" Understood! ", x=250, y=630)
    CardLib.gui.add_obj_to_be_drawn(confirm)

    selectable_objects = [confirm]
    obj = CardLib.gui.get_gui_user_input(selectable_objects)
    CardLib.gui.remove_all_obj()

def start_game():
    CardLib.gui.start_gui("Crazy 8's!", 700, 700)

    game = Crazy8()
    #print("Lets Play Crazy 8's!")

    display_rules()

    player_locations = [(5, 550), (10, 250), (300, 10), (540, 250)]
    player_list = [CardLib.Player("Player", x=5,y=550)]

    for num in range(1, game.PLAYER_COUNT):
        player_list.append(CardLib.Player("AI #" + str(num), is_ai=True, x=player_locations[num][0], y=player_locations[num][1]))

    main_loop(game, player_list)