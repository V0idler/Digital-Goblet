
#Imports & intializes pygame
import sys, pygame
pygame.init()
pygame.font.init()

#Imports from functions file
from Gobblet_Functions import *

#Variable Intialization----------------------------------------------------------------

#Screen dimentions 
screen_side = 600
screen_mid = screen_side / 2 # 600 / 2 = 300

#Clock & screen
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_side, screen_side))

#colors-----------------
dark_color = (89, 13, 34)
med_color = (179, 20, 65)
off_white = (255, 204, 213)

dark_piece_color = (99, 4, 71)
dark_out_color = (120, 2, 83)

back_board_color = (134, 9, 50)

light_piece_color = (250, 107, 82)
light_out_color = (235, 88, 58)

blank_out_color = (163, 18, 59)
blank_piece_color = (148, 19, 56)
#-----------------

#Board dimentions
board_size = 320
square_size = board_size / 4 #80

#X and Y offset values for drawing
offset_x = 20
offset_y = (screen_side - board_size) / 2 #(440 - 320) / 2 = 60

#Other offsets for drawing
player_zones_gap = 15
stack_gap = 20
center_shift = 20
border_thickness = 10
in_adjust = border_thickness * 2 # 20

#Fonts & text string
basic_font = pygame.font.SysFont('Nunito', 36)
large_font = pygame.font.SysFont('Nunito', 120)

game_over_text = basic_font.render(f'Game Over', True, off_white)

#Menu----------------------------------------------------------------

#Prints text explaining the rules of the game
game_rules_text = [
    "Welcome to Gobblet! Select the button ",
    "for continuing a previous game or ",
    "starting a new one. To win, Get 4 ",
    "pieces in a row! But, pieces can be ",
    "gobbled so think carefully! Once a game ",
    "has ended, click the restart button",
    "to play again."
    ]

#Draws the game rule text
def draw_rules():

    rules_text_y = 400
    rules_text_x = screen_mid - 230 # 300 - 230 = 70

    for i, line in enumerate(game_rules_text):
        text_current_y = rules_text_y + (i * 25)
        game_text_render = basic_font.render(line, True, off_white)
        screen.blit(game_text_render, (rules_text_x, text_current_y))

#Draws the menu text & buttons
def draw_menu():

    base_width = 210
    base_height = 100

    base_x = screen_mid
    base_y = screen_mid - (base_height / 2) # 300 - (100 / 2) = 250

    game_label = basic_font.render(f'Game', True, off_white)

    upper_text_y = base_y + 23 # 250 + 23 = 273
    lower_text_y = base_y + 53 # 250 + 53 = 303

    #Menu Text-------------------------------

    menu_x = screen_mid - 120 # 300 - 120 = 180
    menu_y = screen_mid - 145 # 300 - 145 = 155

    menu_label = large_font.render(f'Menu', True, off_white)
    screen.blit(menu_label, (menu_x, menu_y))

    draw_rules()

    #Load Button-------------------------------

    load_x = base_x - base_width # 300 - 210 = 90

    load_rect_out = pygame.Rect(load_x, base_y, base_width, base_height)
    load_rect_in = pygame.Rect(load_x + border_thickness, base_y + border_thickness, base_width - in_adjust, base_height - in_adjust)

    pygame.draw.rect(screen, blank_out_color, load_rect_out)
    pygame.draw.rect(screen, blank_piece_color, load_rect_in)

    load_label = basic_font.render(f'Load Previous', True, off_white)
    screen.blit(load_label, (load_x + 20, upper_text_y))
    screen.blit(game_label, (load_x + 70, lower_text_y))

    #New Game Button-------------------------------

    newgame_x = base_x + 10 # 300 + 10 = 310

    reset_rect_out = pygame.Rect(newgame_x, base_y, base_width, base_height)
    reset_rect_in = pygame.Rect(newgame_x + border_thickness, base_y + border_thickness, base_width - in_adjust, base_height - in_adjust)

    pygame.draw.rect(screen, blank_out_color, reset_rect_out)
    pygame.draw.rect(screen, blank_piece_color, reset_rect_in)

    reset_label = basic_font.render(f'Start New', True, off_white)
    screen.blit(reset_label, (newgame_x + 50, upper_text_y))
    screen.blit(game_label, (newgame_x + 70, lower_text_y))

    return load_rect_out, reset_rect_out

