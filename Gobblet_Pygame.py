
import sys, pygame
pygame.init()
pygame.font.init()

screen_width = 600
screen_height = 550

clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))

#colors:
dark_color = (89, 13, 34)
med_color = (164, 19, 60)
off_white = (255, 204, 213)

dark_out_color = (181, 18, 64)
light_out_color = (250, 82, 113)

dark_piece_color = (128, 15, 47)
light_piece_color = (230, 53, 85)

gen_circs = []

board_size = 320
square_size = board_size / 4 #80

offset_x = 20
offset_y = (screen_height - board_size) / 2 #(440 - 320) / 2 = 60

# Gameboard ----------------------------------------------------------------

gameboard_zones = []
for row in range(4):
    for col in range(4):
        
        x = col * square_size + offset_x
        y = row * square_size + offset_y
        
        gameboard_zones.append(pygame.Rect(x, y, square_size, square_size))

gamebord_centers = []
for col in range(4):
    col_centers = []
    for row in range(4):
        
        x = ((col + 0.5) * square_size) + offset_x
        y = ((row + 0.5) * square_size) + offset_y
        
        col_centers.append((x, y))
    gamebord_centers.append(col_centers)

border_thickness = 10

border_rect = pygame.Rect(offset_x - border_thickness, offset_y - border_thickness,
    board_size + (border_thickness * 2), board_size + (border_thickness * 2))

def gen_zones_gameboard():

    pygame.draw.rect(screen, (134, 9, 50), border_rect, 0)

    for i, zone in enumerate(gameboard_zones):
    
        row = i // 4
        col = i % 4
        
        color = dark_color if (row + col) % 2 == 0 else off_white
        pygame.draw.rect(screen, color, zone)

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

player_zones_gap = 15
stack_gap = 20
center_shift = 20

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
    y = offset_y + border_thickness + square_size + player_zones_gap + board_size
    
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