
import sys, pygame
pygame.init()
pygame.font.init()

from Gobblet_Functions import *

screen_width = 600
screen_height = 550

clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))

#colors:
dark_color = (89, 13, 34)
med_color = (179, 20, 65)
off_white = (255, 204, 213)

dark_piece_color = (118, 5, 37)
dark_out_color = (138, 3, 42)

light_piece_color = (250, 82, 113)
light_out_color = (235, 58, 90)

blank_out_color = (163, 18, 59)
blank_piece_color = (148, 19, 56)

gen_circs = []

board_size = 320
square_size = board_size / 4 #80

offset_x = 20
offset_y = (screen_height - board_size) / 2 #(440 - 320) / 2 = 60

player_zones_gap = 15
stack_gap = 20
center_shift = 20

border_thickness = 10

border_rect = pygame.Rect(offset_x - border_thickness, offset_y - border_thickness,
    board_size + (border_thickness * 2), board_size + (border_thickness * 2))

basic_font = pygame.font.SysFont('Nunito', 36)

# Gameboard ----------------------------------------------------------------

gameboard_zones = []
for col in range(4):
    col_zones = []
    for row in range(4):
        
        x = col * square_size + offset_x
        y = row * square_size + offset_y
        
        col_zones.append(pygame.Rect(x, y, square_size, square_size))
    gameboard_zones.append(col_zones)

gamebord_centers = []
for col in range(4):
    col_centers = []
    for row in range(4):
        
        x = ((col + 0.5) * square_size) + offset_x
        y = ((row + 0.5) * square_size) + offset_y
        
        col_centers.append((x, y))
    gamebord_centers.append(col_centers)

def gen_zones_gameboard():

    pygame.draw.rect(screen, (134, 9, 50), border_rect, 0)

    for col in range(4):
        for row in range(4):

            color = dark_color if (row + col) % 2 == 0 else off_white
            pygame.draw.rect(screen, color, gameboard_zones[col][row])

def draw_piece_for_gameboard(player_color_value, size, position):

    piece_radius = size * 9
    col, row = position

    piece_pos = gamebord_centers[col][row]

    if player_color_value == 2: 
        piece_color = dark_piece_color
        line_color = dark_out_color
    
    elif player_color_value == 1:
        piece_color = light_piece_color
        line_color = light_out_color

    pygame.draw.circle(screen, piece_color, piece_pos, piece_radius, 0)
    pygame.draw.circle(screen, line_color, piece_pos, piece_radius, 7)

def draw_gameboard_pieces(game_board):

    for col in range(4):
        for row in range(4):

            piece = game_board.check_top_piece(col, row)

            if piece.size != 0:

                draw_piece_for_gameboard(piece.color.value, piece.size, (col, row))

# Playerboard ----------------------------------------------------------------

player_dark_zones = []
for stack in range(3):
    
    x = stack * (square_size + stack_gap) + offset_x + center_shift
    y = offset_y - border_thickness - square_size - player_zones_gap
    
    player_dark_zones.append(pygame.Rect(x, y, square_size, square_size))

player_dark_centers = []
for stack in range(3):
    
    x = (stack * (square_size + stack_gap)) + (square_size * 0.5) + offset_x + center_shift
    y = offset_y - border_thickness - (square_size * 0.5) - player_zones_gap

    player_dark_centers.append((x, y))

player_light_zones = []
for stack in range(3):

    x = stack * (square_size + stack_gap) + offset_x + center_shift
    y = offset_y + border_thickness + player_zones_gap + board_size
    
    player_light_zones.append(pygame.Rect(x, y, square_size, square_size))

player_light_centers = []
for stack in range(3):
    
    x = (stack * (square_size + stack_gap)) + (square_size * 0.5) + offset_x + center_shift
    y = offset_y + border_thickness + (square_size * 0.5) + player_zones_gap + board_size

    player_light_centers.append((x, y))

def draw_playerboard_piece(player_color_value, size, position):

    piece_radius = size * 9

    if player_color_value == 2:
        piece_pos = player_dark_centers[position]
    elif player_color_value == 1:
        piece_pos = player_light_centers[position]

    if player_color_value == 2: 
        piece_color = dark_piece_color
        line_color = dark_out_color
    
    elif player_color_value == 1:
        piece_color = light_piece_color
        line_color = light_out_color

    pygame.draw.circle(screen, piece_color, piece_pos, piece_radius, 0)
    pygame.draw.circle(screen, line_color, piece_pos, piece_radius, 7)

def draw_dark_playerboard(player_dark):

    for stack in range(3):

        piece = player_dark.check_top_piece(stack)

        if piece.size != 0:

            draw_playerboard_piece(piece.color.value, piece.size, stack)

def draw_light_playerboard(player_light):

    for stack in range(3):

        piece = player_light.check_top_piece(stack)

        if piece.size != 0:

            draw_playerboard_piece(piece.color.value, piece.size, stack)

# Player Turn ----------------------------------------------------------------

def draw_selected_piece(selected_piece):

    x = screen_width - 125
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

def player_mouse_click(mouse_pos, game_board, current_player, player_light, 
    picking_piece, selected_piece, col_up, row_up, piece_source_board):
    
    move_completed = False

    clicked_zone_type = None
    col_clicked, row_clicked, stack_clicked = None, None, None

    for col in range(4):
        for row in range(4):
            if gameboard_zones[col][row].collidepoint(mouse_pos):
                col_clicked, row_clicked = col, row
                clicked_zone_type = 'game_board'
                break

    if clicked_zone_type is None:
        for stack in range(3):
            if player_light_zones[stack].collidepoint(mouse_pos):
                stack_clicked = stack
                clicked_zone_type = 'player_board'
                break

    if clicked_zone_type is not None:
        if picking_piece:
            pick_result = player_piece_pick(game_board, player_light, col_clicked, row_clicked, stack_clicked, clicked_zone_type)

            if pick_result:
                selected_piece, col_up, row_up, piece_source_board = pick_result
                picking_piece = False

        elif not picking_piece:
            
            move_executed = player_piece_put(game_board, player_light, selected_piece, col_up, row_up, col_clicked, row_clicked, piece_source_board)

            if move_executed:
                move_completed = True
                picking_piece = True
                selected_piece = None

                #Records current game move
                record_moves(current_player.color.name, piece_source_board, col_up, row_up, col_clicked, row_clicked)

    return move_completed, picking_piece, selected_piece, col_up, row_up, piece_source_board