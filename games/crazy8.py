import CardLib
from random import randint

class Crazy8():
	DEAL_COUNT = 5
	PLAYER_COUNT = 4

	def __init__(self):
		self.setup_decks()

	def setup_decks(self):
		self.stock = CardLib.Draw([])
		self.stock = CardLib.fill_deck_standard_52(self.stock)
		self.stock.shuffle()

		self.discard = CardLib.Discard([])
		self.discard.add_card(self.stock.pop_card())


	def draw_card(self):
		if len(self.stock) > 0:
			return self.stock.pop_card()
		else:
			return None

	def is_card_valid(self, card):
		if card.rank == "8":
			return True

		top_card = self.discard.get_top_card()

		if card.suit == top_card.suit:
			return True
		if card.rank == top_card.rank:
			return True

		return False

	def check_player_win(self, player):
		if player.get_amount_of_cards() == 0:
			return True
		else:
			return False

	def on_round_won(self, player):
		player.round_winner()

		self.setup_decks()


	def on_card_played(self, card):
		self.discard.add_card(card)



def get_valid_cards(game, player):
	return player.hand.get_all_valid_cards(game.is_card_valid)


def get_AI_turn(game, player):
	valid_cards = get_valid_cards(game, player)
	while len(valid_cards) == 0:
		drew_card = game.draw_card()

		if drew_card is None:
			return None

		player.add_card_to_hand(drew_card)
		valid_cards = get_valid_cards(game, player)

	card_num = randint(0, len(valid_cards)-1)
	card_to_play = valid_cards.get_card_at(card_num)

	player.hand.rem_card(card_to_play)

	return card_to_play
    


def get_user_turn(game, player):
	valid_cards = get_valid_cards(game, player)
	print("--------------------")
	print("The last discard is: ", game.discard.get_top_card())

	played_valid = False
	while not played_valid:
		action, card_num = CardLib.get_user_input(["play", "hint", "draw", "skip", "end"], "Your Cards: " + str(player.hand))

		if action == "play":
			possible_card_nums = [str(num) for num in range(1, len(player.hand)+1)]

			if card_num is None or card_num not in possible_card_nums:
				card_num, _ = CardLib.get_user_input(possible_card_nums, "Pick a card num to play")

			picked_card = player.hand.get_card_at(int(card_num)-1)

			if valid_cards.is_card_in(picked_card):
				player.hand.rem_card(picked_card)
				played_valid = True
				return picked_card
			else:
				print("That card doesn't follow the game rules!")

		if action == "hint":
			if(len(valid_cards) > 0):
				print("Hint: you can play these: ", str(valid_cards))
			else:
				print("Hint: you need to draw")

		if action == "draw":
			drew_card = game.draw_card()

			if drew_card is None:
				print("The Draw pile is Empty! Cannot draw new card")
			else:
				player.add_card_to_hand(drew_card)
				valid_cards = get_valid_cards(game, player)

				print("Drew : ", drew_card)

		if action == "skip":
			played_valid = True
			return None

		if action  == "end":
			print("Thanks for playing!")
			exit()



def on_player_turn(game, player):
	if player.is_ai:
		played_card = get_AI_turn(game, player)
	else:
		played_card = get_user_turn(game, player)

	return played_card


def main_loop(game, player_list):
	playing = True
	while playing:    
		game.stock, player_list = CardLib.deal_to_players(game.stock, player_list, game.DEAL_COUNT)

		current_player = 0

		playing_round = True

		while playing_round:
			player = player_list[current_player]


			played_card = on_player_turn(game, player)


			if played_card is not None:
				game.on_card_played(played_card)
				print(player.label, " played: ", played_card)
			else:
				print(player.label, " skipped!")


			if game.check_player_win(player):
				playing_round = False
				print(player.label, " has won!")

				game.on_round_won(player)
				for player in player_list:
					player.clear_hand()

			else:
				current_player = (current_player+1) % 4


		action, _ = CardLib.get_user_input(["yes", "no"], "Do you want to play again?")
			
		if action in ["yes"]:
			playing_round = True
		else:
			playing = False

	print("Thank you for playing!")


def start_game():
	CardLib.print_test()


	game = Crazy8()
	print("Lets Play Crazy 8's!")


	player_list = []
	player_list.append(CardLib.Player("Player"))


	for num in range(1, game.PLAYER_COUNT):
		player_list.append(CardLib.Player("AI #" +str(num), is_ai=True))


	main_loop(game, player_list)