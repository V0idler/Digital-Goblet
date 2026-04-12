
from enum import Enum

class player_color_class(Enum):
    
    black = (0, 0, 0)
    white = (255, 255, 255)
    initial = 0

class player_piece_class:
    
    color = player_color_class.initial
    size = 0
    
    def __init__(self, in_color, in_size):
        self.color = in_color
        self.size = in_size

class player_board_class:
    
    def __init__(self, new_player_color: player_color_class):
        NUM_PLAYER_STACKS = 3
        self.player_stacks = [[] for _ in range(NUM_PLAYER_STACKS)]
        for player_stack in range(3):
            for piece_size in range(1, 5):
                new_piece = player_piece_class(new_player_color, piece_size)
                self.player_stacks[player_stack].append(new_piece)

    def look_at_player_board(self, stack_num):
        
        color_letter = 'X'
        
        if self.player_stacks[stack_num]:
            size = self.player_stacks[stack_num][-1].size
            color = self.player_stacks[stack_num][-1].color

            if color == player_color_class.black:
                color_letter = 'B'
            elif color == player_color_class.white:
                color_letter = 'W'
        
        else:
            size = 0
            
        piece_string = color_letter + str(size)
        
        return piece_string
    
    def get_piece(self, coord):

        if not self.player_stacks[coord]:
            return None
        return self.player_stacks[coord].pop()

class game_board_class:
    
    ROWS = 4
    COLS = 4
    
    def __init__(self):
        self.board_stacks = [[[] for _ in range(self.COLS)] for _ in range(self.ROWS)]

        for row in range(4):
            for col in range(4):
                new_piece = player_piece_class(player_color_class.initial, 0)
                self.board_stacks[row][col].append(new_piece)
                

    def look_at_game_board(self, row, col):
        size = self.board_stacks[row][col][-1].size
        color = self.board_stacks[row][col][-1].color
        
        color_letter = 'X'
        
        if color == player_color_class.black:
            color_letter = 'B'
        elif color == player_color_class.white:
            color_letter = 'W'
        elif color == player_color_class.initial:
            color_letter = 'X'
        
        piece_string = color_letter + str(size)
        
        return piece_string
    
    def top_piece(self, row, col):
        return self.board_stacks[row][col][-1]

    def get_piece(self, row_up, col_up):

        top_piece = self.board_stacks[row_up][col_up][-1]
        if top_piece.size == 0 and top_piece.color == player_color_class.initial:
            return None
        return self.board_stacks[row_up][col_up].pop()

    def put_piece(self, row_down, col_down, game_piece):

        self.board_stacks[row_down][col_down].append(game_piece)


