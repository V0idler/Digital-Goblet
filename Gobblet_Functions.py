from Gobblet_Classes import *
import os
import pickle

#Prints text explaining the function of the program
def print_program_instructions():
    print('Welcome to Goblet!')
    print('Valid pick up locations: ')
    print('Player board: a b c')
    print('Gameboard: coordinates 00 to 33 as column then col')
    print('Game autosaves after each turn.')
    print('Player colors: light = purple, dark = green')

#Collects input for what the starting player color is and applies it
def select_start_player(player_light, player_dark):
   
    while True:
            player_start = (input('Who starts the game? (light/dark as l/d) ')).lower()

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
    for row in range(4):
        print(f'{row} ', end='')
        for col in range(4):
            print(game_board.check_top_piece(col, row), end="")
        print(" ")

#Prints the current state of the player board of passed in player
def print_player_board(player_board):
    print('Player Board: ', end="")
    for stack_num in range(3):
        print(player_board.check_top_piece(stack_num), end="")
        print(" ", end="")
    print(" ")

#Saves the current game state by overwriting the previous save
def save_game(game_board, player_light, player_dark, current_player):

    #Opens the save file, assigns current player id to a string based on who the current player is,
    # saves the game data as a dictionary using pickle, closes file automatically using 'with'
    with open('.autosave', 'wb') as file_save:
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
def load_game():

    #Opens the file, extracts data using pickle, restores current player to a player based on who the current player was during the save,
    # returns all loaded game objects, closes file using 'with'
    with open('.autosave', 'rb') as file_load:

        game_data = pickle.load(file_load)

        if game_data['current_player_id'] == 'player_light':
            current_player = game_data['player_light']
        elif game_data['current_player_id'] == 'player_dark':
            current_player = game_data['player_dark']
   
    return game_data['game_board'], game_data['player_light'], game_data['player_dark'], current_player

#Loops collecting input from player for location of picking up a piece until input is confirmed to be a valid pickup location
def check_location_pick(current_player):

    which_board = 0

    current_player_print = current_player.color.name.capitalize()

    while True:
        pick_up = input(f"Pick up piece {current_player_print}: ").strip().lower()

        #If input is coordinates, makes sure that they are within valid range before returning
        if len(pick_up) == 2 and pick_up.isdigit():
            which_board = 0
            col_up, row_up = map(int, pick_up)
            if 0 <= col_up <=3 and 0 <= row_up <= 3:
                return which_board, col_up, row_up

        #If input is a letter, makes that that it is within valid ascii range before returning
        elif len(pick_up) == 1:
           
            letter_val = ord(pick_up)

            if 97 <= letter_val <= 99:
                which_board = 1
                col_up = ord(pick_up) - 97
                row_up = 0

                return which_board, col_up, row_up

        print('Unvalid pick up location, please try again.')

#Loops collecting input from player for location of putting down a piece until input is confirmed to be a valid put down location
def check_location_put(current_player):
   
    current_player_print = current_player.color.name.capitalize()

    while True:
        put_down = input(f"Put down piece {current_player_print}: ").strip()

        #Confirms that input is coordinates and it is within the valid range before returning
        if len(put_down) == 2 and put_down.isdigit():
            col_down, row_down = map(int, put_down)

            if 0 <= col_down <=3 and 0 <= row_down <= 3:
                return col_down, row_down

        print('Unvalid put down location, please try again')

#Once pick up location is confirmed to be valid, loops until the check that the piece at that location is valid
def check_piece_pick(game_board, current_player):

    game_piece = None

    while game_piece is None:

        which_board, col_up, row_up = check_location_pick(current_player)

        if which_board == 0:

            top_piece = game_board.check_top_piece(col_up, row_up)

            #If there is no valid piece on the game board, try again
            if top_piece.size == 0:
                print('You cannot pick up there, try again.')
                continue

            #If the piece color does not match current player color, try again
            if top_piece.color != current_player.color:
                print('You can only pick up your own piece, please try again.')
                continue

            game_piece = game_board.get_piece(col_up, row_up)

        elif which_board == 1:

            #If there is no piece on the player board, try again
            player_game_piece = current_player.get_piece(col_up)
            if player_game_piece is None:
                print('You cannot pick up there, try again.')
                continue

            game_piece = player_game_piece
       
        else:
            print('Unvalid selection, please try again.')

        return game_piece, col_up, row_up, which_board

#Once put down location is confirmed to be valid, loops until the check that the piece at that location is valid
def check_piece_put(game_piece, game_board, current_player, col_up, row_up, which_board):

    while True:
        col_down, row_down = check_location_put(current_player)

        board_piece = game_board.check_top_piece(col_down, row_down).size

        near_win, near_win_player = check_near_win(game_board)

        valid_put = False

        if which_board == 0:
            #Only allows piece to be down at that location as long as it is not the same as the pick up location
            if (col_down, row_down) == (col_up, row_up):
                print('You cannot put down where you picked up, please try again.')
                continue

            #Only allows the piece to be put down if the piece at that location already is smaller than the picked up piece
            if game_piece.size > board_piece:
                game_board.put_piece(col_down, row_down, game_piece)
                valid_put = True
            else:
                print('You cannot place there, try again.')
                continue
       
        #Only allows a pice taken from the player board to be put down on an empty spot on the game board
        # unless the other player has 3 in a col
        if which_board == 1:
            if not near_win and (near_win_player != game_piece.color.name):
                if board_piece != 0:
                    print('You must put down a new piece onto an empty spot, please try again.')
                    continue

            #Only allows the piece to be put down if the piece at that location already is smaller than the picked up piece
            if game_piece.size > board_piece:
                game_board.put_piece(col_down, row_down, game_piece)
                valid_put = True
            else:
                print('You cannot place there, try again.')

        if valid_put:
            return col_down, row_down

