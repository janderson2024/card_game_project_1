import importlib
import os
import sys

GAMES_FOLDER = "games/"

def get_all_game_files() -> [str]:
    files_in_games = os.listdir(GAMES_FOLDER)
    games = [file[:-3] for file in files_in_games if file.endswith(".py")]
    return games

def play_games():
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



def create_game(game_name):
    with open(GAMES_FOLDER + str(game_name) + ".py", "w") as file:
        with open("CardLib/example_game.py", "r") as example_game:
            for line in example_game:
                line = line.replace("{GAME_NAME}", str(game_name))

                file.write(line)
    
    print("Created the ", game_name, "in the games/ folder")


args = sys.argv[1:]

if len(args) == 0:
    play_games()
elif len(args) == 2 and args[0] == "--create-new-game":
    create_game(args[1])
else:
    print("improper argument.")
    print("Arguements: --create-new-game [GAME NAME]")