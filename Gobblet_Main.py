
#Imports other files
from Gobblet_Classes import *
from Gobblet_Functions import *
from Gobblet_Bot_Functions import *
from Gobblet_Pygame import *
import random
import json

import sys, pygame
pygame.init()

def setup_newgame():
    player_light = player_board_class(player_color_class.light)
    player_dark = player_board_class(player_color_class.dark)

    game_board = game_board_class()

    return player_light, player_dark, game_board

def load_json():
    
    with open("gameboard1.json", "r") as file:
        game_data = json.load(file)
    
    player_light, player_dark, game_board = setup_newgame()
    
    current_player = player_dark

    game_board.reinitialize_from_json(game_data["gameboard"])

    player_light.reinitialize_from_json(game_data["playerboard1"])
    player_dark.reinitialize_from_json(game_data["playerboard2"])

    return player_light, player_dark, game_board, current_player

print_program_instructions()

#player_light, player_dark, game_board, current_player = load_json()

menu_active = True

#Loop asking if the players want to load the game, continues until a valid input is entered
while menu_active:

    clock.tick(60)

    screen.fill(med_color)

    load_button, newgame_button = draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if load_button.collidepoint(mouse_pos):

                game_board, player_light, player_dark, current_player = load_game()

                #player_light, player_dark, game_board, current_player = load_json()

                menu_active = False
                break
            
            #If player does not want to load game, generates new game objects 
            # using classes and asks for a starting player color
            if newgame_button.collidepoint(mouse_pos):
            
                player_light, player_dark, game_board = setup_newgame()
                current_player = random.choice((player_light, player_dark))

                menu_active = False
                break


    pygame.display.flip()

picking_piece = True
selected_piece = None
col_up, row_up = None, None
piece_source_board = None
game_active = True

#Plays out game until a player wins
while True:

    clock.tick(60)
    move_completed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if restart_button.collidepoint(mouse_pos):
                player_light, player_dark, game_board = setup_newgame()
                current_player = random.choice((player_light, player_dark))
                game_active = True

            if game_active and current_player == player_light:
                move_completed, picking_piece, selected_piece, col_up, row_up, piece_source_board = player_mouse_click(
                    mouse_pos, game_board, current_player, player_light, picking_piece, selected_piece, col_up, row_up, piece_source_board)
        
    if game_active and current_player == player_dark:

        do_bot_turn(game_board, player_light, player_dark)
        move_completed = True

        pygame.time.delay(500)

    if move_completed:

        #Switches who's turn it is to whoever's turn it is currently not
        current_player = player_dark if current_player == player_light else player_light

        #Saves game automatically after every turn
        save_game(game_board, player_light, player_dark, current_player)

    screen.fill(med_color)
    gen_zones_gameboard()
    draw_gameboard_pieces(game_board)
    draw_playerboard_backing()
    draw_dark_playerboard(player_dark)
    draw_light_playerboard(player_light)
    draw_selected_piece(selected_piece)
    restart_button = draw_restart_button()

    if_win, winner_color = check_win(game_board)

    #If a win is detected, end the game loop
    if if_win:
        game_active = False

    if not game_active:
        draw_game_over_text(winner_color, player_dark, player_light)

    #If a tie is detected, print a such and end the game loop
    if check_tie(move_history):
        print('Game Over!')
        print('Players Tied!')
        break


    pygame.display.flip()