#Draws the restart button
def draw_restart_button():
    base_width = 210
    base_height = 70

    button_x = 370
    button_y = offset_y + border_thickness + player_zones_gap + board_size + 15
    # 60 + 10 + 15 + 320 + 15 = 420

    restart_rect_out = pygame.Rect(button_x, button_y, base_width, base_height)
    restart_rect_in = pygame.Rect(button_x + border_thickness, button_y + border_thickness, base_width - in_adjust, base_height - in_adjust)

    pygame.draw.rect(screen, back_board_color, restart_rect_out)
    pygame.draw.rect(screen, dark_color, restart_rect_in)

    restart_label = basic_font.render(f'Restart Game', True, off_white)
    screen.blit(restart_label, (button_x + 25, button_y + 23))

    return restart_rect_out

#Draws the banner when there is a win in the winner's piece color
def draw_win_text(winner_color, player_dark, player_light):

    base_width = 190
    base_height = 105

    button_x = 375
    button_y = 200

    if winner_color == player_dark.color.name:
        button_out_color = dark_out_color
        button_in_color = dark_piece_color
    elif winner_color == player_light.color.name:
        button_out_color = light_out_color
        button_in_color = light_piece_color

    winner_rect_out = pygame.Rect(button_x, button_y, base_width, base_height)
    winner_rect_in = pygame.Rect(button_x + border_thickness, button_y + border_thickness, base_width - in_adjust, base_height - in_adjust)

    pygame.draw.rect(screen, button_out_color, winner_rect_out)
    pygame.draw.rect(screen, button_in_color, winner_rect_in)

    screen.blit(game_over_text, (button_x + 30, button_y + 15))

    winner_is_text = basic_font.render(f'Winner is:', True, off_white)
    screen.blit(winner_is_text, (button_x + 35, button_y + 40))

    winner_text = basic_font.render(f'{winner_color.capitalize()}', True, off_white)
    screen.blit(winner_text, (button_x + 65, button_y + 65))

#Draws the banner when there is a tie 
def draw_tie_text():

    base_width = 190
    base_height = 85

    button_x = 375
    button_y = 200

    tie_rect_out = pygame.Rect(button_x, button_y, base_width, base_height)
    tie_rect_in = pygame.Rect(button_x + border_thickness, button_y + border_thickness, base_width - in_adjust, base_height - in_adjust)

    pygame.draw.rect(screen, back_board_color, tie_rect_out)
    pygame.draw.rect(screen, dark_color, tie_rect_in)

    screen.blit(game_over_text, (button_x + 30, button_y + 15))

    is_tie_text = basic_font.render(f"It's a Tie!", True, off_white)
    screen.blit(is_tie_text, (button_x + 42, button_y + 40))

#Draws message displayed when there is no autosave
def draw_no_autosave():

    auto_x = screen_mid - 230 # 300 - 230 = 70
    auto_y = screen_mid + 70 # 300 + 70 = 370

    autosave_text = basic_font.render(f'No autosave, start new game.', True, off_white)
    screen.blit(autosave_text, (auto_x, auto_y))

# Gameboard ----------------------------------------------------------------

#Generates gameboard zones for detecting clicks
gameboard_zones = []
for col in range(4):
    col_zones = []
    for row in range(4):
        
        x = col * square_size + offset_x
        y = row * square_size + offset_y
        
        col_zones.append(pygame.Rect(x, y, square_size, square_size))
    gameboard_zones.append(col_zones)

#Generates gameboard zone centers for drawing circle pieces
gamebord_centers = []
for col in range(4):
    col_centers = []
    for row in range(4):
        
        x = ((col + 0.5) * square_size) + offset_x
        y = ((row + 0.5) * square_size) + offset_y
        
        col_centers.append((x, y))
    gamebord_centers.append(col_centers)

#Draws the gameboard zones in a checkerboard pattern based on if the coordinates are even or odd
def gen_zones_gameboard():
    
    border_rect = pygame.Rect((offset_x - border_thickness), (offset_y - border_thickness),
        (board_size + (border_thickness * 2)), (board_size + (border_thickness * 2)))

    pygame.draw.rect(screen, back_board_color, border_rect, 0)

    for col in range(4):
        for row in range(4):

            color = dark_color if (row + col) % 2 == 0 else off_white
            pygame.draw.rect(screen, color, gameboard_zones[col][row])

