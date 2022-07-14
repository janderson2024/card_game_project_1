from Card import Card
from Card_List import Card_List

if __name__ == '__main__':
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

