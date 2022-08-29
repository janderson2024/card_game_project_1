### Author: Joshua Anderson
### Date: 8/28/22
### gitlab: gitlab.com/janderson2024
### Written for the CardLib library

import CardLib
from random import randint
import time

POSSIBLE_NAMES = [
    "dragon",
    "brutes",
    "zombie",
    "mutant",
    "lizard",
    "giant",
    "devil",
    "whale",
    "mummy",
    "snakes",
    "ghost"
]

def make_stats(total_sum, stat_count=3):
    stats = ()
    for count in range(stat_count):
        num = 1
        if total_sum > 1:
            num = randint(1, total_sum-(stat_count-count))
        stats = stats + (num,)
        total_sum -= num
    return stats

class DDCard(CardLib.Card):
    WIDTH = 110
    HEIGHT = 140

    def __init__(self, label, health, defense, damage):
        self.label = label
        self.health = health
        self.damage = damage
        self.defense = defense
        self.has_move = True

        self.gui_obj = CardLib.gui.GuiObject(0,0,self.WIDTH,self.HEIGHT, self.gui_draw)
        
    def take_damage(self, amount):
        if amount > self.defense:
            self.health -= amount
        else:
            print(self.label, "blocked the attack!")
        return self.health <= 0

    def __str__(self):
        return f"{self.label}: is [{self.health},{self.defense},{self.damage}]"

    def __eq__(self, other):
        if isinstance(other, DDCard):
            return self.label == other.label and self.damage == other.damage and self.defense == other.defense and self.has_move == other.has_move
        return False

    def gui_draw(self):
        if self.has_move:
            color = (100,100,100)
        else:
            color = (40,40,40)

        background_rect = CardLib.gui.create_rect(self.gui_obj.x, self.gui_obj.y, self.WIDTH, self.HEIGHT)
        CardLib.gui.draw_rect(color, background_rect)

        if self.displayable:
            gui_label = CardLib.gui.GuiLabel(self.label, x=self.gui_obj.x+4, y=self.gui_obj.y+5)
            stats = CardLib.gui.GuiLabel(f"[{self.health},{self.defense},{self.damage}]", x=self.gui_obj.x+5, y= self.gui_obj.y+70)
            
            stats.gui_obj.draw()
        else:
            gui_label = CardLib.gui.GuiLabel("DDCard", x=self.gui_obj.x, y=self.gui_obj.y+45)
        gui_label.gui_obj.draw()

class DDPlayer(CardLib.Player):
    health = 3
    WIDTH = 640
    HEIGHT = 150


    def _init_gui(self, x, y):
        self.gui_obj = CardLib.gui.GuiObject(x, y, self.WIDTH, self.HEIGHT, self.gui_draw)
        self.background = CardLib.gui.create_rect(self.gui_obj.x, self.gui_obj.y, self.WIDTH, self.HEIGHT)
        self.gui_label = CardLib.gui.GuiLabel(self.label, self.gui_obj.x+20, self.gui_obj.y+50)

        self.kept_hand = DDCardList(2, 50, self.gui_obj.x+170, self.gui_obj.y+5)

    def hurt(self):
        self.health -= 1

        return self.health <= 0

    def gui_draw(self):
        heart_label = CardLib.gui.GuiLabel(f"{self.health} ¤", self.gui_obj.x+570, self.gui_obj.y+50)

        CardLib.gui.draw_rect((150,100,160), self.background)
        self.gui_label.gui_obj.draw()
        self.kept_hand.gui_obj.draw()
        heart_label.gui_obj.draw()

