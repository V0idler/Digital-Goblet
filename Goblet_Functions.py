
from Gobelt_Classes import *
import os
import pickle

full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'autosave.pkl')

#Prints text explaining the function of the program
def print_program_instructions():
    print('Welcome to Goblet!')
    print('Valid pick up locations: ')
    print('Player board: a b c')
    print('Gameboard: coordinates 00 to 33 as colum then row')
    print('Game autosaves after each turn.')

#Collects input for what the starting player color is and applies it
def select_start_player(player_light, player_dark):
    
    while True:
            player_start = (input('Who starts the game? (l/d) ')).lower()

            #If light was selected, current player is light
            if player_start == 'l':
                current_player = player_light
                return current_player

            #If dark was selected, current player is dark
            elif player_start == 'd':
                current_player = player_dark
                return current_player

            print('Unvalid player selection, please try again.')

#Prints the current state of the gameboard with reference coordinates
def print_game_board(game_board):
    print('Gameboard: ')
    print('   0  1  2  3 ')
    for col in range(4):
        print(f'{col} ', end='')
        for row in range(4):
            print(game_board.check_top_piece(row, col), end="")
        print(" ")

#Prints the current state of the player board of passed in player
def print_player_board(player_board):
    print('Player Board: ', end="")
    for stack_num in range(3):
        print(player_board.check_top_piece(stack_num), end="")
        print(" ", end="")
    print(" ")

#Saves the current game state by overwriting the previous save
def save_game(full_path, game_board, player_light, player_dark, current_player):

    #Opens the save file, assigns current player id to a string based on who the current player is, 
    # saves the game data as a dictionary using pickle, closes file automatically using 'with'
    with open(full_path, 'wb') as file_save:
        if current_player == player_light:
            current_player_id = 'player_light'
        elif current_player == player_dark:
            current_player_id = 'player_dark'

        pickle.dump({
            'game_board': game_board,
            'player_light': player_light,
            'player_dark': player_dark,
            'current_player_id': current_player_id
        }, file_save)

#Loads file containing game state from previous game
def load_game(full_path):

    #Opens the file, extracts data using pickle, restores current player to a player based on who the current player was during the save,
    # returns all loaded game objects, closes file using 'with'
    with open(full_path, 'rb') as file_load:
        game_data = pickle.load(file_load)

        if game_data['current_player_id'] == 'player_light':
            current_player = game_data['player_light']
        elif game_data['current_player_id'] == 'player_dark':
            current_player = game_data['player_dark']
    
    return game_data['game_board'], game_data['player_light'], game_data['player_dark'], current_player

#Loops collecting input from player for location of picking up a piece until input is confirmed to be a valid pickup location
def user_interface_pick(current_player):

    which_board = 0

    current_player_print = current_player.color.name.capitalize()

    while True:
        pick_up = input(f"Pick up piece {current_player_print}: ").strip().lower()

        #If input is coordinates, makes sure that they are within valid range before returning
        if len(pick_up) == 2 and pick_up.isdigit():
            which_board = 0
            row_up, col_up = map(int, pick_up)
            if 0 <= row_up <=3 and 0 <= col_up <= 3:
                return which_board, row_up, col_up

        #If input is a letter, makes that that it is within valid ascii range before returning
        elif len(pick_up) == 1:
            
            letter_val = ord(pick_up)

            if 97 <= letter_val <= 99:
                which_board = 1
                row_up = ord(pick_up) - 97
                col_up = 0

                return which_board, row_up, col_up

        print('Unvalid pick up location, please try again.')

#Loops collecting input from player for location of putting down a piece until input is confirmed to be a valid put down location
def user_interface_put(current_player):
    
    current_player_print = current_player.color.name.capitalize()

    while True:
        put_down = input(f"Put down piece {current_player_print}: ").strip()

        #Confirms that input is coordinates and it is within the valid range before returning
        if len(put_down) == 2 and put_down.isdigit():
            row_down, col_down = map(int, put_down)

            if 0 <= row_down <=3 and 0 <= col_down <= 3:
                return row_down, col_down

        print('Unvalid put down location, please try again')

#Once pick up location is confirmed to be valid, loops until the check that the piece at that location is valid
def player_pick(game_board, current_player):

    game_piece = None

    while game_piece is None:

        which_board, row_up, col_up = user_interface_pick(current_player)

        if which_board == 0:

            top_piece = game_board.check_top_piece(row_up, col_up)

            #If there is no valid piece on the game board, try again
            if top_piece is None:
                print('You cannot pick up there, try again.')
                continue

            #If the piece color does not match current player color, try again
            if top_piece.color != current_player.color:
                print('You can only pick up your own piece, please try again.')
                continue

            game_piece = game_board.get_piece(row_up, col_up)

        elif which_board == 1:

            #If there is no piece on the player board, try again
            player_game_piece = current_player.get_piece(row_up)
            if player_game_piece is None:
                print('You cannot pick up there, try again.')
                continue

            game_piece = player_game_piece
        
        else:
            print('Unvalid selection, please try again.')

        return game_piece

#Once put down location is confirmed to be valid, loops until the check that the piece at that location is valid
def player_put(game_piece, game_board, current_player):

    while True:
        row_down, col_down = user_interface_put(current_player)

        board_piece = game_board.check_top_piece(row_down, col_down).size

        #Only allows the piece to be put down if the piece at that location already is smaller than the picked up piece
        if game_piece.size > board_piece:
            game_board.put_piece(row_down, col_down, game_piece)
            break
        else:
            print('You cannot place there, try again.')

#Checks if there are 4 pieces of the same color in the rows, colums, and diagonals, if yes then returns True and who won
def check_win(game_board):
            
    #Checks wins in rows
    for row in range(4):
        first_piece = game_board.check_top_piece(row, 0)
        if first_piece:
            if all(game_board.check_top_piece(row, col).color == first_piece.color for col in range(4)):
                return True, first_piece.color.name
    
    #Check wins in colums
    for col in range(4):
        first_piece = game_board.check_top_piece(0, col)
        if first_piece:
            if all(game_board.check_top_piece(row, col).color == first_piece.color for row in range(4)):
                return True, first_piece.color.name
    
    #Checks win on top-left to bottom-right diagonal
    first_piece = game_board.check_top_piece(0, 0)
    if first_piece:
        if all(game_board.check_top_piece(i, i).color == first_piece.color for i in range(4)):
            return True, first_piece.color.name
    
    #Checks win on top-right to bottom-left diagonal
    first_piece = game_board.check_top_piece(0, 3)
    if first_piece:
        if all(game_board.check_top_piece(i, 3 - i).color == first_piece.color for i in range(4)):
            return True, first_piece.color.name
    
    return False, None

#Checks if a player won, if yes prints game_board (to see 4 in a row), game over, who the winner is, and returns True
def detect_win(game_board):

    if_win, winner_color = check_win(game_board)

    if if_win:
        print_game_board(game_board)
        print('Game Over!')
        print(f'The winner is: {(winner_color).capitalize()}!')
        
        return True