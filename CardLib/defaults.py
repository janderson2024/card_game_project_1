DIAMOND = '\u2666'
HEART = '\u2665'
CLUB = '\u2663'
SPADE = '\u2660'

JOKER = '*'


SUITS = [DIAMOND, HEART, CLUB, SPADE, JOKER]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "L", "H"]
SUIT_TEXT = ["Diamonds", "Hearts", "Clubs", "Spades", "Joker"]


STANDARD_52_SUITS = [DIAMOND, HEART, CLUB, SPADE]
STANDARD_52_RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
STANDARD_52_ACE_HIGH = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

STANDARD_54_SUITS = STANDARD_52_SUITS + [JOKER]
STANDARD_54_RANKS = STANDARD_52_RANKS + ["L", "H"]
STANDARD_54_ACE_HIGH = STANDARD_52_ACE_HIGH + ["L", "H"]


def rank_to_text(rank):
	if rank == "A":
		return "Ace"
	if rank == "K":
		return "King"
	if rank == "Q":
		return "Queen"
	if rank == "J":
		return "Jack"
	return rank
	#maybe expand in the future to include 2-10 and jokers?

def suit_to_text(suit):
	if suit == DIAMOND:
		return "Diamonds"
	if suit == HEART:
		return "Hearts"
	if suit == CLUB:
		return "Clubs"
	if suit == SPADE:
		return "Spades"
	if suit == JOKER:
		return "Joker"
	return "UNKNOWN"