#Draws a piece for when it is on the gameboard
def draw_piece_for_gameboard(player_color_name, size, position):

    piece_radius = size * 9
    col, row = position

    piece_pos = gamebord_centers[col][row]

    if player_color_name == 'dark': 
        piece_color = dark_piece_color
        line_color = dark_out_color
    
    elif player_color_name == 'light':
        piece_color = light_piece_color
        line_color = light_out_color

    pygame.draw.circle(screen, piece_color, piece_pos, piece_radius, 0)
    pygame.draw.circle(screen, line_color, piece_pos, piece_radius, 7)

#Draws all of the current pieces on the gameboard
def draw_gameboard_pieces(game_board):

    for col in range(4):
        for row in range(4):

            piece = game_board.check_top_piece(col, row)

            if piece.size != 0:

                draw_piece_for_gameboard(piece.color.name, piece.size, (col, row))

# Playerboard ----------------------------------------------------------------

#Generates player dark zone centers for drawing circle pieces
# (zones are only required to detecting mouse clicks, so the bot doesn't need them)
player_dark_centers = []
for stack in range(3):
    
    x = (stack * (square_size + stack_gap)) + (square_size * 0.5) + offset_x + center_shift
    y = offset_y - border_thickness - (square_size * 0.5) - player_zones_gap - 10

    player_dark_centers.append((x, y))

#Generates player light player board zones for detecting clicks
player_light_zones = []
for stack in range(3):

    x = stack * (square_size + stack_gap) + offset_x + center_shift
    y = offset_y + border_thickness + player_zones_gap + board_size + 10
    
    player_light_zones.append(pygame.Rect(x, y, square_size, square_size))

#Generates player light zone centers for drawing circle pieces
player_light_centers = []
for stack in range(3):
    
    x = (stack * (square_size + stack_gap)) + (square_size * 0.5) + offset_x + center_shift
    y = offset_y + border_thickness + (square_size * 0.5) + player_zones_gap + board_size + 10

    player_light_centers.append((x, y))

#Draws a piece for when it is on a playerboard
def draw_playerboard_piece(player_color_name, size, position):

    piece_radius = size * 9

    if player_color_name == 'dark':

        piece_pos = player_dark_centers[position]
        piece_color = dark_piece_color
        line_color = dark_out_color

    elif player_color_name == 'light':

        piece_pos = player_light_centers[position]
        piece_color = light_piece_color
        line_color = light_out_color

    pygame.draw.circle(screen, piece_color, piece_pos, piece_radius, 0)
    pygame.draw.circle(screen, line_color, piece_pos, piece_radius, 7)

#Draws the current state of the dark playerboard
def draw_dark_playerboard(player_dark):

    for stack in range(3):

        piece = player_dark.check_top_piece(stack)

        if piece.size != 0:

            draw_playerboard_piece(piece.color.name, piece.size, stack)

#Draws the current state of the light playerboard
def draw_light_playerboard(player_light):

    for stack in range(3):

        piece = player_light.check_top_piece(stack)

        if piece.size != 0:

            draw_playerboard_piece(piece.color.name, piece.size, stack)

#Draws the background for the playerboards
def draw_playerboard_backing():

    back_x_out = offset_x - border_thickness
    light_y_out = offset_y + border_thickness + board_size + 10
    dark_y_out = offset_y - border_thickness - square_size - 40

    base_rect_height = square_size + 30
    base_rect_width = board_size + (border_thickness * 2)

    #Outer Rectangles--------------------------------

    light_out_rect = pygame.Rect(back_x_out, light_y_out, base_rect_width, base_rect_height)
    dark_out_rect = pygame.Rect(back_x_out, dark_y_out, base_rect_width, base_rect_height)

    pygame.draw.rect(screen, blank_out_color, light_out_rect)
    pygame.draw.rect(screen, blank_out_color, dark_out_rect)

    #Inner Rectangles--------------------------------

    light_in_rect = pygame.Rect(back_x_out + border_thickness, light_y_out + border_thickness, base_rect_width - in_adjust, base_rect_height - in_adjust)
    dark_in_rect = pygame.Rect(back_x_out + border_thickness, dark_y_out + border_thickness, base_rect_width - in_adjust, base_rect_height - in_adjust)

    pygame.draw.rect(screen, blank_piece_color, light_in_rect)
    pygame.draw.rect(screen, blank_piece_color, dark_in_rect)

# Player Turn ----------------------------------------------------------------

