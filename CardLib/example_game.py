### Author: Joshua Anderson
### Date: 8/17/22
### gitlab: gitlab.com/janderson2024
### Written for the CardLib library

import CardLib


class {GAME_NAME}:

    def __init__(self):
        #Init all of your game data here
        pass

    def get_ai_turn(self, player):
        #function to run if the player is an AI
        pass

    def get_user_turn(self, player):
        #function to run if the player is a user
        pass

    def on_player_turn(self, player):
        if player.is_ai:
            played_card = self.get_ai_turn(player)
        else:
            played_card = self.get_user_turn(player)

        return played_card


def main_loop(game, player_list):
    playing = True
    while playing:
        #Start of game code goes here

        #example loop of a simple "game loop"
        current_player = 0
        playing_round = True
        while playing_round:

            #gets the current Player object
            player = player_list[current_player]

            # code for each player's turn goes here
            
            #cycles to the next player
            current_player = (current_player + 1) % len(player_list)

        #asks the user to play the game again
        action, _ = CardLib.get_user_input(["yes", "no"], "Do you want to play again?")
        if action == "no":
            playing = False

    #only prints once the user is done playing
    print("Thank you for playing!")


def start_game():
    game = {GAME_NAME}()

    print("Lets play {GAME_NAME}!")
    print("--------------------")

    player_list = [CardLib.Player("Player")]

    PLAYER_COUNT = 4

    for num in range(1, game.PLAYER_COUNT):
        player_list.append(CardLib.Player("AI #" + str(num), is_ai=True))

    main_loop(game, player_list)
