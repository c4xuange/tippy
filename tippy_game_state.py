from game_state import GameState
from tippy_move import TippyMove
from copy import deepcopy


class TippyGameState(GameState):
    ''' The state of a Tippy game. 
    
    dimension: int   ---   dimensions of a square board
    
    Inherits method outcome from parent class GameState.
    '''

    def __init__(self, p, interactive=False, dimension=3, board=None):
        '''(TippyGameState, str, bool, int, list of lists) -> NoneType

        Initialize TippyGameState self with a board of side-length dimension.
        
        Extends __init__ method from parent class GameState.

        Assume:  3 <= dimension is an int
                        p in {'p1', 'p2'}
        '''
        self.dimension = dimension
        if interactive:
            self.dimension = int(input('What dimension grid?'))
        GameState.__init__(self, p)
        if board is None:
            create_board = []
            for n in range(0, self.dimension):
                create_board.append(['-' for i in range(0, self.dimension)])
            self.board = deepcopy(create_board)
        else:
            self.board = deepcopy(board)
        self.over = (self.possible_next_moves() == [] or self.is_tippy('x') 
                     or self.is_tippy('o'))
        self.instructions = ('On your turn, select the coordinate of the tile'
                             ' you would like to place your piece on the grid'
                             ' so long as it is empty.')

    def __repr__(self):
        '''(TippyGameState) -> str

        Return a string representation of TippyGameState self
        that evaluates to an equivalent TippyGameState.

        >>> t = TippyGameState('p1', dimension=4)
        >>> t
        TippyGameState('p1', False, 4)
        '''
        return 'TippyGameState({}, False, {})'.format(repr(self.next_player),
                                                      repr(self.dimension))

    def __str__(self):
        '''(TippyGameState) -> str

        Return a convenient string representation of TippyGameState self.

        >>> t = TippyGameState('p1')
        >>> print(t)
        Next player: p1
        Current board:
        - - -
        - - -
        - - -
        '''
        current_board = '\n'.join([' '.join(row) for row in self.board]) 
        return 'Next player: {}\nCurrent board:\n{}'.format(
            str(self.next_player), current_board)

    def __eq__(self, other):
        '''(TippyGameState, object) -> bool

        Return True iff this TippyGameState is the equivalent to other.

        >>> t1 = TippyGameState('p1', dimension = 3)
        >>> t2 = TippyGameState('p1', dimension = 3)
        >>> t1 == t2
        True
        '''
        return (isinstance(other, TippyGameState) and
                self.board == other.board and
                self.next_player == other.next_player)

    def apply_move(self, move):
        '''(TippyState, TippyMove) -> TippyState

        Return the new TippyState reached by applying move to self.

        Overrides apply_move method in parent class.
        
        >>> t1 = TippyGameState('p1', dimension=3)
        >>> t2 = t1.apply_move(TippyMove((0, 0)))
        >>> print(t2)
        Next player: p2
        Current board:
        o - -
        - - -
        - - -
        '''
        new_board = deepcopy(self.board)
        if self.next_player == 'p1':
            new_board[move.coord[0]][move.coord[1]] = 'o'
        else:
            new_board[move.coord[0]][move.coord[1]] = 'x'
        
        return TippyGameState(self.opponent(), dimension=self.dimension, 
                              board=new_board)

    def rough_outcome(self):
        '''(TippyGameState) -> float

        Return an estimate in interval [LOSE, DRAW, WIN] of best outcome 
        next_player can guarantee from state self.
        
        Overrides rough_outcome method in parent class.
        
        
        >>> b = [['o', 'o', 'o'], ['-', 'o', '-'], ['x', 'x', 'x']]
        >>> TippyGameState('p2', board=b).rough_outcome()
        -1.0
        >>> b = [['o', 'o', 'o'], ['-', 'o', 'x'], ['x', 'x', 'x']]
        >>> TippyGameState('p1', board=b).rough_outcome()
        1.0
        >>> row1 = ['x', 'x', 'x', 'x']
        >>> row2 = ['o', 'o', 'o', 'o']
        >>> b = [row1, row2, row1, ['o', 'o', 'o', '-']]
        >>> TippyGameState('p1', dimension=4, board=b).rough_outcome()
        0.0
        '''
        if self.next_player == 'p1':
            letter = 'o'
            other_letter = 'x'
        else:
            letter = 'x'
            other_letter = 'o'    
        for move in self.possible_next_moves():
            new_state = self.apply_move(move)
            #  if the next player can form a tippy in the next move, they win
            if new_state.is_tippy(letter):
                return self.WIN
            #  if for every move the next player can make, the opponent can 
            #  form a tippy in the move after that, the next player loses
            elif [new_state.apply_move(move).is_tippy(other_letter)
                  for move in new_state.possible_next_moves()]:
                return self.LOSE
            else:
                return self.DRAW               

    def get_move(self):
        '''(TippyGameState) -> TippyMove

        Prompt user in game state self and return move.
        
        Overrides get_move method in parent class.
        '''
        move = input('Occupy which coordinates? ')
        return TippyMove(eval(move))
        
    def winner(self, player):
        '''(TippyGameState, str) -> bool

        Return True iff the TippyGameState self is over and player has won.

        >>> b = [['o', 'o', 'o'], ['x', 'o', 'o'], ['x', 'x', 'x']]
        >>> t = TippyGameState('p1', board=b)
        >>> t.winner('p1')
        True

        Preconditions: player is either 'p1' or 'p2'
        
        Overrides winner method in parent class.
        '''
        if player == 'p1':
            letter = 'o'
        else:
            letter = 'x'

        return self.is_tippy(letter)

    def possible_next_moves(self):
        '''(TippyState) -> list of TippyMove

        Return a (possibly empty) list of moves that are legal
        from the present state self.
        
        Overrides possible_next_moves method in parent class.

        >>> b = [['o', 'o', 'o'], ['x', 'o', 'x'], ['x', 'x', 'x']]
        >>> t1 = TippyGameState('p1', board=b)
        >>> L1 = t1.possible_next_moves()
        >>> L1
        []
        >>> b = [['o', '-', 'o'], ['x', '-', 'x'], ['-', 'o', 'x']]
        >>> t1 = TippyGameState('p1', board=b)
        >>> L1 = t1.possible_next_moves()
        >>> L1
        [TippyMove((0, 1)), TippyMove((1, 1)), TippyMove((2, 0))]
        '''
        lst = []
        for row in range(0, self.dimension):
            for column in range(0, self.dimension):
                if self.board[row][column] == '-':
                    lst.append(TippyMove((row, column)))
        return lst

    def is_tippy(self, letter):
        '''(TippyGameState, str) -> bool
    
        Return whether there is a tippy formed by letter in game state self.
        
        Precondition: letter is either 'x' or 'o'
        
        >>> b = [['o', 'o', 'o'], ['x', 'o', 'o'], ['x', 'x', 'x']]
        >>> t = TippyGameState('p2', board=b)
        >>> t.is_tippy('o')
        True
        >>> t.is_tippy('x')
        False
        '''
        
        return self.is_tippy1(letter) or self.is_tippy2(letter) \
            or self.is_tippy3(letter) or self.is_tippy4(letter)
        
    #Legend
    
    #tile1 = self.board[r][c]
    #tile2 = self.board[r][c+1]
    #tile3 = self.board[r + 1][c]
    #tile4 = self.board[r + 1][c + 1]
    #tile5 = self.board[r + 2][c]
    #tile6 = self.board[r + 2][c + 1]
    #tile7 = self.board[r][c + 2]
    #tile8 = self.board[r + 1][c + 2]
    #   ___________
    #  |_1_|_2_|_7_|
    #  |_3_|_4_|_8_|
    #  |_5_|_6_|___|    
                       
    #tippy1 = [tile1, tile3, tile4, tile6]
    #tippy2 = [tile2, tile4, tile3, tile5]
    #tippy3 = [tile1, tile2, tile4, tile8]
    #tippy4 = [tile7, tile2, tile4, tile3]
    
    def is_tippy1(self, letter):
        '''(TippyGameState, str) -> bool
    
        Return whether there is a tippy1 (refer to legend) formed by letter 
        in game state self.
        
        Precondition: letter is either 'x' or 'o'
        
        >>> b = [['o', 'x', 'x'], ['o', 'o', '-'], ['x', 'o', '-']]
        >>> t = TippyGameState('p2', board=b)
        >>> t.is_tippy1('o')
        True
        '''
        
        for r in range(0, self.dimension - 2):
            for c in range(0, self.dimension - 1):
                if (self.board[r][c] == self.board[r + 1][c] == 
                        self.board[r + 1][c + 1] == self.board[r + 2][c + 1] == 
                        letter):
                    return True
        return False
    
    def is_tippy2(self, letter):
        '''(TippyGameState, str) -> bool
    
        Return whether there is a tippy2 (refer to legend) formed by letter 
        in game state self.
        
        Precondition: letter is either 'x' or 'o'
        
        >>> b = [['o', 'x', 'o'], ['x', 'x', '-'], ['x', 'o', '-']]
        >>> t = TippyGameState('p1', board=b)
        >>> t.is_tippy2('x')
        True
        '''
        
        for r in range(0, self.dimension - 2):
            for c in range(0, self.dimension - 1):
                if (self.board[r + 2][c] == self.board[r + 1][c] ==
                        self.board[r + 1][c + 1] == self.board[r][c + 1] ==
                        letter):
                    return True
        return False
    
    def is_tippy3(self, letter):
        '''(TippyGameState, str) -> bool
    
        Return whether there is a tippy3 (refer to legend) formed by letter 
        in game state self.
        
        Precondition: letter is either 'x' or 'o'
        
        >>> b = [['x', 'o', 'o'], ['o', 'o', '-'], ['-', 'x', 'x']]
        >>> t = TippyGameState('p1', board=b)
        >>> t.is_tippy4('o')
        True
        '''
        for r in range(0, self.dimension - 1):
                for c in range(0, self.dimension - 2):
                    if (self.board[r][c] == self.board[r][c + 1] == 
                            self.board[r + 1][c + 1] == 
                            self.board[r + 1][c + 2] == letter):
                        return True
        return False      
    
    def is_tippy4(self, letter):  
        '''(TippyGameState, str) -> bool
    
        Return whether there is a tippy4 (refer to legend) formed by letter 
        in game state self.
        
        Precondition: letter is either 'x' or 'o'
        
        >>> b = [['o', 'x', 'x'], ['o', 'o', '-'], ['x', 'o', '-']]
        >>> t = TippyGameState('p2', board=b)
        >>> t.is_tippy1('o')
        True
        '''
        for r in range(0, self.dimension - 1):
                for c in range(0, self.dimension - 2):
                    if (self.board[r + 1][c] == self.board[r][c + 1] == 
                            self.board[r + 1][c + 1] == self.board[r][c + 2]
                            == letter):
                        return True
        return False
    
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()