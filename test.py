from Card import Card
from card_list.Card_List import Card_List
from card_list.Discard import Discard
from card_list.Draw import Draw
from card_list.Hand import Hand
from card_list.Pot import Pot

if __name__ == '__main__':
    # Card List
    card_list = Card_List([])
    card_list.set_52_lo()
    print(card_list)
    card_list.set_54_hi()
    print(card_list)
    card_list.shuffle()
    print(card_list)
    card = Card(1, 2)
    card_list.rem_card(card)
    print(card_list)
    cards = Card_List([Card(3, x) for x in range(2, 15)])
    card_list.rem_cards(cards)
    print(card_list)
    print(len(card_list), card_list.num_cards_left())
    cards = card_list.get_card_list()
    print(cards)

    # Pot
    pot = Pot([])
    pot.add_cards(card_list.get_card_list())
    print(pot)
    print(pot.get_highest_card())
    pot = Pot([Card(2, 13), Card(4, 12), Card(3, 14), Card(1, 14)])
    print(pot)
    print(pot.get_highest_card())

    # Draw and Hand
    draw = Draw([])
    draw.set_52_hi()
    hand = Hand([])
    hand.add_card(draw.pop_card())
    hand.add_card(draw.pop_card())
    hand.add_card(draw.pop_card())
    hand.add_card(draw.pop_card())
    hand.add_card(draw.pop_card())
    print(hand)
    hand.sort_suit()
    print(hand)
    hand.sort_rank()
    print(hand)

    # Discard
    discard = Discard([])
    discard.get_top_card()
    discard.add_card(draw.pop_card())
    print(discard.get_top_card())
    discard.add_card(draw.pop_card())
    print(discard.get_top_card())
    discard.add_card(draw.pop_card())
    print(discard.get_top_card())
    discard.add_card(draw.pop_card())
    print(discard.get_top_card())
    discard.add_card(draw.pop_card())
    print(discard)

