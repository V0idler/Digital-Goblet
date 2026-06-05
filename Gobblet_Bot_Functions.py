
from itertools import combinations 
from functools import partial
from Gobblet_Functions import check_win, check_near_win, record_moves
import random

#Checks for multiple pieces in a line------------------------------------

#Checks if there is a 2 in a line for the bot without player pieces and returns the appropriate coordinates for adding to the line
def find_2_in_a_line(game_board, player_dark):

    potential_moves = []
    untouchable_row_pieces = []

    #Processes the current line to be checked for 2 in a line using the coordinates passed in for the line
    #Such that piece's other than the bot's are a size less than 4
    def process_line(line_coords):
        pieces = [game_board.check_top_piece(c, r) for c, r in line_coords]

        dark_pieces = []
        small_piece_coords = []

        #Collects coordinates for the bot's pieces and the 
        # player's piece which are less than size 4 or empty spots
        for coord, piece in zip(line_coords, pieces):
            if piece.color == player_dark.color:
                dark_pieces.append(coord)
            elif piece.size < 4:
                small_piece_coords.append(coord)

        #If there are 2 bot pieces in a row and 2 pieces less than 4:
        if len(dark_pieces) == 2 and len(small_piece_coords) == 2:
            #Then the coordinates for the small peices are added to potential moves
            for coord in small_piece_coords:
                if coord not in potential_moves:
                    potential_moves.append(coord)
            #And the coordinates are added to a list of coordinates to not be touched during this turn
            for coord in dark_pieces:
                if coord not in untouchable_row_pieces:
                    untouchable_row_pieces.append(coord) 

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

#Checks if there is a 3 in a line for the bot or player and returns the appropriate coordinates for blocking/winning
def find_3_in_a_line(game_board, player_dark, player_light):

    potential_moves = {player_dark.color: [], player_light.color: []}
    untouchable_row_pieces = {player_dark.color: [], player_light.color: []}

    #Processes the current line to be checked for 3 in a line using the coordinates passed in for the line
    def process_line(line_coords):

        #Checks every possible combination of 3 coordinates within the line of 4 coordinates
        for line_combos in combinations(line_coords, 3):

            pieces = [game_board.check_top_piece(c, r) for c, r in line_combos]

            #If the 3 pieces in the line combo are not size 0 (empty) and are the same color:
            if all(piece.size != 0 for piece in pieces) and all(piece.color == pieces[0].color for piece in pieces):

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

                    #If the 3 in a line is the player and a piece within the line is less than size 4
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

#Finds and moves the largest available piece------------------------------------

#Finds the largest valid piece in the bot's playerboard by 
# checking each top piece in the stacks for the largest one and returns that coordinate
def find_playerboard_piece(player_dark):
    largest_piece_pos = None
    largest_piece_size = -1
    for stack_pos in range(3):
        top_piece = player_dark.check_top_piece(stack_pos)
        if top_piece.size > largest_piece_size:
            largest_piece_size = top_piece.size
            largest_piece_pos = stack_pos
    return largest_piece_pos

#Finds the largest valid piece on the gameboard by checking every piece on the board
# for one that does not allow a win for the player if moved
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

            #Checks if the revealed piece is on a coordinate for blocking a 3 in a row from the player
            # (revealed a player piece that is part of a 3 in a row)
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

            #Puts the piece down to stop simulating picking it up
            game_board.put_piece(col, row, removed_piece)

    return largest_piece

