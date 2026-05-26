
#Imports other file and pickle module for file saving & loading
from Gobblet_Classes import *
import pickle
import os

#Prints text explaining the function of the program
def print_program_instructions():
    print('Welcome to Gobblet!')
    print('Valid pick up locations: ')
    print('Player board: a b c')
    print('Gameboard: coordinates 00 to 33 as column then row')
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

            #If an unvalid input was entered, loops until a valid one is entered
            print('Unvalid player selection, please try again.')

#Saves the current game state by overwriting the previous save
def save_game(game_board, player_light, player_dark, current_player):

    #Opens the save file, assigns current player id to a string based on who the current player is,
    with open('.autosave', 'wb') as file_save:
        if current_player == player_light:
            current_player_id = 'player_light'
        elif current_player == player_dark:
            current_player_id = 'player_dark'

        #Saves the game data as a dictionary using pickle, closes file automatically using 'with'
        pickle.dump({
            'game_board': game_board,
            'player_light': player_light,
            'player_dark': player_dark,
            'current_player_id': current_player_id
        }, file_save)

#Loads file containing game state from previous game
def load_game():

    #If there is an autosave file, load the file
    if os.path.exists('.autosave'):
        #Opens the file, extracts data using pickle, restores current player to a player based on who the current player was during the save,
        # returns all loaded game objects, closes file using 'with'
        with open('.autosave', 'rb') as file_load:

            game_data = pickle.load(file_load)

            if game_data['current_player_id'] == 'player_light':
                current_player = game_data['player_light']
            elif game_data['current_player_id'] == 'player_dark':
                current_player = game_data['player_dark']
    
        return game_data['game_board'], game_data['player_light'], game_data['player_dark'], current_player
    else:
        print('There is no autosave file.')

#Loops collecting input from player for location of picking up a piece until input is confirmed to be a valid pickup location
def check_location_pick(current_player):

    which_board = 'game_board'

    current_player_print = current_player.color.name.capitalize()

    while True:
        pick_up = input(f"Pick up piece {current_player_print}: ").strip().lower()

        #If input is coordinates, makes sure that they are within valid range before returning
        if len(pick_up) == 2 and pick_up.isdigit():
            which_board = 'game_board'
            col_up, row_up = map(int, pick_up)
            if 0 <= col_up <=3 and 0 <= row_up <= 3:
                return which_board, col_up, row_up

        #If input is a letter, makes sure that that it is within the valid ascii range before returning
        elif len(pick_up) == 1:
           
            letter_val = ord(pick_up)

            if 97 <= letter_val <= 99:
                which_board = 'player_board'
                col_up = ord(pick_up) - 97
                row_up = 0

                return which_board, col_up, row_up

        #If input is not valid, loops until a valid one is entered
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

        #If input is not valid, loops until a valid one is entered
        print('Unvalid put down location, please try again')

#Once pick up location is confirmed to be valid, loops until the check that the piece at that location is valid
def check_piece_pick(game_board, current_player):

    game_piece = None

    while game_piece is None:

        which_board, col_up, row_up = check_location_pick(current_player)

        if which_board == 'game_board':

            top_piece = game_board.check_top_piece(col_up, row_up)

            #If there is no valid piece on the game board, try again
            if top_piece.size == 0:
                print('You cannot pick up there, try again.')
                continue

            #If the piece color does not match current player color, try again
            if top_piece.color != current_player.color:
                print('You can only pick up your own piece, please try again.')
                continue

            #If the piece at the location passes the validity checks, then the game piece is assigned as such
            game_piece = game_board.get_piece(col_up, row_up)

        elif which_board == 'player_board':

            #If there is no piece on the player board, try again
            player_game_piece = current_player.get_piece(col_up)
            if player_game_piece is None:
                print('You cannot pick up there, try again.')
                continue

            #If the piece at the location passes the validity checks, then the game piece is assigned as such
            game_piece = player_game_piece
       
        else:
            #If input is not valid, loops until a valid one is entered
            print('Unvalid selection, please try again.')

        #Returns the game piece, its coordinates and which board it was taken from
        return game_piece, col_up, row_up, which_board

