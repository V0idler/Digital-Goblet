
#Imports other files
from Gobblet_Classes import *
from Gobblet_Functions import *
from Gobblet_Bot_Functions import *
from Gobblet_Pygame import *

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
player_light, player_dark, game_board = setup_newgame()
current_player = player_light

'''
#Loop asking if the players want to load the game, continues until a valid input is entered
while True:

    saved_game = input('Load saved game? (y/n) ').lower()

    #If player wants to load game, plays out load game function which retrieves previous game state
    if saved_game == 'y':
        
        print('Loading saved game.')
        #game_board, player_light, player_dark, current_player = load_game()

        player_light, player_dark, game_board, current_player = load_json()

        break

    #If player does not want to load game, generates new game objects using classes and asks for a starting player color
    elif saved_game == 'n':
        print('Initializing new game.')
       
        player_light, player_dark, game_board = setup_newgame()
        current_player = select_start_player(player_light, player_dark)
        
        break
'''
picking_piece = True
selected_piece = None
col_up, row_up = None, None
piece_source_board = None


#Plays out game until a player wins
while True:

    clock.tick(60)
    move_completed = False

    if current_player == player_light:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                move_completed, picking_piece, selected_piece, col_up, row_up, piece_source_board = player_mouse_click(
                    mouse_pos, game_board, current_player, player_light, picking_piece, selected_piece, col_up, row_up, piece_source_board)
            
    else:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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
    draw_dark_playerboard(player_dark)
    draw_light_playerboard(player_light)
    draw_selected_piece(selected_piece)

    #If a win is detected, plays out function for a detected win and ends the game loop
    if detect_win(game_board):
        #break
        print(' ')

    #If a tie is detected, print a such and end the game loop
    if check_tie(move_history):
        print('Game Over!')
        print('Players Tied!')
        break


    pygame.display.flip()