class DDCardList(CardLib.CardList):
    def __init__(self, card_count, xoffset, x=0, y=0):
        self.card_list = [None for _ in range(card_count)]
        self.max_cards = card_count
        self.xoffset = xoffset

        width = (DDCard.WIDTH * card_count) + (self.xoffset * card_count - 1)
        self.gui_obj = CardLib.gui.GuiObject(x, y, width, DDCard.HEIGHT, self.gui_draw)

    def spots_left(self):
        return self.max_cards - len([card for card in self.card_list if card != None])

    def add_card(self, card):
        for spot in range(self.max_cards):
            if self.card_list[spot] == None:
                self.card_list[spot] = card
                card.gui_obj.move(self.gui_obj.x + (DDCard.WIDTH + self.xoffset) * spot, self.gui_obj.y)
                return

    def rem_card(self, rem_card):
        for index, card in enumerate(self.card_list):
            if rem_card is card:
                self.card_list[index] = None
                return

    def rem_all_cards(self):
        for card in self.card_list:
            self.rem_card(card)

    def gui_draw(self):
        for index, card in enumerate(self.card_list):
            x = self.gui_obj.x + (DDCard.WIDTH + self.xoffset) * index
            if card == None:
                CardLib.gui.draw_rect((0,0,0),CardLib.gui.create_rect(x, self.gui_obj.y, DDCard.WIDTH, DDCard.HEIGHT))
            else:
                card.gui_obj.draw()


class DeckDuel:
    def __init__(self):
        self.player_on_table = DDCardList(3, 50, x=200, y=380)
        self.enemy_on_table = DDCardList(3, 50, x=200, y=180)
        self.player_draw = CardLib.gui.GuiButton(" draw ", x=800, y=580)
        self.player_end = CardLib.gui.GuiButton(" pass ", x=805, y=630)
        self.card_label = CardLib.gui.GuiLabel("[health, defense, damage]", x=250, y=330)

    def add_all_game_gui(self, players):
        CardLib.gui.add_obj_to_be_drawn(self.player_on_table)
        CardLib.gui.add_obj_to_be_drawn(self.enemy_on_table)
        CardLib.gui.add_obj_to_be_drawn(self.player_draw)
        CardLib.gui.add_obj_to_be_drawn(self.player_end)
        CardLib.gui.add_obj_to_be_drawn(self.card_label)

        for player in players:
            CardLib.gui.add_obj_to_be_drawn(player)

    def deal_new_card(self):
        label = POSSIBLE_NAMES[randint(0, len(POSSIBLE_NAMES) - 1)]
        health, defense, damage = make_stats(10, 3)
        return DDCard(label, health, defense, damage)

    def deal_to_players(self, players):
        for player in players:
            for _ in range(2):
                player.kept_hand.add_card(self.deal_new_card())
        return players

    def on_round_won(self, players):
        CardLib.gui.remove_all_obj()
        self.player_on_table.rem_all_cards()
        self.enemy_on_table.rem_all_cards()
        for player in players:
            player.health = 3
            player.kept_hand.rem_all_cards()


    def mark_all_to_move(self, cards):
        for card in cards:
            if card:
                card.has_move = True
        return cards

    def get_ai_turn(self, player):
        player.kept_hand = self.mark_all_to_move(player.kept_hand)
        self.enemy_on_table = self.mark_all_to_move(self.enemy_on_table)

        if len(self.enemy_on_table) <= 1:
            if len(player.kept_hand):
                obj.has_move = False
                player.kept_hand.rem_card(obj)
                self.enemy_on_table.add_card(obj)
                CardLib.gui.redraw()    
                time.sleep(0.5)
            else:
                player.kept_hand.add_card(self.deal_new_card())
                return False

        if player.kept_hand.spots_left() > 1:
            player.kept_hand.add_card(self.deal_new_card())
            return False

        if player.kept_hand.spots_left() < 2 and self.enemy_on_table.spots_left():
            cards = [card for card in player.kept_hand if card]
            obj = cards[randint(0, len(cards) - 1)]
            obj.has_move = False
            player.kept_hand.rem_card(obj)
            self.enemy_on_table.add_card(obj)
            CardLib.gui.redraw()
            time.sleep(0.5)

        else:
            attackers = [card for card in self.enemy_on_table if card and card.has_move]
            attacker = attackers[randint(0, len(attackers))]


            defenders = [card for card in self.player_on_table if card and card.has_move]

            if len(defenders):
                attacker.gui_obj.has_highlight = True
                defender = CardLib.gui.get_gui_user_input(defenders)
                if defender.take_damage(attacker.damage):
                    attacker.gui_obj.has_highlight = False
                    self.player_on_table.rem_card(defender)
                attacker.gui_obj.has_highlight = False
                defender.has_move = False
            else:
                attacker.has_move = False
                return True

            attacker.has_move = False

        attackers = [card for card in self.enemy_on_table if card and card.has_move]
        if len(attackers):
            attacker = attackers[randint(0, len(attackers) - 1)]

            defenders = [card for card in self.player_on_table if card and card.has_move]

            if len(defenders):
                attacker.gui_obj.has_highlight = True
                defender = CardLib.gui.get_gui_user_input(defenders)
                if defender.take_damage(attacker.damage):
                    attacker.gui_obj.has_highlight = False
                    self.player_on_table.rem_card(defender)
                attacker.gui_obj.has_highlight = False
                defender.has_move = False
            else:
                attacker.has_move = False
                return True

            attacker.has_move = False
        CardLib.gui.redraw()
        return False

    def get_user_turn(self, player):
        player.kept_hand = self.mark_all_to_move(player.kept_hand)
        self.player_on_table = self.mark_all_to_move(self.player_on_table)

        has_ended = False
        while not has_ended:

            selectable = [self.player_end]

            if player.kept_hand.spots_left():
                selectable += [self.player_draw]

            if self.player_on_table.spots_left():
                selectable += [card for card in player.kept_hand if card and card.has_move]

            selectable += [card for card in self.player_on_table if card and card.has_move]

            obj = CardLib.gui.get_gui_user_input(selectable)

            if obj is self.player_end:
                has_ended = True

            elif obj is self.player_draw:
                player.kept_hand.add_card(self.deal_new_card())
                has_ended = True

            elif obj in player.kept_hand:
                #card that needs to be put onto the table
                obj.has_move = False
                player.kept_hand.rem_card(obj)
                self.player_on_table.add_card(obj)

            else:
                #obj = card on table
                defenders = [card for card in self.enemy_on_table if card and card.has_move]
                if len(defenders):
                    defender = defenders[randint(0, len(defenders) - 1)]
                    if defender.take_damage(obj.damage):
                        self.enemy_on_table.rem_card(defender)
                    defender.has_move = False
                    CardLib.gui.redraw()
                else:
                    obj.has_move = False
                    return True #remove one health from the enemy

                obj.has_move = False

        #NEEDS TO BE DONE
        #function to run if the player is a user
        return False

    def on_player_turn(self, player):
        if player.is_ai:
            was_attacked = self.get_ai_turn(player)
        else:
            was_attacked = self.get_user_turn(player)

        return was_attacked

