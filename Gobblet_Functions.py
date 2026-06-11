
#Imports other file and pickle module for file saving & loading
from Gobblet_Classes import *
import pickle
import os

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
        #Opens the file, extracts data using pickle, restores current player to 
        # a player based on who the current player was during the save,
        # returns all loaded game objects, closes file using 'with'
        with open('.autosave', 'rb') as file_load:

            game_data = pickle.load(file_load)

            if game_data['current_player_id'] == 'player_light':
                current_player = game_data['player_light']
            elif game_data['current_player_id'] == 'player_dark':
                current_player = game_data['player_dark']
    
        return game_data['game_board'], game_data['player_light'], game_data['player_dark'], current_player

# Intializes new game by generating new game objects using classes and randomly selecting the starting player
def setup_newgame():
    player_light = player_board_class(player_color_class.light)
    player_dark = player_board_class(player_color_class.dark)

    game_board = game_board_class()

    return player_light, player_dark, game_board

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

#Checks if there is a near win by checking if there are 3 pieces of 
# the same color in the rows, columns, and diagonals of the game board,
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
    left_dia_piece_colors = []
    for i in range(4):

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
    right_dia_piece_colors = []
    for i in range(4):
       
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
    if len(move_history) >= 6:

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
        while len(move_history) > 5:
            move_history.pop(0)

    return tie

