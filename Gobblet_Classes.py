
#Imports enumeration module for player_colo_class
from enum import Enum

#Class that contains a collection of player colors as numbers
class player_color_class(Enum):
   
    dark = 2
    light = 1
    initial = 0

#Class that contains all the attributes and methods of a player piece
class player_piece_class:
   
    color = player_color_class.initial
    size = 0
   
    #Sets the color and size of a player piece
    def __init__(self, in_color, in_size):
        self.color = in_color
        self.size = in_size

    #Defines what to do when print() is called for a player piece
    def __str__(self):
        piece_string = 'XXX'

        #If piece size is 0, print dash
        if self.size == 0:
            piece_string = " - "
       
        #If piece has a valid color, print piece size with assigned background color
        if self.color == player_color_class.dark:
            piece_string = f"\033[42m {self.size} \033[0m"
        elif self.color == player_color_class.light:
            piece_string = f"\033[45m {self.size} \033[0m"

        return piece_string
   
    def __bool__(self):
        return self.size != 0

#Class that contains all the attributes and methods of the stacks of the unplayed pieces in the player boards
class player_board_class:
   
    #Creates a list of 3 lists where each list contains 4 different sized pieces,
    # stacked in order of smallest to largest in the selected color
    def __init__(self, new_player_color: player_color_class):
        self.color = new_player_color
        NUM_PLAYER_STACKS = 3
        self.player_stacks = [[] for _ in range(NUM_PLAYER_STACKS)]
        for player_stack in range(3):
            for piece_size in range(1, 5):
                new_piece = player_piece_class(new_player_color, piece_size)
                self.player_stacks[player_stack].append(new_piece)

    #Removes the piece from the top of the stack at the passed in coordinate for the player board and returns it
    def get_piece(self, coord):

        if not self.player_stacks[coord]:
            return None
        return self.player_stacks[coord].pop()
   
    #Returns the piece at the top of the stack without removing it, at the passed in coordinate for the player board
    #Allows viewing of the top piece without removing it
    #Only returns the piece if there is one there, otherwise returns null piece
    def check_top_piece(self, coord):
        if len(self.player_stacks[coord]) == 0:
            return player_piece_class(player_color_class.initial, 0)
        return self.player_stacks[coord][-1]
    
    def reinitialize_from_json(self, player_board_json_data):

        for index in range(3):
            json_len = len(player_board_json_data[index])
            pieces_to_remove = 4 - json_len
            if json_len < 4:
                for _ in range(pieces_to_remove):
                    self.player_stacks[index].pop()
   


#Class that contains all the attributes and methods of the gameboard and the played pieces
class game_board_class:
   
    COLS = 4
    ROWS = 4
   
    #Creates 2d list of stacks containing null pieces to represent empty spots on the game board
    def __init__(self):
        self.board_stacks = [[[] for _ in range(self.ROWS)] for _ in range(self.COLS)]

        for col in range(4):
            for row in range(4):
                new_piece = player_piece_class(player_color_class.initial, 0)
                self.board_stacks[col][row].append(new_piece)
   
    #Removes the piece from the top of the stack at the passed in coordinate for the game board and returns it
    # Only returns if it is a valid piece otherwise returns none
    def get_piece(self, col_up, row_up):

        check_top_piece = self.board_stacks[col_up][row_up][-1]
        if check_top_piece.size == 0:
            return None
        return self.board_stacks[col_up][row_up].pop()

    #Returns the piece at the top of the stack without removing it,
    # Allows for viewing of the top piece without removing it
    def check_top_piece(self, col, row):
        return self.board_stacks[col][row][-1]

    #Puts a piece on the game board by appending it to the stack at the coordinates passed in for the game board
    def put_piece(self, col_down, row_down, game_piece):

        self.board_stacks[col_down][row_down].append(game_piece)

    def reinitialize_from_json(self, game_board_json_data):

        for col in range(4):
            for row in range(4):
                if len(game_board_json_data[col][row]) > 1:
                    for piece in game_board_json_data[col][row][1:]:
                        piece_color = piece[0]
                        piece_size = int(piece[1])

                        if piece_color == 'W':
                            new_color = player_color_class.light
                        elif piece_color == 'B':
                            new_color = player_color_class.dark
                
                        new_piece = player_piece_class(new_color, piece_size)
                        self.board_stacks[col][row].append(new_piece)