#Once put down location is confirmed to be valid, loops until the check that the piece at that location is valid
def check_piece_put(game_piece, game_board, current_player, col_up, row_up, which_board):

    while True:
        col_down, row_down = check_location_put(current_player)

        board_piece = game_board.check_top_piece(col_down, row_down).size

        near_win, near_win_player = check_near_win(game_board)

        valid_put = False

        if which_board == 'game_board':
            #Only allows piece to be down at that location as long as it is not the same as the pick up location
            if (col_down, row_down) == (col_up, row_up):
                print('You cannot put down where you picked up, please try again.')
                continue

            #Only allows the piece to be put down if the piece at that location is smaller than the picked up piece
            # (includes empty spots as a null piece with size 0)
            if game_piece.size > board_piece:
                game_board.put_piece(col_down, row_down, game_piece)
                valid_put = True
            else:
                print('You cannot place there, try again.')
                continue
       
        #Only allows a piece taken from the player board to be put down on an empty spot on the game board
        # unless the other player has 3 in a row (near win)
        if which_board == 'player_board':
            if not near_win and (near_win_player != game_piece.color.name):
                if board_piece != 0:
                    print('You must put down a new piece onto an empty spot, please try again.')
                    continue

            #Only allows the piece to be put down if the piece at that location is smaller than the picked up piece
            # (includes empty spots as a null piece with size 0)
            if game_piece.size > board_piece:
                game_board.put_piece(col_down, row_down, game_piece)
                valid_put = True
            else:
                print('You cannot place there, try again.')

        #If the piece at the put down location allows for the picked up piece to be placed on top, 
        # then the put down location is returned
        if valid_put:
            return col_down, row_down

#Checks if there are 4 pieces of the same color in the rows, columns, and diagonals of the game board,
# if yes, returns True and which player won
def check_win(game_board):
           
    #Checks for a win in each column
    for col in range(4):
        first_piece = game_board.check_top_piece(col, 0)
        if first_piece:
            if all(game_board.check_top_piece(col, row).color == first_piece.color for row in range(4)):
                return True, first_piece.color.name
   
    #Checks for a win in each row
    for row in range(4):
        first_piece = game_board.check_top_piece(0, row)
        if first_piece:
            if all(game_board.check_top_piece(col, row).color == first_piece.color for col in range(4)):
                return True, first_piece.color.name
   
    #Checks for a win on the top-left to bottom-right diagonal
    first_piece = game_board.check_top_piece(0, 0)
    if first_piece:
        if all(game_board.check_top_piece(i, i).color == first_piece.color for i in range(4)):
            return True, first_piece.color.name
   
    #Checks for a win on top-right to bottom-left diagonal
    first_piece = game_board.check_top_piece(3, 0)
    if first_piece:
        if all(game_board.check_top_piece(i, 3 - i).color == first_piece.color for i in range(4)):
            return True, first_piece.color.name
   
    return False, None

#Checks if a player won, if yes prints the game board (to see the win), game over, who the winner is, and returns True
def detect_win(game_board):

    if_win, winner_color = check_win(game_board)

    if if_win:
        print('Game Over!')
        print(f'The winner is: {(winner_color).capitalize()}!')
       
        return True

