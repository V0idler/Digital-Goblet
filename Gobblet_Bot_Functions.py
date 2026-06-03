
from itertools import combinations 
from functools import partial
from Gobblet_Functions import check_win, check_near_win, record_moves
import random

#Checks if there is a 2 in a line for the bot without player pieces and returns the appropriate coordinates for adding to the line
def find_2_in_a_line(game_board, player_dark):

    potential_moves = []

    def process_line(line_coords):
        pieces = [game_board.check_top_piece(c, r) for c, r in line_coords]

        dark_count = 0
        empty_coords = []

        for coord, piece in zip(line_coords, pieces):
            if piece.size == 0:
                empty_coords.append(coord)
            elif piece.color == player_dark.color:
                dark_count += 1

        if dark_count == 2 and len(empty_coords) == 2:
            for coord in empty_coords:
                if coord not in potential_moves:
                    potential_moves.append(coord)

    #Checks rows
    for row in range(4):
        process_line([(col, row) for col in range(4)])

    #Checks columns
    for col in range(4):
        process_line([(col, row) for row in range(4)])
        
    #Generates the line coordinates for the diagonals
    diagonals = [
        [(i, i) for i in range(4)],
        [(i, 3 - i) for i in range(4)]
    ]

    #Checks diagonals
    for diag in diagonals:
        process_line(diag)

    return potential_moves

#Returns wether or not the list of inputted pieces are the same color
def is_same_color(pieces):

    return all(piece.color == pieces[0].color for piece in pieces)

#Checks if there is a 3 in a line for the bot or player and returns the appropriate coordinates for blocking/winning
def find_3_in_a_line(game_board, player_dark, player_light):

    potential_moves = {player_dark.color: [], player_light.color: []}
    untouchable_row_pieces = {player_dark.color: [], player_light.color: []}

    #Processes the current row/col/diag to be checked for 3 in a line using the coordinates passed in for the line
    def process_line(line_coords):

        #Checks every possible combination of 3 coordinates within the line of 4 coordinates
        for line_combos in combinations(line_coords, 3):

            pieces = [game_board.check_top_piece(c, r) for c, r in line_combos]

            #If the 3 pieces in the line combo are not size 0 (empty) and are the same color:
            if all(piece.size != 0 for piece in pieces) and is_same_color(pieces):

                line_color = pieces[0].color

                #Adds pieces that are the largest size and not part of the three in a row to a list of pieces that cannot be moved
                #If there is a piece like this then skip this line because it has already been blocked
                blockers = [(c, r) for c, r in line_coords if game_board.check_top_piece(c, r).color != line_color and game_board.check_top_piece(c, r).size == 4]
                if blockers:
                    for block_col, block_row in blockers:
                        if (block_col, block_row) not in untouchable_row_pieces[line_color]:
                            untouchable_row_pieces[line_color].append((block_col, block_row))
                    continue
                
                #Finds the piece that is not apart of the 3 in a row
                last_coord = [coord for coord in line_coords if coord not in line_combos][0]
                last_col, last_row = last_coord
                
                #If the last piece is less than 4 then the coordinate is added to potential moves
                if game_board.check_top_piece(last_col, last_row).size < 4:
                    if (last_col, last_row) not in potential_moves[line_color]:
                        potential_moves[line_color].append((last_col, last_row))


                for (c, r) in line_combos:

                    #If the 3 in a line is the player and a piece within the line is less than 4 
                    # then the coordinates are added to potential moves (for blocking)
                    if line_color != player_dark.color:
                        if game_board.check_top_piece(c, r).size < 4:
                                if (c, r) not in potential_moves[line_color]:
                                    potential_moves[line_color].append((c, r))
                        
                        #If the piece is size 4 then it can not be blocked and is added to the untouchable pieces
                        else:
                            if (c, r) not in untouchable_row_pieces[line_color]:
                                untouchable_row_pieces[line_color].append((c, r))

                    #If the 3 in a line is the bot then it should not do anything to the piece 
                    # because it does not need to and moving/gobbling it could prevent the bot from scoring
                    else:
                        if (c, r) not in untouchable_row_pieces[line_color]:
                            untouchable_row_pieces[line_color].append((c, r))

    #Checks rows
    for row in range(4):
        process_line([(col, row) for col in range(4)])

    #Checks columns
    for col in range(4):
        process_line([(col, row) for row in range(4)])
        
    #Generates the line coordinates for the diagonals
    diagonals = [
        [(i, i) for i in range(4)],
        [(i, 3 - i) for i in range(4)]
    ]

    #Checks diagonals
    for diag in diagonals:
        process_line(diag)

    return potential_moves, untouchable_row_pieces

