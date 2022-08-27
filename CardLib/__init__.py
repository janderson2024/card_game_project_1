from .Card import Card

from .cardlists.CardList import CardList
from .cardlists.Hand import Hand
from .cardlists.DrawPile import DrawPile
from .cardlists.Discard import Discard

from .Player import Player
from .UserInput import get_user_input
from .CalcAllScores import calculate_all_possible_scores

from . import gui

__all__ = [
    "DIAMOND",
    "HEART",
    "CLUB",
    "SPADE",
    "JOKER",
    "Card",
    "CardList",
    "Hand",
    "DrawPile",
    "Discard",
    "Player",
    "get_user_input",
    "calculate_all_possible_scores",
    "print_test",
    "deal_to_players",
    "fill_deck_standard_52",
    "fill_deck_standard_54",
    "get_highest_card",
    "gui"
]


DIAMOND = '\u2666'
HEART = '\u2665'
CLUB = '\u2663'
SPADE = '\u2660'

JOKER = '*'
CARD_WIDTH = 70


def print_test():
    print("Hello World")


def deal_to_players(cards, players, deal_count):
    for _ in range(deal_count):
        for player in players:
            player.add_card_to_hand(cards.pop_card())
    return (cards, players)


def fill_deck_standard_52(deck, ace_high=False):
    rank_start, rank_end = 1, 14
    if ace_high:
        rank_start += 1
        rank_end += 1

    for suit in range(1, 5):
        for rank in range(rank_start, rank_end):
            deck.add_card(Card(suit, rank))
    return deck


def fill_deck_standard_54(deck, ace_high=False):
    deck = fill_deck_standard_52(deck, ace_high)
    deck.add_card(Card(0, 15))
    deck.add_card(Card(0, 16))
    return deck


def get_highest_card(card_list: CardList):
    return max(card_list)
