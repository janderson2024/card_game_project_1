# CODE TO GO BACK UP A LAYER TO USE CARDLIB
import sys

sys.path.insert(0, '..')

import CardLib


CardLib.change_suit_list([CardLib.SPADE, CardLib.DIAMOND, CardLib.CLUB, CardLib.HEART])
CardLib.change_rank_list(CardLib.STANDARD_52_RANKS)

print(CardLib.fill_deck(CardLib.CardList()))
print(CardLib.SUIT_TEXT)
