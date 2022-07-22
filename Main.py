import importlib
import os

GAMES_FOLDER = "games/"

def get_all_game_files():
	files_in_games = os.listdir(GAMES_FOLDER)
	games = [file[:-3] for file in files_in_games if file.endswith(".py")]
	return games


from CardLib import get_user_input

all_games = get_all_game_files()

user_input, _ = get_user_input(all_games, "Please select which game you would like to play")

module_to_import = "games." + user_input
#module_to_import = "games.crazy8" FOR TESTING

game = importlib.import_module(module_to_import)

game.start_game()