#Finds the largest possible piece for the bot to use for blocking/scoring
def find_largest_piece(game_board,
                       potential_moves, 
                       player_light, 
                       player_dark, 
                       untouchable_row_pieces,
                       two_in_a_line):

    found_piece = None

    #If the line is the bot:
    if potential_moves[player_dark.color]:

        #If all the possible move pieces are not empty spots:
        if all(game_board.check_top_piece(coord[0], coord[1]).size > 0 for coord in potential_moves[player_dark.color]):

            #Finds a piece from the gameboard
            gameboard_coord = find_gameboard_piece(game_board, player_light, player_dark, potential_moves, untouchable_row_pieces)
            gameboard_size = game_board.check_top_piece(gameboard_coord[0], gameboard_coord[1]).size if gameboard_coord is not None else 0
            
            #Finds a piece from the playerboard
            playerboard_stack = find_playerboard_piece(player_dark)
            playerboard_size = player_dark.check_top_piece(playerboard_stack).size if playerboard_stack is not None else 0

            #If it is to add to a 2 in a line:
            if two_in_a_line:
                #Then compare the playerboard and gamboard piece options and use the largest one
                if playerboard_size >= gameboard_size and playerboard_size > 0:
                    found_piece = playerboard_stack
                elif gameboard_size > 0:
                    found_piece = gameboard_coord
            #If it is to add to a 3 in a line, then just use the gameboard option
            #Because you can't use a piece from the playerboard for winning, only blocking
            else:
                if gameboard_size > 0:
                    found_piece = gameboard_coord

        #If there is an empty spot:
        else:

            #Check the playerboard & the gameboard 

            playerboard_stack = find_playerboard_piece(player_dark)
            playerboard_size = player_dark.check_top_piece(playerboard_stack).size if playerboard_stack is not None else 0

            gameboard_coord = find_gameboard_piece(game_board, player_light, player_dark, potential_moves, untouchable_row_pieces)
            gameboard_size = game_board.check_top_piece(gameboard_coord[0], gameboard_coord[1]).size if gameboard_coord is not None else 0

            #Use whichever found piece is larger
            if playerboard_size >= gameboard_size and playerboard_size > 0:
                found_piece = playerboard_stack
            elif gameboard_size > 0:
                found_piece = gameboard_coord
    

    #If the line is the player:
    elif potential_moves[player_light.color]:

        #Check the playerbaord & the gameboard
        #Because the opponent is being blocked the bot can gobble using a piece from the playerboard

        playerboard_stack = find_playerboard_piece(player_dark)
        playerboard_size = player_dark.check_top_piece(playerboard_stack).size if playerboard_stack is not None else 0

        gameboard_coord = find_gameboard_piece(game_board, player_light, player_dark, potential_moves, untouchable_row_pieces)
        gameboard_size = game_board.check_top_piece(gameboard_coord[0], gameboard_coord[1]).size if gameboard_coord is not None else 0

        #Use whichever found piece is larger
        if playerboard_size >= gameboard_size and playerboard_size > 0:
            found_piece = playerboard_stack
        elif gameboard_size > 0:
            found_piece = gameboard_coord

    return found_piece

#Moves the largest piece for blocking/winning if it is from the gameboard 
def moves_largest_gameboard_piece(bot_targets, game_board, largest_piece_pos, player_dark):

    large_col, large_row = largest_piece_pos
    moved = False

    for move in bot_targets:
        col_down, row_down = move

        #If the largest selected piece is bigger than the target piece:
        if game_board.check_top_piece(large_col, large_row).size > game_board.check_top_piece(col_down, row_down).size:
            #Puts down the piece and records the move
            moved_piece = game_board.get_piece(large_col, large_row)
            game_board.put_piece(col_down, row_down, moved_piece)
            record_moves(player_dark.color.name, 'game_board', large_col, large_row, col_down, row_down)
            moved = True
            break

    #Returns if the move was sucessfull
    return moved

#Moves the largest piece for blocking/winning if it is from the playerboard 
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
            #Puts down the piece and records the move
            moved_piece = player_board.get_piece(largest_piece_pos)
            game_board.put_piece(col_down, row_down, moved_piece)
            record_moves(player_dark.color.name, 'player_board', largest_piece_pos, 0, col_down, row_down)
            moved = True
            break

    #Returns if the move was sucessfull
    return moved     

#For playing out various bot turn senarios------------------------------------

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
        # (So a 90% chance of selecting from the playerboard and a 10% chance for the gameboard)
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

            #Randomly picks a stack 
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

        #If the selected pick up board was the player board and the pick up and put down coordinates are the same:
        if not select_playerboard and (rand_col_pick, rand_row_pick) == (rand_col_put, rand_row_put):
            #Then continue to try another random turn
            continue

        #If the put down coordinates are not the same as the pick up coordinates,
        # then assign a target put down preview
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

            #Checks for win/near win(s)
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

                #Continues to try another random turn
                continue

            #If moving the piece did not create a 3 or 4 in a line, then the turn is complete and the loop is ended
            break

