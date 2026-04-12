
from Gobelt_Classes import *
import os
import pickle

full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'autosave.pkl')
pick_int = False

def program_instructions():
    print('Welcome to Goblet!')
    print('Valid pick up locations: ')
    print('Player board White: a b c')
    print('Player board Black: x y z')
    print('Gameboard: coordinates 00 to 33')
    print('Game autosaves after each turn.')

def print_board(game_board_in):
    print('Gameboard: ')
    for col in range(4):
        for row in range(4):
            print(game_board_in.look_at_game_board(row, col), end="")
            print(" ", end="")
        print(" ")

def print_player_board(board):
    print('Player Board: ', end="")
    for stack_num in range(3):
        print(board.look_at_player_board(stack_num), end="")
        print(" ", end="")
    print(" ")

def user_interface_pick(current_player):

    which_board = 0

    while True:
        pick_up = input("Pick up piece: ").strip()

        if len(pick_up) == 2 and pick_up.isdigit():
            which_board = 0
            row_up, col_up = map(int, pick_up)
            if 0 <= row_up <=3 and 0 <= col_up <= 3:
                return which_board, row_up, col_up

        elif len(pick_up) == 1:
            
            letter_val = ord(pick_up)

            if 97 <= letter_val <= 99:
                which_board = 1
                row_up = ord(pick_up) - 97
                col_up = 0

                return which_board, row_up, col_up

        print('Unvalid pick up location, please try again.')

def user_interface_put():
    
    while True:
        put_down = input("Put down piece: ").strip()

        if len(put_down) == 2 and put_down.isdigit():
            row_down, col_down = map(int, put_down)

            if 0 <= row_down <=3 and 0 <= col_down <= 3:
                return row_down, col_down

        print('Unvalid put down location, please try again')

def check_win(game_board):
            
    for row in range(4):
        first_piece = game_board.top_piece(row, 0)
        if first_piece.color != player_color_class.initial:
            if all(game_board.top_piece(row, col).color == first_piece.color for col in range(4)):
                return True, first_piece.color.name
    
    for col in range(4):
        first_piece = game_board.top_piece(0, col)
        if first_piece.color != player_color_class.initial:
            if all(game_board.top_piece(row, col).color == first_piece.color for row in range(4)):
                return True, first_piece.color.name
    
    first_piece = game_board.top_piece(0, 0)
    if first_piece.color != player_color_class.initial:
        if all(game_board.top_piece(i, i).color == first_piece.color for i in range(4)):
            return True, first_piece.color.name
    
    first_piece = game_board.top_piece(3, 0)
    if first_piece.color != player_color_class.initial:
        if all(game_board.top_piece(3 - i, i).color == first_piece.color for i in range(4)):
            return True, first_piece.color.name
    
    return False, None

def save_game(full_path, game_board, player_white, player_black, current_player):

    with open(full_path, 'wb') as file_save:
        if current_player == player_white:
            current_player_id = 'player_white'
        else:
            current_player_id = 'player_black'

        pickle.dump({
            'game_board': game_board,
            'player_white': player_white,
            'player_black': player_black,
            'current_player_id': current_player_id
        }, file_save)

def load_game(full_path):

    with open(full_path, 'rb') as file_load:
        game_data = pickle.load(file_load)

        if game_data['current_player_id'] == 'player_white':
            current_player = game_data['player_white']
        else:
            current_player = game_data['player_black']
    
    return game_data['game_board'], game_data['player_white'], game_data['player_black'], current_player

def player_pick(game_board, current_player):
    while True:

        which_board, row_up, col_up = user_interface_pick(current_player)

        if which_board == 0:

            game_piece = game_board.get_piece(row_up, col_up)
            if game_piece is None:
                print('You cannot pick up there, try again.')
            return game_piece

        elif which_board == 1:

            game_piece = current_player.get_piece(row_up)
            if game_piece is None:
                print('You cannot pick up there, try again.')
            return game_piece
    
def player_put(game_piece, game_board):
    
    while True:
        row_down, col_down = user_interface_put()

        if game_piece.size > game_board.top_piece(row_down, col_down).size:
            game_board.put_piece(row_down, col_down, game_piece)
            break
        else:
            print('You cannot place there, try again.')

def detect_win(game_board):

    if_win, winner_color = check_win(game_board)

    if if_win:
        print_board(game_board)
        print('Game Over!')
        print(f'The winner is: {(winner_color).capitalize()}!')
        
        return True
    

def select_start_player(player_white, player_black):
    
    while True:
            player_start = (input('Who starts the game? (white/black) ')).lower()

            if player_start == 'white':
                current_player = player_white
                return current_player

            elif player_start == 'black':
                current_player = player_black
                return current_player

            print('Unvalid player color, please try again.')