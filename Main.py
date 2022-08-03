import importlib
import os

GAMES_FOLDER = "games/"


def get_all_game_files() -> [str]:
    files_in_games = os.listdir(GAMES_FOLDER)
    games = [file[:-3] for file in files_in_games if file.endswith(".py")]
    return games


from CardLib import get_user_input

all_games = get_all_game_files() + ["exit"]

user_input, _ = get_user_input(all_games, "Please select which game you would like to play")

if user_input == "exit":
    exit()
else:
    module_to_import = "games." + user_input
    # module_to_import = "games.crazy8" FOR TESTING

    game = importlib.import_module(module_to_import)

    game.start_game()
