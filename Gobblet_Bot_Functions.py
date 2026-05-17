
from itertools import combinations 

def is_same_color(pieces):

    return all(piece.color == pieces[0].color for piece in pieces)

def find_3_in_a_row(game_board):

    empty_spots = []
    potential_moves = []

    #Checks columns
    for row in range(4):
        full_line = [(col, row) for col in range(4)]
        for cols in combinations(range(4), 3):

            lines = [(col, row) for col in cols]

            pieces = [game_board.check_top_piece(col, row) for col, row in lines]

            if all(piece.size != 0 for piece in pieces):
                if is_same_color(pieces):

                    row_color = pieces[0].color
                    if any(game_board.check_top_piece(col, row).color != row_color and game_board.check_top_piece(col, row).size == 4 for col, row in full_line):
                        continue

                    last_col = [col for col in range(4) if col not in cols][0]

                    if game_board.check_top_piece(last_col, row).size == 0:
                        empty_spots.append((last_col, row))
                    
                    elif game_board.check_top_piece(last_col, row).size < 4:
                        potential_moves.append((last_col, row))

                    for c, r in lines:
                        if game_board.check_top_piece(c, r).size < 4:
                            potential_moves.append((c, r))

    #Checks rows
    for col in range(4):
        full_line = [(col, row) for row in range(4)]
        for rows in combinations(range(4), 3):

            lines = [(col, row) for row in rows]

            pieces = [game_board.check_top_piece(col, row) for col, row in lines]

            if all(piece.size != 0 for piece in pieces):
                if is_same_color(pieces):
                    
                    row_color = pieces[0].color
                    if any(game_board.check_top_piece(col, row).color != row_color and game_board.check_top_piece(col, row).size == 4 for col, row in full_line):
                        continue

                    last_row = [row for row in range(4) if row not in rows][0]

                    if game_board.check_top_piece(col, last_row).size == 0:
                        empty_spots.append((col, last_row))
                    
                    elif game_board.check_top_piece(col, last_row).size < 4:
                        potential_moves.append((col, last_row))

                    for c, r in lines:
                        if game_board.check_top_piece(c, r).size < 4:
                            potential_moves.append((c, r))

    diagonals = [
        [(i, i) for i in range(4)],
        [(i, 3 - i) for i in range(4)]
    ]

    for diag in diagonals:

        for indicies in combinations(range(4), 3):

            lines = [diag[i] for i in  indicies]
            pieces = [game_board.check_top_piece(col, row) for col, row in lines]

            if all(piece.size != 0 for piece in pieces):
                if is_same_color(pieces):

                    row_color = pieces[0].color
                    if any(game_board.check_top_piece(col, row).color != row_color and game_board.check_top_piece(col, row).size == 4 for col, row in diag):
                        continue

                    last_index = [i for i in range(4) if i not in indicies][0]
                    last_col, last_row = diag[last_index]

                    if game_board.check_top_piece(last_col, last_row).size == 0:
                        empty_spots.append((last_col, last_row))
                    
                    elif game_board.check_top_piece(last_col, last_row).size < 4:
                        potential_moves.append((last_col, last_row))

                    for c, r in lines:
                        if game_board.check_top_piece(c, r).size < 4:
                            potential_moves.append((c, r))


    return empty_spots, potential_moves


def do_bot_turn(game_board, dark_board, light_board):

    empty_spots, potential_moves = find_3_in_a_row(game_board)
    print(f' Empty: {empty_spots}')
    print(f' Non-empty: {potential_moves}')