#Checks if there are 4 pieces of the same color in the cols, columns, and diagonals of the game board,
# if yes, returns True and which player won
def check_win(game_board):
           
    #Checks wins in cols
    for col in range(4):
        first_piece = game_board.check_top_piece(col, 0)
        if first_piece:
            if all(game_board.check_top_piece(col, row).color == first_piece.color for row in range(4)):
                return True, first_piece.color.name
   
    #Check wins in columns
    for row in range(4):
        first_piece = game_board.check_top_piece(0, row)
        if first_piece:
            if all(game_board.check_top_piece(col, row).color == first_piece.color for col in range(4)):
                return True, first_piece.color.name
   
    #Checks win on top-left to bottom-right diagonal
    first_piece = game_board.check_top_piece(0, 0)
    if first_piece:
        if all(game_board.check_top_piece(i, i).color == first_piece.color for i in range(4)):
            return True, first_piece.color.name
   
    #Checks win on top-right to bottom-left diagonal
    first_piece = game_board.check_top_piece(3, 0)
    if first_piece:
        if all(game_board.check_top_piece(i, 3 - i).color == first_piece.color for i in range(4)):
            return True, first_piece.color.name
   
    return False, None

#Checks if a player won, if yes prints game_board (to see 4 in a col), game over, who the winner is, and returns True
def detect_win(game_board):

    if_win, winner_color = check_win(game_board)

    if if_win:
        print_game_board(game_board)
        print('Game Over!')
        print(f'The winner is: {(winner_color).capitalize()}!')
       
        return True

#Checks if there are 3 pieces of the same color in the cols, columns, and diagonals of the game board,
# If yes, returns true and which player it is with 3 in a col
def check_near_win(game_board):
   
    near_win = False
    near_win_player = 'X'
   
    #Checks if 3 in a col for columns
    for col in range(4):
       
        col_piece_colors = []
       
        #Adds the names of every color in the col color to a list
        # (unless there is no piece, then None is appended)
        for row in range(4):
            piece = game_board.check_top_piece(col, row)
            col_piece_colors.append(piece.color.name if piece else None)
           
        #Only checks each color (+ None) once by removing duplicates in the list
        for piece_color in set(col_piece_colors):
           
            #If there are 3 of one color in the list for this col
            # then near_win is True and the near_win_player is assigned to the color of the near win
            if piece_color is not None and col_piece_colors.count(piece_color) == 3:
                near_win = True
                near_win_player = piece_color
   
    #Checks if 3 in a col for rows
    for row in range(4):
       
        row_piece_colors = []
       
        #Adds the names of every color in the col color to a list
        # (unless there is no piece, then None is appended)
        for col in range(4):
            piece = game_board.check_top_piece(col, row)
            row_piece_colors.append(piece.color.name if piece else None)
           
        #Only checks each color (+ None) once by removing duplicates in the list
        for piece_color in set(row_piece_colors):
           
            #If there are 3 of one color in the list for this column
            # then near_win is True and the near_win_player is assigned to the color of the near win
            if piece_color is not None and row_piece_colors.count(piece_color) == 3:
                near_win = True
                near_win_player = piece_color
   
    #Checks if 3 in a col for top-left to bottom-right diagonal
    for i in range(4):
       
        left_dia_piece_colors = []

        #Appends each piece along the diagonal to a list
        # (unless there is no piece, then None is appended)
        piece = game_board.check_top_piece(i, i)
        left_dia_piece_colors.append(piece.color.name if piece else None)
       
        #Only checks each color (+ None) once by removing duplicates in the list
        for piece_color in set(left_dia_piece_colors):
           
            #If there are 3 of one color in the list for this diagonal
            # then near_win is True and the near_win_player is assigned to the color of the near win
            if piece_color is not None and left_dia_piece_colors.count(piece_color) == 3:
                near_win = True
                near_win_player = piece_color
   
    #Checks if 3 in a col for top-right to bottom-left diagonal
    for i in range(4):
       
        right_dia_piece_colors = []
       
        #Appends each piece along the diagonal to a list
        # (unless there is no piece, then None is appended)
        piece = game_board.check_top_piece(i, 3 - i)
        right_dia_piece_colors.append(piece.color.name if piece else None)
       
        #Only checks each color (+ None) once by removing duplicates in the list
        for piece_color in set(right_dia_piece_colors):
           
            #If there are 3 of one color in the list for this diagonal
            # then near_win is True and the near_win_player is assigned to the color of the near win
            if piece_color is not None and right_dia_piece_colors.count(piece_color) == 3:
                near_win = True
                near_win_player = piece_color
               
    return near_win, near_win_player
   
move_history = []

def record_moves(current_player_name, which_board, col_up, row_up, col_down, row_down):
   
    if which_board == 0:
        start = (col_up, row_up)
        end = (col_down, row_down)

        if start <= end:
            move = (current_player_name, start, end)
        else:
            move = (current_player_name, end, start)
   
    else:
        move = (current_player_name, 1, col_up, col_down, row_down)

    move_history.append(move)

def check_tie(move_history):

    tie = False

    if len(move_history) > 5:

        current_player = move_history[-1][0]
        repeating_player_moves = []

        for move in reversed(move_history):
            if move[0] == current_player:
                repeating_player_moves.append(move)

            if len(repeating_player_moves) == 3:
                break

        if len(repeating_player_moves) == 3:
            if repeating_player_moves[0] == repeating_player_moves[1] == repeating_player_moves[2]:
                tie = True
        
        move_history.pop(0)
    return tie

