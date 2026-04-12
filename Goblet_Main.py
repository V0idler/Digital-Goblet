
from Gobelt_Classes import *
from Goblet_Functions import *

while True:
    if input('Load saved game? ').lower() == 'y':
        game_board, player_1, player_2 = load_game()
        print('Loading saved game.')
        break
    else:
        print('Initializing new game.')
        
        player_1 = player_board_class(player_color_class.white)
        player_2 = player_board_class(player_color_class.black)

        game_board = game_board_class()
        break

while True:
    print_board(game_board)
    print_player_board(player_1)
    print_player_board(player_2)

    game_piece = player_pick(game_board, player_1, player_2)
    
    player_put(game_piece)

    if_win, winner_color = check_win(game_board)

    if if_win:
        print_board(game_board)
        print('Game Over!')
        print(f'The winner is: {(winner_color).capitalize()}!')
        break

    save_game(game_board, player_1, player_2)