#Finds the largest valid piece in the bot's playerboard by checking each top piece in the stacks for the largest one and returns that coordinate
def find_playerboard_piece(player_dark):

    largest_piece_pos = None
    largest_piece_size = -1

    for stack_pos in range(3):

        top_piece = player_dark.check_top_piece(stack_pos)

            top_piece = player_dark.check_top_piece(stack_pos)

            if top_piece.size > largest_piece_size:
                largest_piece_size = top_piece.size
                largest_piece_pos = stack_pos
    
    return largest_piece_pos

#Finds the largest valid piece on the gameboard by checking every piece on the board for one that does not allow a win for the player if moved
def find_gameboard_piece(game_board, player_light, player_dark, potential_moves, untouchable_row_pieces):

    largest_piece = None
    largest_piece_size = 0

    #Adds the pieces that are a part of the 3 in a line(s) (potential blocks/scores and the untouchables)
    # to a complete list of coordinates to avoid for picking pieces
    avoid_coords = (
        potential_moves.get(player_dark.color, []) + potential_moves.get(player_light.color, []) +
        untouchable_row_pieces.get(player_dark.color, []) + untouchable_row_pieces.get(player_light.color, [])
    )

    #Iterates through every piece on the gameboard:
    for col in range(4):
        for row in range(4):

            #Skips piece if it is part of the coordinates to be avoided
            if (col, row) in avoid_coords:
                continue

            piece = game_board.check_top_piece(col, row)

            #Skips piece if it is size 0 (empty) or not the color of the bot
            if piece.size == 0 or (piece.color != player_dark.color):
                continue

            #Simulates lifting the piece to check for wins and near wins
            removed_piece = game_board.get_piece(col, row)

            is_win, winner_player = check_win(game_board)
            
            new_moves, new_untouchables = find_3_in_a_line(game_board, player_dark, player_light)

            uncovered_player_threat = ((col, row) in new_moves.get(player_light.color, []))

            #If there is not a win and moving the piece did not reveal a player piece
            if not is_win and not uncovered_player_threat:

                #If the piece is a size 4 (the largest) then stop checking for a larger one
                if piece.size == 4:
                    largest_piece = (col, row)
                    largest_piece_size = piece.size
                    game_board.put_piece(col, row, removed_piece)
                    break
                
                #If the piece is larger than the current largest piece then it is now the largest piece
                elif piece.size > largest_piece_size:
                    largest_piece = (col, row)
                    largest_piece_size = piece.size

            game_board.put_piece(col, row, removed_piece)

    return largest_piece

