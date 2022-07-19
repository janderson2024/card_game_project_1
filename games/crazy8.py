import sys
sys.path.insert(0, '..')

from Game import Game
from card_list.Card_List import Draw, Discard

class crazy8(Game):
	DEAL_COUNT = 5

	round_counter = 1

	discard = Discard([])

	def __init__(self):
		self.stock = Draw([])
		self.stock.set_52_lo()
		self.stock.shuffle()

	def start_game(self):
		discard.add_card(stock.pop_card())
		pass

	def deal_to_players(self, players):
		for _ in range(self.DEAL_COUNT):
			for player in players:
				player.deck.append(stock.pop_card()) #TODO create a getTopCard and popTopCard

	def is_card_valid(self, card):
		if card.rank == 8:
			return True

		top_card = discard.get_top_card

		if card.suit == top_card.suit:
			return True
		if card.rank == top_card.rank:
			return True

		return True

	def on_card_played(self, card):
		discard.add_card(card)


	def check_player_win(self, player):
		if player.get_number_of_cards() == 0
			return True
		else:
			return False

	def on_round_won(self, player):
		player.round_winner()
		self.round_counter += 1
