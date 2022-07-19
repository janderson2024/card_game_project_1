from abc import ABC, abstractmethod
from Player import Player

class Game(ABC):


	def getNewPlayer(self, player_label):
		#method that can be polymorphized by the game if the game has a different type of player
		return Player(player_label)

	@abstractmethod
	def start_game(self):
		#used for beginning game logic before the first card is played, but after the cards are dealt
		#Ex: flipping the first card into the discard
		#to be implemented by each game
		pass	

	@abstractmethod
	def deal_to_players(self, players):
		#used for each game to deal cards to the players
		#to be implemented by each game
		pass


	@abstractmethod
	def is_card_valid(self, card):
		#return either true or false based on the rules of the game
		#to be implemented by each game
		pass

	@abstractmethod
	def on_card_played(self, card):
		pass

	@abstractmethod
	def check_player_win(self, player):
		#return either true or false based on if the player wins
		#to be implemented by each game
		pass

	@abstractmethod
	def on_round_won(self, player):
		#logic here will be run after a round is won. Useful to "reset" the
		#cards after the end of the round, or to check win logic for a round based game
		pass