#Finds the largest possible piece for the bot to use for blocking/scoring
def find_largest_piece(game_board,
                       potential_moves, 
                       player_light, 
                       player_dark, 
                       untouchable_row_pieces):

    found_piece = None

    #If the 3 in a line is the bot:
    if potential_moves[player_dark.color]:

        #If all the possible move pieces are not empty spots:
        if all(game_board.check_top_piece(coord[0], coord[1]).size > 0 for coord in potential_moves[player_dark.color]):

            #Only pick a piece from the gameboard because a piece played from the playerboard
            # cannot gobble another piece unless it is to block the other player

            gameboard_coord = find_gameboard_piece(game_board, player_light, player_dark, potential_moves, untouchable_row_pieces)
            gameboard_size = game_board.check_top_piece(gameboard_coord[0], gameboard_coord[1]).size if gameboard_coord is not None else 0
            
            if gameboard_size > 0:
                found_piece = gameboard_coord

        #If there is an empty spot:
        else:

            #Check the playerboard & the gameboard and use whichever piece is larger

            playerboard_stack = find_playerboard_piece(player_dark)
            playerboard_size = player_dark.check_top_piece(playerboard_stack).size if playerboard_stack is not None else 0

            gameboard_coord = find_gameboard_piece(game_board, player_light, player_dark, potential_moves, untouchable_row_pieces)
            gameboard_size = game_board.check_top_piece(gameboard_coord[0], gameboard_coord[1]).size if gameboard_coord is not None else 0

            if playerboard_size >= gameboard_size and playerboard_size > 0:
                found_piece = playerboard_stack
            elif gameboard_size > 0:
                found_piece = gameboard_coord
    

    #If the 3 in a line is the player:
    elif potential_moves[player_light.color]:

        #Check the playerbaord & the gameboard and use whichever piece is larger
        #Because the opponent is being blocked the bot can gobble using a piece from the playerboard

        playerboard_stack = find_playerboard_piece(player_dark)
        playerboard_size = player_dark.check_top_piece(playerboard_stack).size if playerboard_stack is not None else 0

        gameboard_coord = find_gameboard_piece(game_board, player_light, player_dark, potential_moves, untouchable_row_pieces)
        gameboard_size = game_board.check_top_piece(gameboard_coord[0], gameboard_coord[1]).size if gameboard_coord is not None else 0

        if playerboard_size >= gameboard_size and playerboard_size > 0:
            found_piece = playerboard_stack
        elif gameboard_size > 0:
            found_piece = gameboard_coord

    return found_piece

#Moves the largest piece for blocking/winning if it is from the gameboard & larger than the piece at the target coordinates
def moves_largest_gameboard_piece(bot_targets, game_board, largest_piece_pos, player_dark):

    large_col, large_row = largest_piece_pos
    move = False

    for move in bot_targets:
        col_down, row_down = move

        if game_board.check_top_piece(large_col, large_row).size > game_board.check_top_piece(col_down, row_down).size:
            moved_piece = game_board.get_piece(large_col, large_row)
            game_board.put_piece(col_down, row_down, moved_piece)
            record_moves(player_dark.color.name, 'game_board', large_col, large_row, col_down, row_down)
            moved = True
            break

    #If the largest piece was not placed, then it can't be 
    return moved

#Moves the largest piece for blocking/winning if it is from the playerboard & larger than the piece at the target coordinates
def moves_largest_playerboard_piece(bot_targets, player_board, game_board, largest_piece_pos, is_scoring_turn, player_dark):

    moved = False

    for move in bot_targets:
                
        col_down, row_down = move
        target_size = game_board.check_top_piece(col_down, row_down).size

        #If its the bot trying to win and the target space is not empty then the bot can't play
        #The check for placing the piece is then skipped
        if is_scoring_turn and target_size > 0:
            continue

        #If the largest selected piece is bigger than the target piece:
        if player_board.check_top_piece(largest_piece_pos).size > target_size:

            moved_piece = player_board.get_piece(largest_piece_pos)
            game_board.put_piece(col_down, row_down, moved_piece)
            record_moves(player_dark.color.name, 'player_board', largest_piece_pos, 0, col_down, row_down)
            moved = True
            break
    
    #If the largest piece was not placed, then it can't be 

    return moved     

