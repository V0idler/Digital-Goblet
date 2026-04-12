
from Gobelt_Classes import *
from Goblet_Functions import *

print_program_instructions()

while True:

    saved_game = input('Load saved game? (y/n) ').lower()

    if saved_game == 'y':
        game_board, player_light, player_dark, current_player = load_game(full_path)
        print('Loading saved game.')
        break

    elif saved_game == 'n':
        print('Initializing new game.')
        
        player_light = player_board_class(player_color_class.light)
        player_dark = player_board_class(player_color_class.dark)

        game_board = game_board_class()

        current_player = select_start_player(player_light, player_dark)
        break

while True:

    print_game_board(game_board)
    print_player_board(player_light)
    print_player_board(player_dark)

    game_piece = player_pick(game_board, current_player)
    
    player_put(game_piece, game_board, current_player)

    current_player = player_dark if current_player == player_light else player_light

    save_game(full_path, game_board, player_light, player_dark, current_player)

    if detect_win(game_board):
        break

    

