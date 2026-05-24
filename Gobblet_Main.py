
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

player_light, player_dark, game_board, current_player = load_json()

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

#Plays out game until a player wins
while True:

    clock.tick(60)

    screen.fill(med_color)

    gen_zones_gameboard()

    draw_gameboard_pieces(game_board)
    draw_dark_playerboard(player_dark)
    draw_light_playerboard(player_light)

    #Prints current game state
    print_game_board(game_board)
    print_player_board(player_light)
    print_player_board(player_dark)

    if current_player == player_light:

        #Picks up piece at the location selected by the player
        game_piece, col_up, row_up, which_board = check_piece_pick(game_board, current_player)
    
        #Prints current game state
        print_game_board(game_board)
        print_player_board(player_light)
        print_player_board(player_dark)

        #Puts down piece at location selected by the player
        col_down, row_down = check_piece_put(game_piece, game_board, current_player, col_up, row_up, which_board)

        #Records current game move
        record_moves(current_player.color.name, which_board, col_up, row_up, col_down, row_down)
    
    else:

        do_bot_turn(game_board, player_light, player_dark)

    #Switches who's turn it is to whoever's turn it is currently not
    current_player = player_dark if current_player == player_light else player_light

    #Saves game automatically after every turn
    save_game(game_board, player_light, player_dark, current_player)

    #If a win is detected, plays out function for a detected win and ends the game loop
    if detect_win(game_board):
        #break
        print(' ')

    #If a tie is detected, print a such and end the game loop
    if check_tie(move_history):
        print_game_board(game_board)
        print('Game Over!')
        print('Players Tied!')
        break


    pygame.display.flip()