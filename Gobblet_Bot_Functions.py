
from itertools import combinations 
from functools import partial

def is_same_color(pieces):

    return all(piece.color == pieces[0].color for piece in pieces)

def find_3_in_a_row(game_board):

    potential_moves = []

    #Checks rows
    for row in range(4):
        full_line = [(col, row) for col in range(4)]

        #Creates every combination of 3 numbers within a range of 4
        for col_combos in combinations(range(4), 3):

            #List of 3 coordinates, one for every combinations of columns
            lines = [(col, row) for col in col_combos]

            #Creates a list of every piece at the coordinates for lines
            pieces = [game_board.check_top_piece(c, r) for c, r in lines]

            #If all the pieces exist and they are the same color
            if all(piece.size != 0 for piece in pieces):
                if is_same_color(pieces):

                    #Skips this combination if there is a size 4 piece of the other color in the row
                    row_color = pieces[0].color
                    if any(game_board.check_top_piece(c, r).color != row_color and game_board.check_top_piece(c, r).size == 4 for c, r in full_line):
                        continue

                    #The last unchecked column coordinate
                    last_col = [col for col in range(4) if col not in col_combos][0]
                    
                    if game_board.check_top_piece(last_col, row).size < 4:
                        potential_moves.append((last_col, row))

                    #If one of the pieces in the 3 in a row is less than 4, add it to potential moves
                    for c, r in lines:
                        if game_board.check_top_piece(c, r).size < 4:
                            potential_moves.append((c, r))

    #Checks columns
    for col in range(4):
        full_line = [(col, row) for row in range(4)]
        for row_combos in combinations(range(4), 3):

            lines = [(col, row) for row in row_combos]

            pieces = [game_board.check_top_piece(c, r) for c, r in lines]

            if all(piece.size != 0 for piece in pieces):
                if is_same_color(pieces):
                    
                    row_color = pieces[0].color
                    if any(game_board.check_top_piece(c, r).color != row_color and game_board.check_top_piece(c, r).size == 4 for c, r in full_line):
                        continue

                    last_row = [row for row in range(4) if row not in row_combos][0]
                    
                    if game_board.check_top_piece(col, last_row).size < 4:
                        potential_moves.append((col, last_row))

                    for c, r in lines:
                        if game_board.check_top_piece(c, r).size < 4:
                            potential_moves.append((c, r))

    diagonals = [
        [(i, i) for i in range(4)],
        [(i, 3 - i) for i in range(4)]
    ]

    #Checks diagonals
    for diag in diagonals:

        for index_combos in combinations(range(4), 3):

            lines = [diag[i] for i in  index_combos]
            pieces = [game_board.check_top_piece(c, r) for c, r in lines]

            if all(piece.size != 0 for piece in pieces):
                if is_same_color(pieces):

                    row_color = pieces[0].color
                    if any(game_board.check_top_piece(c, r).color != row_color and game_board.check_top_piece(c, r).size == 4 for c, r in diag):
                        continue

                    last_index = [i for i in range(4) if i not in index_combos][0]
                    last_col, last_row = diag[last_index]
                    
                    if game_board.check_top_piece(last_col, last_row).size < 4:
                        potential_moves.append((last_col, last_row))

                    for c, r in lines:
                        if game_board.check_top_piece(c, r).size < 4:
                            potential_moves.append((c, r))


    return potential_moves, row_color

piece_color_order = {
    1: 0,
    0: 1,
    2: 2
}

def check_for_sort(game_board, color_order, coord):

    piece = game_board.check_top_piece(coord[0], coord[1])

    color = piece.color.value
    size = piece.size

    color_sort = color_order.get(color, 99)

    return (color_sort, size)

def find_playerboard_piece(player_dark):

    largest_piece_pos = None
    largest_piece_size = -1

    for stack_pos in range(3):

        stack = player_dark.player_stacks[stack_pos]

        if stack:

            top_piece = stack[-1]

            if top_piece.size > largest_piece_size:
                largest_piece_size = top_piece.size
                largest_piece_pos = stack_pos
    
    return largest_piece_pos

def can_playerlight_win(game_board, player_light):

    potential_moves, row_color = find_3_in_a_row(game_board)
    return row_color == player_light

def find_gameboard_piece(game_board, player_light):

    largest_piece = None
    largest_piece_size = 0

    for col in range(4):
        for row in range(4):

            piece = game_board.check_top_piece(col, row)

            if piece.size == 0:
                continue

            removed_piece = game_board.get_piece(col, row)

            if not can_playerlight_win(game_board, player_light):

                if piece.size > largest_piece_size:
                    largest_piece = (col, row)
                    largest_piece_size = piece.size

            game_board.put_piece(col, row, removed_piece)

    return largest_piece

def find_largest_piece(game_board,
                       potential_moves, 
                       near_win_color, player_light, 
                       player_dark):

    found_piece = None

    if near_win_color == player_dark.color:
        
        for space in potential_moves:

            if game_board.check_top_piece(space[0], space[1]).size == 0:

                found_piece = find_playerboard_piece(player_dark)

            else:

                found_piece = find_gameboard_piece(game_board, player_light)

            if found_piece is not None:
                break

    elif near_win_color == player_light.color:

        found_piece = find_playerboard_piece(player_dark)

        if found_piece is None:

            found_piece = find_gameboard_piece(game_board, player_light)

    return found_piece

def do_bot_turn(game_board, player_light, player_dark):

    potential_moves, row_color = find_3_in_a_row(game_board)

    moves_sort = partial(
        check_for_sort, 
        game_board,
        piece_color_order,
        )
    potential_moves.sort(key=moves_sort)

    print(f'Potential Moves: {potential_moves}')

    largest_piece_pos = find_largest_piece(game_board, potential_moves, row_color, player_light, player_dark)

    print(largest_piece_pos)

