
from enum import Enum

class player_color_class(Enum):
    
    dark = (0, 0, 0)
    light = (255, 255, 255)
    initial = 0

class player_piece_class:
    
    color = player_color_class.initial
    size = 0
    
    def __init__(self, in_color, in_size):
        self.color = in_color
        self.size = in_size

    def __str__(self):
        piece_string = 'XXX'

        if self.color == player_color_class.dark:
            piece_string = f"\033[42m {self.size} \033[0m"
        elif self.color == player_color_class.light:
            piece_string = f"\033[45m {self.size} \033[0m"

        if self.size == 0:
            piece_string = " - "
        
        return piece_string

class player_board_class:
    
    def __init__(self, new_player_color: player_color_class):
        self.color = new_player_color
        NUM_PLAYER_STACKS = 3
        self.player_stacks = [[] for _ in range(NUM_PLAYER_STACKS)]
        for player_stack in range(3):
            for piece_size in range(1, 5):
                new_piece = player_piece_class(new_player_color, piece_size)
                self.player_stacks[player_stack].append(new_piece)

    def get_piece(self, coord):

        if not self.player_stacks[coord]:
            return None
        return self.player_stacks[coord].pop()
    
    def top_piece(self, coord):
        if len(self.player_stacks[coord]) == 0:
            return player_piece_class(player_color_class.initial, 0)
        return self.player_stacks[coord][-1]

class game_board_class:
    
    ROWS = 4
    COLS = 4
    
    def __init__(self):
        self.board_stacks = [[[] for _ in range(self.COLS)] for _ in range(self.ROWS)]

        for row in range(4):
            for col in range(4):
                new_piece = player_piece_class(player_color_class.initial, 0)
                self.board_stacks[row][col].append(new_piece)
    
    def top_piece(self, row, col):
        return self.board_stacks[row][col][-1]

    def get_piece(self, row_up, col_up):

        top_piece = self.board_stacks[row_up][col_up][-1]
        if top_piece.size == 0 and top_piece.color == player_color_class.initial:
            return None
        return self.board_stacks[row_up][col_up].pop()

    def put_piece(self, row_down, col_down, game_piece):

        self.board_stacks[row_down][col_down].append(game_piece)


