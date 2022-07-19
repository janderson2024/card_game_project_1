from Card import Card
from Player import Player

def game_testing(game, player_list):
    print(game.discard)

    test_card = Card(1, 8, displayable=True)
    print(test_card)

    print("is card valid: ", game.is_card_valid(test_card))

    game.on_card_played(test_card)

    print(game.discard)

    print("------")
    print(player_list[0])

    print(game.check_player_win(player_list[0]))

    player_list[0].reset_hand()
    print(player_list[0])
    print(game.check_player_win(player_list[0]))
    game.on_round_won(player_list[0])

    print(player_list[0].win_count)


if __name__ == '__main__':
    #TODO: make the import of the game not hardcoded
    #ask what game to play
    from games import crazy8
    game = crazy8.crazy8()



    player_list = []

    for num in range(4):
        player_list.append(game.getNewPlayer(str(num)))


    game.deal_to_players(player_list)
    print("shuffle and deal to players: ")

    print(game.stock)
    for player in player_list:
        print(player)

    game.start_game()

    game_testing(game, player_list)
    