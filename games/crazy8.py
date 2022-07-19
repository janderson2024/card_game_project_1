import sys
sys.path.insert(0, '..')

from Game import Game
from card_list.Draw import Draw
from card_list.Discard import Discard

class crazy8(Game):
	DEAL_COUNT = 5

	round_counter = 1

	

	def __init__(self):
		self.stock = Draw([])
		self.stock.set_52_lo()
		self.stock.shuffle()
		self.discard = Discard([])

	def start_game(self):
		self.discard.add_card(self.stock.pop_card())
		pass

	def deal_to_players(self, players):
		for _ in range(self.DEAL_COUNT):
			for player in players:
				player.add_card(self.stock.pop_card())

	def is_card_valid(self, card):
		if card.rank is "8":
			return True

		top_card = self.discard.get_top_card()

		if card.suit == top_card.suit:
			return True
		if card.rank == top_card.rank:
			return True

		return False

	def on_card_played(self, card):
		self.discard.add_card(card)


	def check_player_win(self, player):
		if player.get_amount_of_cards() == 0:
			return True
		else:
			return False

	def on_round_won(self, player):
		player.round_winner()
		self.round_counter += 1
