# Digital-Goblet

    This is a digital version of the game Gobblet programed in VS Code as a graphics based local 1 player vs bot game.

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

    1. Pressing the load button will load the last autosave from the previous game and the game will continue from there. 
    2. If the start new game button is clicked then the program will start a new game where
    the first player is randomly selected.
    3. When it is the player's turn then they will click on the spot where they want to
    pick up their piece.
    4. After a piece is picked up the program will display the current piece in the top right.
    5. For putting down a piece the player clicks where they want to put it down.
    6. If the player tries to place a piece in an invalid location then the piece is not put down and the program waits for them to try again.
    7. After the current player has successfully picked up and put down a piece then their turn is over and it switches to the bot's turn.
    8. The bot's turn is entirely automatic.
    9. The program continues running in a loop until a player wins or the game is tied and then it is stopped.
