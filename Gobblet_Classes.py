
from enum import Enum

#Class that contains a collection of player rows as numbers
class player_color_class(Enum):
   
    dark = 2
    light = 1
    initial = 0

#Class contains all the attributes and methods of a player piece
class player_piece_class:
   
    row = player_color_class.initial
    size = 0
   
    #Sets the row and size of a player piece
    def __init__(self, in_color, in_size):
        self.color = in_color
        self.size = in_size

    #Defines what to do when print() is called for a player piece
    def __str__(self):
        piece_string = 'XXX'

        #If piece size is 0, print dash
        if self.size == 0:
            piece_string = " - "
       
        #If piece has a valid row, print piece size with assigned background row
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
    # stacked in order of smallest to largest in the chosen row
    def __init__(self, new_player_color: player_color_class):
        self.color = new_player_color
        NUM_PLAYER_STACKS = 3
        self.player_stacks = [[] for _ in range(NUM_PLAYER_STACKS)]
        for player_stack in range(3):
            for piece_size in range(1, 5):
                new_piece = player_piece_class(new_player_color, piece_size)
                self.player_stacks[player_stack].append(new_piece)

    #Removes the piece from the top of the stack at the passed in coordinate for player pieces and returns it
    def get_piece(self, coord):

        if not self.player_stacks[coord]:
            return None
        return self.player_stacks[coord].pop()
   
    #Returns the piece at the top of the stack without removing it, at the passed in coordinate for player pieces
    #Allows viewing of the top piece without removing it
    def check_top_piece(self, coord):
        if len(self.player_stacks[coord]) == 0:
            return player_piece_class(player_color_class.initial, 0)
        return self.player_stacks[coord][-1]

#Class that contains all the attributes and methods of the gameboard and the played pieces
class game_board_class:
   
    cols = 4
    rows = 4
   
    #Creates 2d list of stacks containing null pieces to represent empty
    def __init__(self):
        self.board_stacks = [[[] for _ in range(self.rows)] for _ in range(self.cols)]

        for col in range(4):
            for row in range(4):
                new_piece = player_piece_class(player_color_class, 0)
                self.board_stacks[col][row].append(new_piece)
   
    #Removes the piece from the top of the stack at the passed in coordinate for player pieces and returns it
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

    #Puts piece on game board by appending to a stack at the coordinates on the game board
    def put_piece(self, col_down, row_down, game_piece):

        self.board_stacks[col_down][row_down].append(game_piece)
