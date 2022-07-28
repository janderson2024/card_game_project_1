def get_user_input(possible_inputs, start_prompt):
	possible_inputs = [str(input) for input in possible_inputs]
	help_response = "Valid Inputs are: " + str(possible_inputs)

	
	print(start_prompt)
	print(help_response)

	valid_input = False

	while not valid_input:
		user_input = input(">>")
		user_input.lower()
		user_input = user_input.split()

		if len(user_input) > 0:
			cmd = user_input[0]
			arguments = user_input[1:]

			if cmd == "help":
				print(help_response)
			elif cmd in possible_inputs:
				if len(arguments) == 0:
					valid_input = True
					return (cmd, None)
				valid_input = True
				return (cmd, arguments[0])

if __name__ == "__main__":

	##EXAMPLE CODE ON HOW THIS WOULD BE USED
	#getUserInput([list of choices as strings], string prompt for the user)
	#automatic "help" command is checked to print out all possible actions

	#currently this will only return the command picked
	#and the first argument passed (or None) as a tuple

	#ex: ("play", None)
	#ex: ("draw", 1)


	player_hand = ["[1c]", "[4p]", "[10s]"]

	#if you need the possible arguement
	action, card_num = get_user_input(["play", "hand", "draw", "exit"], "Your Turn to play")

	if action == "play":
		possible_card_nums = [str(num) for num in range(1, len(player_hand)+1)]
		if card_num is None or card_num not in possible_card_nums:

			#if you dont care and only want that command
			card_num, _ = get_user_input(possible_card_nums, "Pick a card num to play")

	
	print(action, "  ", card_num)
