
from Gobelt_Classes import *
from Goblet_Functions import *

program_instructions()

while True:

    saved_game = input('Load saved game? (y/n) ').lower()

    if saved_game == 'y':
        game_board, player_white, player_black, current_player = load_game(full_path)
        print('Loading saved game.')
        break

    elif saved_game == 'n':
        print('Initializing new game.')
        
        player_white = player_board_class(player_color_class.white)
        player_black = player_board_class(player_color_class.black)

        game_board = game_board_class()

        current_player = select_start_player(player_white, player_black)
        break

while True:
    
    print(f"{(current_player.color.name).capitalize()}'s turn.")
    
    print_board(game_board)
    print_player_board(player_white)
    print_player_board(player_black)

    game_piece = player_pick(game_board, current_player)
    
    player_put(game_piece, game_board)

    current_player = player_black if current_player == player_white else player_white

    save_game(full_path, game_board, player_white, player_black, current_player)

    if detect_win(game_board):
        break

    