#Checks if there is a near win by checking if there are 3 pieces of the same color in the rows, columns, and diagonals of the game board,
# If yes, returns true and which player it is with 3 in a row
def check_near_win(game_board):
   
    near_win = False
    near_win_player = 'X'
   
    #Checks if 3 of the same in columns
    for col in range(4):
       
        col_piece_colors = []
       
        #Adds the names of every color in the column to a list
        # (unless there is no piece, then None is appended)
        for row in range(4):
            piece = game_board.check_top_piece(col, row)
            col_piece_colors.append(piece.color.name if piece else None)
           
        #Only checks each color (+ None) once by removing duplicates in the list
        for piece_color in set(col_piece_colors):
           
            #If there are 3 of one color in the list for this column
            # then near_win is True and the near_win_player is assigned to the color of the near win
            if piece_color is not None and col_piece_colors.count(piece_color) == 3:
                near_win = True
                near_win_player = piece_color
   
    #Checks if 3 of the same in rows
    for row in range(4):
       
        row_piece_colors = []
       
        #Adds the names of every color in the row to a list
        # (unless there is no piece, then None is appended)
        for col in range(4):
            piece = game_board.check_top_piece(col, row)
            row_piece_colors.append(piece.color.name if piece else None)
           
        #Only checks each color (+ None) once by removing duplicates in the list
        for piece_color in set(row_piece_colors):
           
            #If there are 3 of one color in the list for this row
            # then near_win is True and the near_win_player is assigned to the color of the near win
            if piece_color is not None and row_piece_colors.count(piece_color) == 3:
                near_win = True
                near_win_player = piece_color
   
    #Checks if 3 of the same in the top-left to bottom-right diagonal
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
   
    #Checks if 3 of the same in the top-right to bottom-left diagonal
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
   
#Stores moves in move_history:
move_history = []
#Game board to game board moves are stored with the lower coordinate first,
# this is so that moving a piece back & forth between the same spots is considered the same move
def record_moves(current_player_name, which_board, col_up, row_up, col_down, row_down):
   
    #If the piece was picked up from the gameboard,
    #the coordinates are stored in sorted order (smallest -> largest)
    if which_board == 'game_board':
        start = (col_up, row_up)
        end = (col_down, row_down)

        #Formats the move as start = smallest coordinate and end = largest
        #The coordinates are compared left to right, so the x's (columns) are compared first, then the y's (rows)
        # Ex: 01 and 00 becomes 00 and 01, but 00 and 01 will stay the same
        if start <= end:
            move = (current_player_name, start, end)
        else:
            move = (current_player_name, end, start)
   
    #If the piece was picked up from the player board,
    # store where it came from and where it was placed
    elif which_board == 'player_board':
        move = (current_player_name, 'player_board', col_up, (col_down, row_down))

    #Add move to move history
    move_history.append(move)

#Checks if there is a tie between the players 
# looks through the move history for 3 identical moves in a row from both players
def check_tie(move_history):

    tie = False
    current_identical = False
    last_identical = False

    #If there are 6 moves in move_history
    if len(move_history) == 6:

        #The current and last players are in the last and second last move of the move history
        # at position 0 of the inputed move information
        current_player = move_history[-1][0]
        last_player = move_history [-2][0]

        #Counts every move from the players in the history
        curent_player_moves = []
        last_player_moves = []

        #Collects moves from the current player in the history until there are 3 moves in the list
        for move in reversed(move_history):
            if move[0] == current_player:
                curent_player_moves.append(move)

            if len(curent_player_moves) == 3:
                break

        #Collects moves from the last player in the history until there are 3 moves in the list
        for move in reversed(move_history):
            if move[0] == last_player:
                last_player_moves.append(move)

            if len(last_player_moves) == 3:
                break

        #If there are 3 moves from the current player in the history and they are all the same then the current player has made 3 identical moves
        if len(curent_player_moves) == 3:
            if curent_player_moves[0] == curent_player_moves[1] == curent_player_moves[2]:
                current_identical = True

        #If there are 3 moves from the last player in the history and they are all the same then the last player has made 3 identical moves
        if len(last_player_moves) == 3:
            if last_player_moves[0] == last_player_moves[1] == last_player_moves[2]:
                last_identical = True
        
        if current_identical and last_identical:
            tie = True

        #Removes oldest move from the history to make room for the next
        move_history.pop(0)

    return tie

