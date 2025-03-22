# 2024-09-15
import os


class Game_Ops:
    """Singleton class handling game-data logic.

       |   |            |   |
     0 | 1 | 2          |   | X
    ___|___|___      ___|___|___
       |   |            |   |
     3 | 4 | 5        O | X | O
    ___|___|___      ___|___|___
       |   |            |   |
     6 | 7 | 8          |   |
       |   |            |   |

    Binary representation of board-state:
        876543210
    Digits represent the corresponding location (see diagram).
    Example of the board-state on the right would be
        Player X: 000010100
        Player O: 000101000
    Both board-states will be stored as two integers in a list.

    Input can be handled by OR-ing a left-shifted 1-bit with the player's board-state.
    For instance, player X would like to input into location 6:
        000010100 OR 1<<6 = 000010100 OR 001000000 = 001010100.
        => 20 | (1 << 6) = 84.

    Input can be checked for existing symbols in both board-states by using the AND operator and checking if 0:
        000010100 & (1 << 4) != 0 => symbol already exists in that location.

    Win conditions can be checked by taking the states and using the AND operator with a specific list of integers. For instance, to check the 2-4-6 diagonal:
        000010100 & 001010100 = 000010100 => 20 & 84 = 20.
        101010100 & 001010100 = 001010100 => 340 & 84 = 84 => win.
    Win conditions are:
        [0b000000111, 0b000111000, 0b111000000, 0b001001001, 0b010010010, 0b100100100, 0b100010001, 0b001010100]
        = [7, 56, 448, 73, 146, 292, 273, 84].
    Pseudo:
        for winNum in [7, 56, 448, 73, 146, 292, 273, 84]:
            if player0State & winNum == winNum:
                win = True
    or:
        if any(player0State & winNum == winNum for winNum in [7, 56, 448, 73, 146, 292, 273, 84]):
            win = True

    Programmes can then interface with this class to either read its information or manipulate the data using class methods.
    """
    _instance = None

    def __new__(cls):
        """Singleton constructor.
        return: class instance of Game_Ops.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            return cls._instance
        else:
            print('Instance of \'Game_Ops\' already exists.')
            return cls._instance

    def __init__(self):
        """Initialize values.
        """
        self.boardStates  = [0, 0]
        self.playerCount  = 0
        self.turnCount    = 0

    def insert_index(self, insertIndex):
        """Insert a digit for a player into the board-state of that player using the OR operator.
        """
        self.boardStates[self.playerCount] = self.boardStates[self.playerCount] | (1 << insertIndex)

    def is_in_board_state(self, insertIndex):
        """Check if a location is already occupied by checking the index with the board-state.
        Number 1 is left-shifted by insertIndex amount of times. Then the board-state is AND-ed with this number.
        If the result is 0, then the location is free, or put another way, if not zero, then this returns true.
        Since there exist 2 board-states, one for each player, any() will be used to check both board-states with the insertIndex.
        return: bool.
        """
        return any(boardState & (1 << insertIndex) != 0 for boardState in self.boardStates)

    def is_win(self):
        """Here the board-state for the current playerCount is checked against a predetermined set of integers defining 
        the win conditions. If boardState AND one of these integers returns the same integer, a win condition is met.
        return: bool.
        """
        return any(self.boardStates[self.playerCount] & winNum == winNum for winNum in [7, 56, 448, 73, 146, 292, 273, 84])

    def update_player_count(self):
        """Since there are only two players, the counter which keeps track of which player the turn belongs to
        can simply be incremented by 1 before being modded by 2, such that the counter is always either 0 or 1.
        """
        self.playerCount = (self.playerCount + 1) % 2

    def update_turn(self, num):
        """Simply add 1 to the turn counter.
        """
        self.turnCount += num


def frontend_pre_game():
    """Ask of players which symbols they would like to use.
    return: list of symbols ordered by players.
    """
    symbols = [input('Player 0 symbol: '), input('Player 1 symbol: ')]
    return symbols


def clearScreen():
    """Clear console screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def frontend_draw_board(symbols):
    """Here a docstring is defined for the basic playfield graphic which is later populated by the corresponding values.
    This function translates the integer data in the Game_Ops class to symbols and displays them in the graphic.
    This is done by first defining a list of 'empty' cells (spaces), which are later filled up by the symbols from
    frontend_pre_game(). The binary data from the Game_Ops class is translated to a 9-character binary string where the indices of
    the '1' digits are noted in reverse for each player's board-state. In reverse because the index counter of strings counts in the
    reverse order of the index counter of the playfield. Then the corresponding positions in the boardData list are
    replaced by the player symbols. Finally, the resulting data is formatted into the basic graphic and displayed.
    Note: Graphic makes use of unicode superscript symbols.
    """
    clearScreen()
    boardGraphic  = '\n\u2070  |\u00b9  |\u00b2  \n {0} | {1} | {2} \n___|___|___\n\u00b3  |\u2074  |\u2075  \n {3} | {4} | {5} \n___|___|___\n\u2076  |\u2077  |\u2078  \n {6} | {7} | {8} \n   |   |   \n'
    # boardGraphic  = '\n0  |1  |2  \n {0} | {1} | {2} \n___|___|___\n3  |4  |5  \n {3} | {4} | {5} \n___|___|___\n6  |7  |8  \n {6} | {7} | {8} \n   |   |   \n'
    boardData     = [' '] * 9

    player0BinStr = bin(Game_Ops.boardStates[0])[2:].zfill(9)
    player1BinStr = bin(Game_Ops.boardStates[1])[2:].zfill(9)

    boardIndices  = [[8 - i for i, v in enumerate(player0BinStr) if v == '1'], [8 - i for i, v in enumerate(player1BinStr) if v == '1']]
    for n, playerIndices in enumerate(boardIndices):
        for i in playerIndices:
            boardData[i] = symbols[n]

    print(boardGraphic.format(*boardData))


def frontend_ask_input(symbols):
    """This function asks the player for the index of the location they would like to insert their symbol in.
    This input must be a number in the interval [0, 8], which is checked. It is then checked whether a symbol
    is already there by asking the Game_Ops class to perform the necessary AND operation as described in the
    corresponding function.
    return: Index of the location in which the player would like to insert their symbol.
    """
    while True:
        inputIndex = input(f'Player {symbols[Game_Ops.playerCount]}; input location index: ')

        if inputIndex not in [f'{i}' for i in range(0, 9)]:
            print('Please choose a number between 0 and 8.')
            continue

        insertIndex = int(inputIndex)
        if Game_Ops.is_in_board_state(insertIndex):
            print('There is already a symbol there. Please input an index corresponding to a free location.')
        else:
            return insertIndex


def main():
    """Main function which handles pre-, inter-, and post-turn logic. The programme exits when a winner is detected and declared.
    If no winner is detected after 9 turns the programme declares a draw before exiting, as the while condition
    handling inter-turn game logic will no longer be met.
    """
    frontend_draw_board([' ', ' '])
    symbols = frontend_pre_game()

    while Game_Ops.turnCount < 9:
        frontend_draw_board(symbols)
        insertIndex = frontend_ask_input(symbols)

        Game_Ops.insert_index(insertIndex)

        if Game_Ops.is_win():
            frontend_draw_board(symbols)
            print(f'Player {symbols[Game_Ops.playerCount]} won!')
            exit()

        Game_Ops.update_player_count()
        Game_Ops.update_turn(1)

    frontend_draw_board(symbols)
    print('It\'s a draw!')


if __name__ == '__main__':
    Game_Ops = Game_Ops()
    main()