#Plays out a random turn for the bot
def random_bot_turn(game_board, player_dark):

    while True:

        full_playerboard = False
        empty_playerboard = False
        
        #Checks if the bot's playerboard is full or empty

        if all(player_dark.check_top_piece(stack).size == 4 for stack in range(3)):
            full_playerboard = True
        
        if all(player_dark.check_top_piece(stack).size == 0 for stack in range(3)):
            empty_playerboard = True

        #Sets the options for which board is chosen and the chances per board
        # (True/False is for the selecting the playerboard)
        options = [True, False]
        # (So a 90% chance of selecting from the playerboard and a 10% for the gameboard)
        weights = [90, 10]

        #If the playerboard is full then a piece cannot be selected from the gameboard 
        # and is automatically selected from the playerboard
        if full_playerboard:
            select_playerboard = True

        #If the playerboard is empty then a piece cannot be selected from the playerboard 
        # and is automatically selected from the gameboard
        elif empty_playerboard:
            select_playerboard = False
        
        #If there are no restrictions on where the bot can pick from then the board is selected randomly
        else:
            select_playerboard = random.choices(options, weights = weights, k=1)[0]


        picked_piece_preview = None

        #If the selected board was the playerboard:
        if select_playerboard:

            #Randomly pick a stack 

            rand_stack = random.randint(0, 2)
                                        
            #Check that the stack is not empty
            if player_dark.check_top_piece(rand_stack).size > 0:
                picked_piece_preview = player_dark.check_top_piece(rand_stack)

            #If it is then choose another random piece
            else:
                continue
            
        #If the selected board was the gameboard:
        else:

            #Randomly select coordinates on the gameboard
            rand_col_pick = random.randint(0, 3)
            rand_row_pick = random.randint(0, 3)
            gameboard_target = game_board.check_top_piece(rand_col_pick, rand_row_pick)

            #Check that there is a piece at those coordinates and that it is a bot piece
            if gameboard_target.size > 0 and gameboard_target.color == player_dark.color:
                picked_piece_preview = game_board.check_top_piece(rand_col_pick, rand_row_pick)
            
            #If it is empty or a player piece then choose another random piece
            else:
                continue

        #Randomly selects coordinates on the gameboard for putting down the piece
        rand_col_put = random.randint(0, 3)
        rand_row_put = random.randint(0, 3)
        target_preview = game_board.check_top_piece(rand_col_put, rand_row_put)

        #If the selected pick up piece is larger than the piece at the put down coordinates:
        if picked_piece_preview.size > target_preview.size:

            #If the selected board was playerboard then take the piece from there
            if select_playerboard:
                actual_piece = player_dark.get_piece(rand_stack)
                record_moves(player_dark.color.name, 'player_board', rand_stack, 0, rand_col_put, rand_row_put)
            #If the selected board was gameboard then take the piece from there
            else:
                actual_piece = game_board.get_piece(rand_col_pick, rand_row_pick)
                record_moves(player_dark.color.name, 'game_board', rand_col_pick, rand_row_pick, rand_col_put, rand_row_put)
            
            #Puts down the piece
            game_board.put_piece(rand_col_put, rand_row_put, actual_piece)

            is_win, winner = check_win(game_board)
            is_near_win, near_win_player = check_near_win(game_board)

            #If moving the piece creates a 3 or 4 in a line:
            if is_win or is_near_win:

                game_board.get_piece(rand_col_put, rand_row_put)

                #Put the piece back where it came from
                if select_playerboard:
                    player_dark.player_stacks[rand_stack].append(actual_piece)

                else:
                    game_board.put_piece(rand_col_pick, rand_row_pick, actual_piece)

                continue

            break

#Reassigns values to the color values for sorting
# in order of white, empty, black
piece_color_order = {
    'light': 0,
    'initial': 1,
    'dark': 2
}

#Returns a tuple of (sorting color value, size) to sorts moves first by color, then by size in decending order
def check_for_sort(game_board, color_order, coord):

    piece = game_board.check_top_piece(coord[0], coord[1])

    color = piece.color.name
    size = piece.size

    color_sort = color_order.get(color, 99)

    return (color_sort, -size)

