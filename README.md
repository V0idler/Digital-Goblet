# Digital-Goblet

    This is a digital version of the game Gobblet programed in VS Code as a text based local 2 player game.

# Game Rules:

Goal: To be the first player to get 4 pieces in a row. The first player who does this wins.

Important:
    You can 'gobble' (put a piece on top of another) your opponent's pieces or your own, as long as the piece getting gobbled is smaller than the one gobbling it.
    When you add a new piece to the board from a player stack it must be put on an empty spot on the game board.
        *Exception: your opponent already has 3 pieces in a row, then you can gobble up a piece.
    You can move any piece you want on the game board (even if it is currently gobbling another piece), or you can add a piece to the game board from one of your stacks.
    When adding pieces to the game board they are taken from the player stacks in order from largest to smallest.
    Once you pick up a piece you have to move it, you cannot put it back down in the same place and you don't get to undo your turn and try again.
    The game is considered a tie when both players have made the same move of moving a piece back & forth between 2 locations on the board 3 times. Other than that it is up to the players to determine a tie.


Turns:
    During your turn you play one piece, you can either add a new piece to (an empty spot on) the game board from your stacks or move a piece that is already on the game board to an empty spot or gobble up a piece.

# Program Instructions:

1. First it asks you if you want to load from an autosave
2. Typing 'y' will load the last autosave from the previous game and the game will continue from there. 
3. If 'n' is entered then the program will ask which color wants to start, if 'l' is entered then purple starts, if 'd' is entered then green starts. 
4. Whoever was entered to start goes first, the program will ask for an input of where you want to pick up your piece.
5. If a letter a, b or c is entered then the piece is picked up from the player board of the current player.
6. If a coordinate of (0, 0) to (3, 3) (entered as eg: 00) is entered then the player picks up a piece that has already been played on the game board.
7. After a piece is picked up the program will print the current game board without the picked up piece, then it will ask for an input of where the player would like to put down the piece.
8. For putting down a piece the input can only be a coordinate (for the game board).
9. After the current player has successfully picked up and put down a piece then their turn is over and it switches to the next player's turn.
10. The program continues running in a loop until a player wins or the game is tied and then it is stopped.
