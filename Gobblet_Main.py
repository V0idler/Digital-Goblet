
#Imports other files
from Gobblet_Classes import *
from Gobblet_Functions import *
from Gobblet_Bot_Functions import *
from Gobblet_Pygame import *
#Imports module & system
import random
import sys, pygame
pygame.init()

#Sets menu as active
menu_active = True
#Intializes the no autosave text to False
autosave_text = False

#Loop asking if the players want to load the game, continues until a valid input is entered
while menu_active:

    clock.tick(60)

    #Draws the menu screen
    screen.fill(med_color)
    load_button, newgame_button = draw_menu()
    #If the load button was clicked, but there is no autosave:
    if autosave_text:
        #Display message stating as such
        draw_no_autosave()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #Checks for mouse click events
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            #If the load button was clicked:
            #Load new previous game if it exists,
            # if there is no previous game, displays message saying as such
            if load_button.collidepoint(mouse_pos):

                load_result = load_game()
                if load_result is None:
                    autosave_text = True
                else:
                    game_board, player_light, player_dark, current_player = load_result
                    menu_active = False

                break
            
            #If player does not want to load game, creates new game
            if newgame_button.collidepoint(mouse_pos):
            
                player_light, player_dark, game_board = setup_newgame()
                current_player = random.choice((player_light, player_dark))

                picking_piece = True
                selected_piece = None
                col_up = None
                col_down = None
                piece_source_board = None
                move_history.clear()

                menu_active = False
                break


    pygame.display.flip()

#Initializes required variables
picking_piece = True
selected_piece = None
col_up, row_up = None, None
piece_source_board = None
game_active = True
game_won = False
game_tied = False

#Plays out game until a player wins
while True:

    clock.tick(60)

    #Intializes move completion and draws restart button
    move_completed = False
    screen.fill(med_color)
    restart_button = draw_restart_button()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #Checks for mouse click events
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            #If the restart button was clicked:
            # creates new game and resets variables
            if restart_button.collidepoint(mouse_pos):
                player_light, player_dark, game_board = setup_newgame()
                current_player = random.choice((player_light, player_dark))
                game_active = True
                game_won = False
                game_tied = False
                picking_piece = True
                selected_piece = None
                col_up = None
                col_down = None
                piece_source_board = None
                move_history.clear()

            #If the game is currently happening and it is the player's turn:
            # carries out the player's turn
            if game_active and current_player == player_light:
                move_completed, picking_piece, selected_piece, col_up, row_up, piece_source_board = player_mouse_click(
                    mouse_pos, game_board, current_player, player_light, picking_piece, selected_piece, col_up, row_up, piece_source_board)
    
    #If the game is currently happening and it is the bot's turn:
    # carries out the bot's turn with a starting delay
    if game_active and current_player == player_dark:

        pygame.time.delay(500)

        do_bot_turn(game_board, player_light, player_dark)
        move_completed = True

    #If a move was completed:
    if move_completed:

        #Switches who's turn it is to whoever's turn it is currently not
        current_player = player_dark if current_player == player_light else player_light

        #Saves game automatically after every turn
        save_game(game_board, player_light, player_dark, current_player)

    #Draws the entire gameboard
    gen_zones_gameboard()
    draw_gameboard_pieces(game_board)
    draw_playerboard_backing()
    draw_dark_playerboard(player_dark)
    draw_light_playerboard(player_light)
    draw_selected_piece(selected_piece)

    #Checks if there is a win
    if_win, winner_color = check_win(game_board)

    #If a win is detected, the game is no longer active
    if if_win:
        game_active = False
        game_won = True

    #If a tie is detected, the game is no longer active
    if check_tie(move_history):
        game_active = False
        game_tied = True

    #If the game is not currently active:
    if not game_active:
        #And the game was won:
        if game_won:
            #Draws win text
            draw_win_text(winner_color, player_dark, player_light)
        #And the game was tied:
        elif game_tied:
            #Draws tie text
            draw_tie_text()

    pygame.display.flip()