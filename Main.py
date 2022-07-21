from Card import Card
from Player import Player
from User_Input import getUserInput

#DEPRECIATED. THIS IS THE OLD WORK, AND WE ARE SWITCHING TO A NEW CLASS FORMAT

if __name__ == '__main__':
    #TODO: make the import of the game not hardcoded
    #ask what game to play
    from games import crazy8
    game = crazy8.crazy8()



    player_list = []
    player_list.append(game.getNewPlayer("Player"))

    for num in range(1, game.get_player_count()):
        player_list.append(game.getNewPlayer("AI #" +str(num), is_ai=True))


    playing = True
    while playing:    
        game.deal_to_players(player_list)

        game.start_game()

        current_player = 0

        playing_round = True

        while playing_round:
            player = player_list[current_player]

            played_card = player.play_card(game)
            if played_card is not None:
                game.on_card_played(played_card)


            if game.check_player_win(player):
                playing_round = False
                print(player.label, " has won!")

                game.on_round_won(player)
                for player in player_list:
                    player.clear_hand()
                
            else:
                current_player = (current_player+1) % 4

        if game.get_max_round() < game.get_current_round():
            action, _ = getUserInput(["yes", "y", "no", "n"], "Do you want to play again?")
            if action in ["yes", "y"]:
                game.reset_game()
            else:
                playing = False




    print("Thank you for playing!")