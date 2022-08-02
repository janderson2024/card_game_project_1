import CardLib
from CardLib import Card

# CODE TO GO BACK UP A LAYER TO USE CARDLIB
import sys

sys.path.insert(0, '..')

if __name__ == '__main__':
    # Card List
    card_list = CardLib.CardList([])
    card_list = CardLib.fill_deck_standard_52(card_list, False)
    print(card_list)
    card_list = CardLib.fill_deck_standard_54(card_list, True)
    print(card_list)
    card_list.shuffle()
    print(card_list)
    card = Card(1, 2)
    card_list.rem_card(card)
    print(card_list)
    card_list.rem_cards([Card(3, x) for x in range(2, 15)])
    print(card_list)
    print(len(card_list), card_list.num_cards_left())
    cards = CardLib.CardList([])
    cards.add_cards(card_list.get_card_list())
    print(cards)

    # Draw and Hand
    draw = CardLib.Draw([])
    draw = CardLib.fill_deck_standard_52(draw, True)
    hand = CardLib.Hand([])
    hand.add_card(draw.pop_card())
    hand.add_card(draw.pop_card())
    hand.add_card(draw.pop_card())
    hand.add_card(draw.pop_card())
    hand.add_card(draw.pop_card())
    print(hand)
    hand.sort_by_suit()
    print(hand)
    hand.sort_by_rank()
    print(hand)

    # Discard
    discard = CardLib.Discard([])
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

    # Mutable test.
    a = CardLib.CardList()
    a.add_card(Card(1, 1))
    print(a)
    b = CardLib.CardList()
    print(b)