#Executes the bot's turn
def do_bot_turn(game_board, player_light, player_dark):

    #Retrieves the potential block/win moves 
    potential_moves, untouchable_row_pieces = find_3_in_a_line(game_board, player_dark, player_light)

    #Prefills the parameters for the check_for_sort function so it only needs a coordinate for sorting
    moves_sort = partial(
        check_for_sort, 
        game_board,
        piece_color_order,
        )

    #Creates a list of target coordinates for winning & sorts it
    dark_bot_targets = potential_moves[player_dark.color]
    dark_bot_targets.sort(key=moves_sort)

    #Creates a list of target coordinates for blocking & sorts it
    light_bot_targets = potential_moves[player_light.color]
    light_bot_targets.sort(key=moves_sort)

    #Retrieves the coordinate for the largest available piece for blocking/winning
    largest_piece_pos = find_largest_piece(game_board, potential_moves, player_light, player_dark, untouchable_row_pieces)

    move_executed = False

    #If there was a piece selected:
    if largest_piece_pos is not None:

        #If it is a gameboard coordinate:
        if isinstance(largest_piece_pos, tuple):

            #If the bot can win:
            if dark_bot_targets:

                #Try to win using largest piece from the gameboard
                move_executed = moves_largest_gameboard_piece(dark_bot_targets, game_board, largest_piece_pos, player_dark)
                
            #If the player needs to be blocked:
            elif light_bot_targets:

                #Try to block using largest piece from the gameboard
                move_executed = moves_largest_gameboard_piece(light_bot_targets, game_board, largest_piece_pos, player_dark)

            #If the move was not fully executed, then it is not possible and a random move is completed
            if not move_executed:
                random_bot_turn(game_board, player_dark)

        #If it is a playerboard coordinate:
        elif isinstance(largest_piece_pos, int):

            #If the bot can win:
            if dark_bot_targets:

                #Try to win using largest piece from the playerboard
                move_executed = moves_largest_playerboard_piece(dark_bot_targets, player_dark, game_board, largest_piece_pos, True, player_dark)
                
            #If the player needs to be blocked:
            elif light_bot_targets:

                #Try to block using largest piece from the playerboard
                move_executed = moves_largest_playerboard_piece(light_bot_targets, player_dark, game_board, largest_piece_pos, False, player_dark)

            #If the move was not fully executed, then it is not possible and a random move is completed
            if not move_executed:
                random_bot_turn(game_board, player_dark)
    
    #If there was no largest piece meaning there is no 3 in a line,
    # then complete a random move
    else:
        print('no 3 in a row, check for 2 in a row')

        dark_2_targets = find_2_in_a_line(game_board, player_dark)
        untouchable_row_pieces = {player_dark.color: [], player_light.color: []}

        if dark_2_targets:

            mock_potential_moves = {
                player_dark.color: dark_2_targets,
                player_light.color: []
            }

            largest_piece_pos_2 = find_largest_piece(
                game_board, mock_potential_moves, player_light, player_dark,
                untouchable_row_pieces
            )

            print(f'pick up for 2 in a row at {largest_piece_pos_2}')

            if largest_piece_pos_2 is not None:
                if isinstance(largest_piece_pos_2, tuple):
                    #Try to win using largest piece from the gameboard
                    move_executed = moves_largest_gameboard_piece(dark_2_targets, game_board, largest_piece_pos_2)

                elif isinstance(largest_piece_pos_2, int):
                    #Try to win using largest piece from the playerboard
                    move_executed = moves_largest_playerboard_piece(dark_2_targets, player_dark, game_board, largest_piece_pos_2, is_scoring_turn = False)

    if not move_executed:
        print('no 3 or 2 in a row, going random')
        random_bot_turn(game_board, player_dark)
