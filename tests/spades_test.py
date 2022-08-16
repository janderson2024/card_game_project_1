import unittest
from decimal import *

import CardLib
import games.Spades

# Something

class TestSpadesAI(unittest.TestCase):
    def setUp(self) -> None:
        self.test = games.Spades.Spades()
        self.test.player_count = 6
        self.test.pot = CardLib.CardList([CardLib.Card(3, 3), CardLib.Card(3, 10), CardLib.Card(3, 9)])
        self.test.discard = CardLib.Discard([CardLib.Card(2, 14), CardLib.Card(2, 8), CardLib.Card(2, 7),
                                             CardLib.Card(2, 3), CardLib.Card(2, 10), CardLib.Card(2, 4)])

    def test_get_ratio(self):
        card = CardLib.Card(3, 14)
        cards = CardLib.Hand([CardLib.Card(4, 16), CardLib.Card(4, 15), CardLib.Card(4, 14), CardLib.Card(4, 13),
                              CardLib.Card(4, 12), CardLib.Card(4, 11), CardLib.Card(4, 10), CardLib.Card(4, 9),
                              CardLib.Card(4, 8), CardLib.Card(4, 7), CardLib.Card(4, 6), CardLib.Card(4, 4),
                              CardLib.Card(3, 13), CardLib.Card(3, 12), CardLib.Card(3, 8), CardLib.Card(3, 7),
                              CardLib.Card(3, 6), CardLib.Card(3, 5), CardLib.Card(3, 4), CardLib.Card(3, 2)])
        card_to_beat = CardLib.Card(3, 10)
        self.assertEqual(games.Spades.Spades.get_ratio(self.test, card, cards, card_to_beat), Decimal('0.4'))

    def test_winning_ratios_1(self):
        # Both valid cards are better than the card to beat.
        card_to_beat = CardLib.Card(3, 10)
        valid_plays = CardLib.CardList([CardLib.Card(3, 14), CardLib.Card(3, 11)])
        hand = CardLib.Hand([CardLib.Card(4, 5), CardLib.Card(4, 3), CardLib.Card(4, 2), CardLib.Card(3, 14),
                             CardLib.Card(3, 11), CardLib.Card(2, 11), CardLib.Card(2, 5), CardLib.Card(1, 2)])
        self.assertEqual(games.Spades.Spades.winning_ratios(self.test, card_to_beat, valid_plays, hand), [0.16, 0.09])

    def test_winning_ratios_2(self):
        # One valid card is better than the card to beat.
        card_to_beat = CardLib.Card(3, 10)
        valid_plays = CardLib.CardList([CardLib.Card(3, 12), CardLib.Card(3, 8)])
        hand = CardLib.Hand([CardLib.Card(4, 5), CardLib.Card(4, 3), CardLib.Card(4, 2), CardLib.Card(3, 12),
                             CardLib.Card(3, 8), CardLib.Card(2, 11), CardLib.Card(2, 5), CardLib.Card(1, 2)])
        self.assertEqual(games.Spades.Spades.winning_ratios(self.test, card_to_beat, valid_plays, hand), [0.09, 0.0])

    def test_winning_ratios_3(self):
        # Both valid cards are worse than the card to beat.
        card_to_beat = CardLib.Card(3, 10)
        valid_plays = CardLib.CardList([CardLib.Card(3, 7), CardLib.Card(3, 2)])
        hand = CardLib.Hand([CardLib.Card(4, 5), CardLib.Card(4, 3), CardLib.Card(4, 2), CardLib.Card(3, 7),
                             CardLib.Card(3, 2), CardLib.Card(2, 11), CardLib.Card(2, 5), CardLib.Card(1, 2)])
        self.assertEqual(games.Spades.Spades.winning_ratios(self.test, card_to_beat, valid_plays, hand), [0.0, 0.0])

    def test_winning_ratios_4(self):
        # Valid cards don't match suit of card to beat. Spades will trump.
        card_to_beat = CardLib.Card(3, 10)
        valid_plays = CardLib.CardList([CardLib.Card(4, 5), CardLib.Card(4, 3), CardLib.Card(4, 2), CardLib.Card(2, 12),
                                        CardLib.Card(2, 11), CardLib.Card(2, 5), CardLib.Card(1, 10), CardLib.Card(1, 2)])
        hand = CardLib.Hand([CardLib.Card(4, 5), CardLib.Card(4, 3), CardLib.Card(4, 2), CardLib.Card(2, 12),
                             CardLib.Card(2, 11), CardLib.Card(2, 5), CardLib.Card(1, 10), CardLib.Card(1, 2)])
        self.assertEqual(games.Spades.Spades.winning_ratios(self.test, card_to_beat, valid_plays, hand),
                         [0.25, 0.2066115702479339, 0.2066115702479339, 0.0, 0.0, 0.0, 0.0, 0.0])

    def test_winning_ratios_5(self):
        # No cards have been played so there is no card to beat. Spades have not been broken.
        card_to_beat = None
        self.test.pot = CardLib.CardList()
        valid_plays = CardLib.CardList([CardLib.Card(2, 12), CardLib.Card(2, 11), CardLib.Card(2, 5),
                                        CardLib.Card(1, 10), CardLib.Card(1, 2)])
        hand = CardLib.Hand([CardLib.Card(4, 5), CardLib.Card(4, 3), CardLib.Card(4, 2), CardLib.Card(2, 12),
                             CardLib.Card(2, 11), CardLib.Card(2, 5), CardLib.Card(1, 10), CardLib.Card(1, 2)])
        self.assertEqual(games.Spades.Spades.winning_ratios(self.test, card_to_beat, valid_plays, hand),
                         [0.881095693359375, 0.881095693359375, 0.677187080078125, 0.59049, 0.200304189453125])

    def test_winning_ratios_6(self):
        # Last card to play so both cards should be equal as they both win
        card_to_beat = CardLib.Card(3, 10)
        self.test.pot = CardLib.CardList([CardLib.Card(3, 3), CardLib.Card(3, 10), CardLib.Card(3, 9),
                                          CardLib.Card(3, 7), CardLib.Card(3, 8)])
        valid_plays = CardLib.CardList([CardLib.Card(3, 14), CardLib.Card(3, 11)])
        hand = CardLib.Hand([CardLib.Card(4, 5), CardLib.Card(4, 3), CardLib.Card(4, 2), CardLib.Card(3, 14),
                             CardLib.Card(3, 11), CardLib.Card(2, 11), CardLib.Card(2, 5), CardLib.Card(1, 2)])
        self.assertEqual(games.Spades.Spades.winning_ratios(self.test, card_to_beat, valid_plays, hand), [1.0, 1.0])

    def test_get_choice_1(self):
        # Last turn to play, should pick the lowest card as they both win
        valid_plays = CardLib.CardList([CardLib.Card(3, 14), CardLib.Card(3, 11)])
        ratios = [1.0, 1.0]
        self.assertEqual(games.Spades.Spades.get_choice(self.test, valid_plays, ratios), CardLib.Card(3, 11))

    def test_get_choice_2(self):
        # Last turn to play, should pick the lowest card as they both lose
        valid_plays = CardLib.CardList([CardLib.Card(3, 7), CardLib.Card(3, 2)])
        ratios = [0.0, 0.0]
        self.assertEqual(games.Spades.Spades.get_choice(self.test, valid_plays, ratios), CardLib.Card(3, 2))

    def test_get_choice_3(self):
        # Last turn to play, should pick the lowest winning card as two win and two lose
        valid_plays = CardLib.CardList([CardLib.Card(3, 14), CardLib.Card(3, 11), CardLib.Card(3, 7), CardLib.Card(3, 2)])
        ratios = [1.0, 1.0, 0.0, 0.0]
        self.assertEqual(games.Spades.Spades.get_choice(self.test, valid_plays, ratios), CardLib.Card(3, 11))
