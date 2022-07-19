from Card import Card
from Card_List import Card_List


def game_testing():
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

def card_testing():
    card_list = Card_List([])
    card_list.set_52()
    print(card_list)
    card_list.set_54()
    print(card_list)
    card_list.shuffle()
    print(card_list)
    card = Card(0, 0)
    card_list.rem_card(card)
    print(card_list)
    cards = Card_List([Card(3, x) for x in range(13)])
    card_list.rem_cards(cards)
    print(card_list)
    print(len(card_list), card_list.num_cards_left())
    cards = card_list.get_card_list()
    print(cards)




if __name__ == '__main__':
    game_testing()