#Key for sorting the possibles moves, 
# reassigns the color names to the values required for sorting,
# in order of white, empty, black
color_order = {
    'light': 0,
    'initial': 1,
    'dark': 2
}

#Returns a tuple of (sorting color, size) for sorting potential moves 
def move_key(game_board, color_order, coord):
    piece = game_board.check_top_piece(coord[0], coord[1])
    #Returns the new value for the color of the piece,
    # and flips the size value for sorting in ascending order
    return (color_order.get(piece.color.name, 99), -piece.size)

#Insertion sort for sorting potential moves in order first by color, then by size in acending order
def potential_moves_sort(potential_moves, game_board):
    #Loop through the list staring from the second item
    for current_index in range(1, len(potential_moves)):

        #Saves the current move being sorted
        current_move = potential_moves[current_index]
        #Gets the correct sorting data for the current move
        current_piece_info = move_key(game_board, color_order, current_move)

        #Sets up an index for the item to the left of the current one
        prev_index = current_index - 1

        #Shifts moves to the right if they are larger than the current piece info
        # (While the current position is after the first position
        # and the move info at the previous position is larger than the current move info)
        while prev_index >= 0 and move_key(game_board, color_order, potential_moves[prev_index]) > current_piece_info:

            #Shifts the larger move info to the right
            potential_moves[prev_index + 1] = potential_moves[prev_index]
            #Move previous index to the left to check the next move
            prev_index -= 1

        #Inserts the original move into its correct sorted position
        potential_moves[prev_index + 1] = current_move

#Executes the bot's turn
def do_bot_turn(game_board, player_light, player_dark):

    #Retrieves the potential block/win moves 
    potential_moves, untouchable_row_pieces = find_3_in_a_line(game_board, player_dark, player_light)

    #Creates a list of target coordinates for winning & sorts it
    dark_bot_targets = potential_moves[player_dark.color]
    potential_moves_sort(dark_bot_targets, game_board)

    #Creates a list of target coordinates for blocking & sorts it
    light_bot_targets = potential_moves[player_light.color]
    potential_moves_sort(light_bot_targets, game_board)

    #Retrieves the coordinate for the largest available piece for blocking/winning
    largest_piece_pos = find_largest_piece(game_board, potential_moves, player_light, player_dark, untouchable_row_pieces, False)

    #Initializes if move executed
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
    
    #If there were no possible moves for a 3 in a line:
    # then check if there is a 2 in a line to add to
    if not move_executed:

        #Retrieves & sorts the potential moves for adding to the 2 in a row
        dark_2_targets, untouchable_2_pieces = find_2_in_a_line(game_board, player_dark)
        potential_moves_sort(dark_2_targets, game_board)
        #Adds the new list of untouchable pieces to the new dictionary of untouchable pieces
        # (this only checks for the bot, so the player has no untouchable pieces)
        untouchable_row_pieces = {player_dark.color: untouchable_2_pieces, player_light.color: []}

        #If there is a 2 in a line for the bot:
        if dark_2_targets:

            #Creates a dictionary for possible moves
            # (but there are none for blocking the player)
            mock_potential_moves = {
                player_dark.color: dark_2_targets,
                player_light.color: []
            }

            #Retrieves the coordinate for the largest available piece for adding to a 2 in a line
            largest_piece_pos_2 = find_largest_piece(game_board, mock_potential_moves, player_light, player_dark, untouchable_row_pieces, True)

            #If there was a piece selected:
            if largest_piece_pos_2 is not None:

                #If it is from the gameboard:
                if isinstance(largest_piece_pos_2, tuple):
                    #Try to add using largest piece from the gameboard
                    move_executed = moves_largest_gameboard_piece(dark_2_targets, game_board, largest_piece_pos_2, player_dark)

                #If it is from the playerboard:
                elif isinstance(largest_piece_pos_2, int):
                    #Try to add using largest piece from the playerboard
                    move_executed = moves_largest_playerboard_piece(dark_2_targets, player_dark, game_board, largest_piece_pos_2, False, player_dark)

    #If there were no possible moves for 3 or 2 in a lines then play out a random turn
    if not move_executed:
        random_bot_turn(game_board, player_dark)