def play_again(winner_label):
    play_again_prompt = CardLib.gui.GuiLabel("Do you want to play again?", x=270, y=260)
    yes = CardLib.gui.GuiButton(" yes ", x=340, y=400)
    no = CardLib.gui.GuiButton(" no ", x=500, y=400)

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
        player_list = game.deal_to_players(player_list)

        current_player = 0

        playing_round = True

        skip_count = 0
        while playing_round:
            player = player_list[current_player]
            CardLib.gui.redraw()

            attack_other = game.on_player_turn(player)
            other_died = False

            if attack_other:
                other_player = player_list[(current_player + 1) % len(player_list)]
                other_died = other_player.hurt()

            if other_died:
                CardLib.gui.redraw()
                playing_round = False
                won_label = CardLib.gui.GuiLabel(player.label + " has won!", x=340, y=180)

                game.on_round_won(player_list)
                
            else:
                current_player = (current_player + 1) % len(player_list)
                CardLib.gui.redraw()
                time.sleep(0.5)


        CardLib.gui.redraw()
        for player in player_list:
                player.clear_hand()

        playing = play_again(won_label)
    print("Thank you for playing!")


def start_game():
    CardLib.gui.start_gui("DeckDuel", 900, 700, background_color=(110, 160, 100))
    game = DeckDuel()

    print("Lets Battle!")
    print("------------")

    player_list = [DDPlayer("Player", x=110, y=540), DDPlayer("Enemy", is_ai=True, x=110, y=10)]

    main_loop(game, player_list)