#Draws the player's current selected piece & background
def draw_selected_piece(selected_piece):

    x = screen_side - 125 # 300 - 125 = 175
    y = 100

    blank_radius = 50

    pygame.draw.circle(screen, blank_piece_color, (x, y), blank_radius, 0)
    pygame.draw.circle(screen, blank_out_color, (x, y), blank_radius, 7)

    if selected_piece and selected_piece.size !=0:

        piece_radius = selected_piece.size * 9

        pygame.draw.circle(screen, light_piece_color, (x, y), piece_radius, 0)
        pygame.draw.circle(screen, light_out_color, (x, y), piece_radius, 7)
  
    selected_piece_label = basic_font.render(f'Current Piece:', True, off_white)
    screen.blit(selected_piece_label, (395, 20))

#Processes the player's pick up selection
def player_piece_pick(game_board, player_light, col_clicked, row_clicked, stack_clicked, which_board):

    selected_piece = None
    col_up, row_up = None, None

    if which_board == 'game_board':
        top_piece = game_board.check_top_piece(col_clicked, row_clicked)

        if top_piece.size > 0 and top_piece.color == player_light.color:
            selected_piece = game_board.get_piece(col_clicked, row_clicked)
            col_up, row_up = col_clicked, row_clicked
            which_board = 'game_board'

    elif which_board == 'player_board':
        top_piece = player_light.check_top_piece(stack_clicked)

        if top_piece.size > 0:
            selected_piece = player_light.get_piece(stack_clicked)
            col_up = stack_clicked
            row_up = 0

    return (selected_piece, col_up, row_up, which_board) if selected_piece else None

#Processes the player's put down selection
def player_piece_put(game_board, player_light, selected_piece, col_up, row_up, col_down, row_down, which_board):

    board_piece = game_board.check_top_piece(col_down, row_down)
    move_executed = False

    if which_board == 'game_board':
        if (col_up, row_up) != (col_down, row_down) and selected_piece.size > board_piece.size:
            game_board.put_piece(col_down, row_down, selected_piece)
            record_moves(player_light.color.name, which_board, col_up, row_up, col_down, row_down)
            move_executed = True
        
    elif which_board == 'player_board':
        if board_piece.size == 0:
            game_board.put_piece(col_down, row_down, selected_piece)
            move_executed = True

    return move_executed

#Plays out the player's turn
def player_mouse_click(mouse_pos, game_board, current_player, player_light, 
    picking_piece, selected_piece, col_up, row_up, piece_source_board):
    
    move_completed = False

    clicked_zone_type = None
    col_clicked, row_clicked, stack_clicked = None, None, None

    #Checks if piece was selected on the gameboard
    for col in range(4):
        for row in range(4):
            if gameboard_zones[col][row].collidepoint(mouse_pos):
                col_clicked, row_clicked = col, row
                clicked_zone_type = 'game_board'
                break

    #If the piece was not selected on the gameboard:
    # checks if the piece was selected on the playerboard
    if clicked_zone_type is None:
        for stack in range(3):
            if player_light_zones[stack].collidepoint(mouse_pos):
                stack_clicked = stack
                clicked_zone_type = 'player_board'
                break

    #If the player clicked on a valid zone:
    if clicked_zone_type is not None:
        #If the player is picking up a piece:
        if picking_piece:
            pick_result = player_piece_pick(game_board, player_light, col_clicked, row_clicked, stack_clicked, clicked_zone_type)

            #Checks that the piece is in a valid zone before processing
            # if it is not then the loop requires that the player choose again
            if pick_result:
                selected_piece, col_up, row_up, piece_source_board = pick_result
                picking_piece = False

        #If the player is putting down a piece:
        elif not picking_piece:
            #If the player clicked on the gameboard:
            if clicked_zone_type == 'game_board':
            
                move_executed = player_piece_put(game_board, player_light, selected_piece, col_up, row_up, col_clicked, row_clicked, piece_source_board)

                #If the put down location was confirmed to be valid, then the move was done sucessfully:
                # set variables as such
                if move_executed:
                    move_completed = True
                    picking_piece = True
                    selected_piece = None

                    #Records current game move
                    record_moves(current_player.color.name, piece_source_board, col_up, row_up, col_clicked, row_clicked)
            
            #If the player clicked somewhere that is not the gameboard:
            # then the loop requires that the player choose again
            else:
                move_executed = False

    #Returns all required variables
    return move_completed, picking_piece, selected_piece, col_up, row_up, piece_source_board