import sys
sys.path.insert(0, '..')

from Game import Game
from card_list.Card_List import Card_List

class crazy8(Game):
	DEAL_COUNT = 5

	round_counter = 1
		

	def __init__(self):
		self.stock = Card_List([])
		self.stock.set_52()
		self.stock.shuffle()

	def deal_to_players(self, cards, players):
		for _ in range(self.DEAL_COUNT):
			for player in players:
				player.deck.append(cards.card_list.pop(0)) #TODO create a getTopCard and popTopCard

	def is_card_valid(self, card):
		return true

	def check_player_win(self, player):
		return false

	def on_round_won(self, player):
		self.round_counter += 1
