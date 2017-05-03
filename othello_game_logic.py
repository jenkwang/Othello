#Jenny Chong 23733553 Lab Section 8

NONE = 0
BLACK = 'B'
WHITE = 'W'

class InvalidMoveError(Exception):
    '''Raised when an invalid move is made'''
    pass

class GameOverError(Exception):
    '''Raised when game is over but attempt to make a move occurs'''
    pass

class GameState():
    def __init__(self, rows: int, columns: int, first_turn: str, win_method: str):
        self._rows = rows
        self._columns = columns
        self._board = self.new_board()
        self._turn = first_turn
        self._score = self.score()
        self._win_type = win_method
        self._player_peices = []
    
    def new_board(self):
        '''Creates an empty board'''
        board = []
        for r in range(self._rows):
            board.append([])
            for c in range(self._columns):
                board[r].append(0)
        return board

    def board_arrangement(self):
        '''Creates the board initialized by user'''
        for r in range(len(self._board)):
            element = input()
            self._board[r] = element.split()
        return self._board

    def switch_turn(self):
        '''Changes turn when function is called'''
        if self._turn == BLACK:
            return WHITE
        else:
            return BLACK

    def score(self): 
        '''Counts the total points of each player and puts it in a list attribute'''
        black = 0
        white = 0
        for r in range(len(self._board)):
            for c in range(len(self._board[r])):
                if self._board[r][c] == BLACK:
                    black += 1
                elif self._board[r][c] == WHITE:
                    white += 1
        self._score = [str(black), str(white)]

    def player_peices(self):
        '''Creates a list of all cells a player has occupied'''
        player_peices = []
        for r in range(len(self._board)):
            for c in range(len(self._board[r])):
                if self._board[r][c] == self._turn:
                    player_peices.append([r, c])
        return player_peices

    def require_game_not_over(self):
        '''Checks to make sure that a player can still make a move'''
        if self.get_all_peices(self.player_peices(), self.check_for_valid_move) == []:
            self._turn = self.switch_turn()
            if self.get_all_peices(self.player_peices(), self.check_for_valid_move) == []:
                raise GameOverError
            else:
                return True
        else:
            return True
                       
    def make_move(self, cell: str):
        '''Flips peices after checking if move made is valid'''
        #row_col = cell.split()
        row = int(cell[0])
        col = int(cell[1])
        move = [row, col]
        if move in self.get_all_peices(self.player_peices(), self.check_for_valid_move):
            self._board[move[0]][move[1]] = self._turn
            for peice in self.get_all_peices([move], self.start_flips):
                self._board[peice[0]][peice[1]] = self._turn
            self._turn = self.switch_turn()
            return True
        else:
            raise InvalidMoveError
        
    def winner(self) -> str:
        '''Returns the winner depending on win type'''
        if self._win_type == '>':
            if int(self._score[0]) > int(self._score[1]):
                return BLACK
            elif int(self._score[0]) < int(self._score[1]):
                return WHITE
            else:
                return 'NONE'
        elif self._win_type == '<':
            if int(self._score[0]) > int(self._score[1]):
                return WHITE
            elif int(self._score[0]) < int(self._score[1]):
                return BLACK
            else:
                return 'NONE'
    
    def start_flips(self, start_cell: list, drow: int, dcol: int):
        '''Creates a list of the peices to flip'''
        row = start_cell[0]
        col = start_cell[1]
        opponent = self.switch_turn()
        i = 1
        peices = []
        try:
            while self._is_valid_row_number(row + drow * i) \
               and self._is_valid_column_number(col + dcol * i) \
               and self._board[row + drow * i][col + dcol * i] == opponent: 
                i += 1
                if self._is_valid_row_number(row + drow * i) \
                   and self._is_valid_column_number(col + dcol * i) \
                   and self._board[row + drow * i][col + dcol * i] == self._turn:
                    for x in range(1,i):
                        peices.append([row + drow * (i-x), col + dcol * (i-x)])
                else:
                    continue
        except IndexError: #accounts for the row/column out of range
            pass
       
        return peices

    def check_for_valid_move(self, player_peice: list, drow: int, dcol: int):
        '''Checks for possible valid moves a player can make'''
        row = int(player_peice[0])
        col = int(player_peice[1])
        opponent = self.switch_turn()
        i = 1
        valid_moves = []
        try:
            while self._is_valid_row_number(row + drow * i) \
               and self._is_valid_column_number(col + dcol * i) \
               and self._board[row + drow * i][col + dcol * i] == opponent:
                i += 1
                if self._is_valid_row_number(row + drow * i) \
                   and self._is_valid_column_number(col + dcol * i) \
                   and self._board[row + drow * i][col + dcol * i] == 0:
                    valid_moves.append([row + drow * i, col + dcol * i])
                else:
                    continue
        except IndexError: #accounts for the row/column out of range
            pass    
        return valid_moves

    def get_all_peices(self, peices_or_moves, function) -> list:
        '''
        Creates a list of all peices that are valid or to flip
        after checking all 8 directions
        '''
        all_peices = []
        for i in peices_or_moves:
            all_peices.extend(function(i, 0, 1))
            all_peices.extend(function(i, 1, 1))
            all_peices.extend(function(i, 1, 0))
            all_peices.extend(function(i, 1, -1))
            all_peices.extend(function(i, 0, -1))
            all_peices.extend(function(i, -1, -1))
            all_peices.extend(function(i, -1, 0))
            all_peices.extend(function(i, -1, 1))   
        return all_peices          

    def _is_valid_row_number(self, row_num: int) -> bool:
        '''Returns True if the given row number is valid'''
        return 0 <= row_num < self._rows

    def _is_valid_column_number(self, column_num: int) -> bool:
        '''Returns True if the given column number is valid'''
        return 0 <= column_num < self._columns
