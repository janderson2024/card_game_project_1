if __name__ == '__main__':
    #TODO: make the import of the game not hardcoded
    #ask what game to play
    from games import crazy8

    game = crazy8.crazy8()

    player_list = []

    for num in range(4):
        player_list.append(game.getNewPlayer(str(num)))

    #print(game.stock)
    #print(player_list[0])

    game.deal_to_players(game.stock, player_list)
    print("shuffle and deal to players: ")

    print(game.stock)
    for player in player_list:
        print(player)