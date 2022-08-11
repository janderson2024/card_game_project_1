from .defaults import *

from .Card import Card

from .cardlists.CardList import CardList
from .cardlists.Hand import Hand
from .cardlists.Draw import Draw
from .cardlists.Discard import Discard

from .Player import Player
from .UserInput import get_user_input
from .CalcAllScores import calculate_all_possible_scores

__all__ = [
    "Card",
    "CardList",
    "Hand",
    "Draw",
    "Discard",
    "Player",
    "get_user_input",
    "calculate_all_possible_scores",
    "deal_to_players",
    "change_rank_list",
    "change_suit_list",
    "fill_deck",
    "get_highest_card"
]
#MAYBE add defaults to this all list


def deal_to_players(cards, players, deal_count):
    for _ in range(deal_count):
        for player in players:
            player.add_card_to_hand(cards.pop_card())
    return (cards, players)


def change_rank_list(rank_list):
    global RANKS
    RANKS = rank_list

def change_suit_list(suit_list):
    global SUITS
    SUITS = suit_list

    global SUIT_TEXT
    SUIT_TEXT = [suit_to_text(suit) for suit in suit_list]

def fill_deck(deck):
    for suit in range(len(SUITS)):
        for rank in range(len(RANKS)):
            deck.add_card(Card(suit, rank))
    return deck

def get_highest_card(card_list: CardList):
    return max(card_list)
