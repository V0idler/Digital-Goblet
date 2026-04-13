
from Gobelt_Classes import *
from Goblet_Functions import *

print_program_instructions()

#Loop asking if the players want to load the game, continues until a valid input is entered
while True:

    saved_game = input('Load saved game? (y/n) ').lower()

    #If player wants to load game, plays out load game function which retrives previous game state
    if saved_game == 'y':
        game_board, player_light, player_dark, current_player = load_game(full_path)
        print('Loading saved game.')
        break

    #If player does not want to load game, generates new game objects using classes and asks for a starting player color
    elif saved_game == 'n':
        print('Initializing new game.')
        
        player_light = player_board_class(player_color_class.light)
        player_dark = player_board_class(player_color_class.dark)

        game_board = game_board_class()

        current_player = select_start_player(player_light, player_dark)
        break

#Plays out game until a player wins
while True:

    #Prints current game state
    print_game_board(game_board)
    print_player_board(player_light)
    print_player_board(player_dark)

    #Picks up piece at the location selected by the player
    game_piece = player_pick(game_board, current_player)
    
    #Puts down piece at location selected by the player
    player_put(game_piece, game_board, current_player)

    #Switches who's turn it is to whoever's turn it is currently not
    current_player = player_dark if current_player == player_light else player_light

    #Saves game automatically after every turn
    save_game(full_path, game_board, player_light, player_dark, current_player)

    #If a win is detected, plays out function for a detected win and ends the game loop
    if detect_win(game_board):
        break

    

