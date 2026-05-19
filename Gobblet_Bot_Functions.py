
from itertools import combinations 
from functools import partial
from Gobblet_Functions import check_win

def is_same_color(pieces):

    return all(piece.color == pieces[0].color for piece in pieces)

def find_3_in_a_row(game_board, player_dark, player_light):

    potential_moves = {player_dark.color: [], player_light.color: []}
    untouchable_row_pieces = {player_dark.color: [], player_light.color: []}

    def process_line(line_coords):

        for line_combos in combinations(line_coords, 3):
            pieces = [game_board.check_top_piece(c, r) for c, r in line_combos]

            if all(piece.size != 0 for piece in pieces) and is_same_color(pieces):

                line_color = pieces[0].color

                blockers = [(c, r) for c, r in line_coords if game_board.check_top_piece(c, r).color != line_color and game_board.check_top_piece(c, r).size == 4]
                if blockers:
                    for block_col, block_row in blockers:
                        if (block_col, block_row) not in untouchable_row_pieces[line_color]:
                            untouchable_row_pieces[line_color].append((block_col, block_row))
                    continue
                
                last_coord = [coord for coord in line_coords if coord not in line_combos][0]
                last_col, last_row = last_coord
                
                if game_board.check_top_piece(last_col, last_row).size < 4:
                    if (last_col, last_row) not in potential_moves[line_color]:
                        potential_moves[line_color].append((last_col, last_row))

                for (c, r) in line_combos:

                    if line_color != player_dark.color:
                        if game_board.check_top_piece(c, r).size < 4:
                                if (c, r) not in potential_moves[line_color]:
                                    potential_moves[line_color].append((c, r))
                        else:
                            if (c, r) not in untouchable_row_pieces[line_color]:
                                untouchable_row_pieces[line_color].append((c, r))

                    else:
                        if (c, r) not in untouchable_row_pieces[line_color]:
                            untouchable_row_pieces[line_color].append((c, r))

    #Checks rows
    for row in range(4):
        process_line([(col, row) for col in range(4)])

    #Checks columns
    for col in range(4):
        process_line([(col, row) for row in range(4)])
        
    diagonals = [
        [(i, i) for i in range(4)],
        [(i, 3 - i) for i in range(4)]
    ]

    #Checks diagonals
    for diag in diagonals:
        process_line(diag)

    return potential_moves, untouchable_row_pieces

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

def find_gameboard_piece(game_board, player_light, player_dark, potential_moves, untouchable_row_pieces):

    largest_piece = None
    largest_piece_size = 0

    for col in range(4):
        for row in range(4):

            if (col, row) in potential_moves or (col, row) in untouchable_row_pieces:
                continue

            piece = game_board.check_top_piece(col, row)

            if piece.size == 0 or (piece.color != player_dark.color):
                continue

            removed_piece = game_board.get_piece(col, row)

            is_win, winner_player = check_win(game_board)

            if not (is_win and (winner_player == player_light.color)):

                if piece.size > largest_piece_size:
                    largest_piece = (col, row)
                    largest_piece_size = piece.size

            game_board.put_piece(col, row, removed_piece)

    return largest_piece

def find_largest_piece(game_board,
                       potential_moves, 
                       player_light, 
                       player_dark, 
                       untouchable_row_pieces):

    found_piece = None

    all_protected_pieces = untouchable_row_pieces[player_dark.color] + untouchable_row_pieces[player_light.color]

    if potential_moves[player_dark.color]:

        targets = potential_moves[player_dark.color]

        gameboard_coord = find_gameboard_piece(game_board, player_light, player_dark, targets, all_protected_pieces)
        gameboard_size = game_board.check_top_piece(gameboard_coord[0], gameboard_coord[1]).size if gameboard_coord is not None else 0

        if gameboard_size > 0:
            found_piece = gameboard_coord

    if potential_moves[player_light.color]:

        targets = potential_moves[player_light.color]

        playerboard_stack = find_playerboard_piece(player_dark)
        playerboard_size = player_dark.check_top_piece(playerboard_stack).size if playerboard_stack is not None else 0

        gameboard_coord = find_gameboard_piece(game_board, player_light, player_dark, targets, all_protected_pieces)
        gameboard_size = game_board.check_top_piece(gameboard_coord[0], gameboard_coord[1]).size if gameboard_coord is not None else 0

        if playerboard_size >= gameboard_size and playerboard_size > 0:
            found_piece = playerboard_stack
        elif gameboard_size > 0:
            found_piece = gameboard_coord

    return found_piece

def gameboard_largest_piece(bot_targets, game_board, largest_piece_pos):

    large_col, large_row = largest_piece_pos

    for move in bot_targets:

        col_down, row_down = move

        if game_board.check_top_piece(large_col, large_row).size > game_board.check_top_piece(col_down, row_down).size:

            moved_piece = game_board.get_piece(large_col, large_row)
            game_board.put_piece(col_down, row_down, moved_piece)

        else:
            print('no gameboard')

def playerboard_largest_piece(bot_targets, player_board, game_board, largest_piece_pos):

    for move in bot_targets:
                
                col_down, row_down = move

                if player_board.check_top_piece(largest_piece_pos).size > game_board.check_top_piece(col_down, row_down).size:

                    moved_piece = player_board.get_piece(largest_piece_pos)
                    game_board.put_piece(col_down, row_down, moved_piece)

                    break

                else:
                    print('no playerboard')

def do_bot_turn(game_board, player_light, player_dark):

    potential_moves, untouchable_row_pieces = find_3_in_a_row(game_board, player_dark, player_light)

    moves_sort = partial(
        check_for_sort, 
        game_board,
        piece_color_order,
        )

    dark_bot_targets = potential_moves[player_dark.color]
    dark_bot_targets.sort(key=moves_sort)

    light_bot_targets = potential_moves[player_light.color]
    light_bot_targets.sort(key=moves_sort)


    print(f'Potential Moves: {dark_bot_targets}, {light_bot_targets}')

    largest_piece_pos = find_largest_piece(game_board, potential_moves, player_light, player_dark, untouchable_row_pieces)

    print(largest_piece_pos)

    if largest_piece_pos is not None:
        if isinstance(largest_piece_pos, tuple):

            if dark_bot_targets:

                gameboard_largest_piece(dark_bot_targets, game_board, largest_piece_pos)
                
            elif light_bot_targets:

                gameboard_largest_piece(light_bot_targets, game_board, largest_piece_pos)

            else:
                print('no gameboard targets')

        elif isinstance(largest_piece_pos, int):

            if dark_bot_targets:

                playerboard_largest_piece(dark_bot_targets, player_dark, game_board, largest_piece_pos)
                
            elif light_bot_targets:

                playerboard_largest_piece(light_bot_targets, player_dark, game_board, largest_piece_pos)

            else:
                print('no playerboard targets')

    else:
        print('no 3 in a row')


        

                


