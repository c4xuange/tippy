from strategy import Strategy
from subtract_square_state import SubtractSquareState
from tippy_game_state import TippyGameState


class StrategyMinimaxMemoize(Strategy):
    ''' Interface to suggest a move producing the best possible outcome for
    a player assuming both players have all the information to make the
    best possible move from any game state. Eliminates the redundancy of
    calculating scores for equivalent game positions more than once.
    '''    
    
    def __init__(self, interactive=False):
        '''(StrategyMinimaxMemoize, bool) -> NoneType

        Extends __init__ method from parent class Strategy.
        self.ms_dict is dictionary of game states and the score they lead to.
        '''        
        Strategy.__init__(self)
        self.ms_dict = {}
        
    def __repr__(self):
        '''(StrategyMinimaxMemoize) -> str

        Return a string representation of StrategyMinimaxMemoize self
        that evaluates to an equivalent strategy.

        >>> S = StrategyMinimaxMemoize()
        >>> S
        StrategyMinimaxMemoize()
        '''
        return 'StrategyMinimaxMemoize()'
    
    def __str__(self):
        '''(StrategyMinimaxMemoize) -> str

        Return a convenient string representation of strategy self.

        >>> S = StrategyMinimaxMemoize()
        >>> print(S)
        The current strategy is Minimax memoization.
        The current moves to score dictionary is {}.
        '''
        return 'The current strategy is Minimax memoization.\n' + \
               'The current moves to score dictionary is ' +\
               '{}.'.format(self.ms_dict)  
    
    def __eq__(self, other):
        '''(StrategyMinimaxMemoize, object) -> bool
        
        Return True iff strategy self is equivalent to other.
        
        >>> S = StrategyMinimaxMemoize()
        >>> Q = SubtractSquareState('p1', current_total = 2)
        >>> T = StrategyMinimaxMemoize()
        >>> S.suggest_move(Q)
        SubtractSquareMove(1)
        >>> S.ms_dict
        {'Current total: 1; next player: p2': 1.0}
        >>> T.suggest_move(Q)
        SubtractSquareMove(1)
        >>> T.ms_dict
        {'Current total: 1; next player: p2': 1.0}
        >>> S == T
        True
        '''
        return (isinstance(other, StrategyMinimaxMemoize) and
                self.ms_dict == other.ms_dict)

    def suggest_move(self, state):
        '''(StrategyMinimaxMemoize, GameState) -> Move
        
        Returns a move that would result in a best possible outcome from the
        present game state state using Strategy self.
        
        Overrides suggest_move method in parent class.
        
        >>> S = StrategyMinimaxMemoize()
        >>> b = [['o', 'o', 'o'], ['-', '-', '-'], ['x', 'x', 'x']]
        >>> t = TippyGameState('p2', board = b)
        >>> S.suggest_move(t)
        TippyMove((1, 1))
        '''
        score_moves = []
        for move in state.possible_next_moves():
            score = (-1) * (self.find_score(state.apply_move(move)))
            score_moves.append((score, move))
        return max(score_moves, key=produce_max)[1]

    # helper function for suggest_move
    def find_score(self, state):
        '''(StrategyMinimaxMemoize, GameState) -> float
        
        Returns the score of the best possible outcome from the present game
        state state using strategy self.
        
        >>> S = StrategyMinimaxMemoize()
        >>> b = [['o', 'o', 'o'], ['-', 'o', '-'], ['x', 'x', 'x']]
        >>> t1 = TippyGameState('p2', board = b)
        >>> S.find_score(t1)
        -1.0
        >>> b = [['o', 'o', 'o'], ['-', '-', '-'], ['x', 'x', 'x']]
        >>> t2 = TippyGameState('p2', board = b)
        >>> S.find_score(t2)
        1.0
        >>> row1 = ['x', 'x', 'x', 'x']
        >>> row2 = ['o', 'o', 'o', 'o']
        >>> b = [row1, row2, row1, ['o', 'o', 'o', '-']]
        >>> t3 = TippyGameState('p1', dimension = 4, board = b)
        >>> S.find_score(t3)
        -0.0
        '''
        
        if state.over:
            return state.outcome()

        else:
            if state.__str__() not in self.ms_dict:
                score = max(self.find_score(state.apply_move(move)) * (-1) 
                            for move in state.possible_next_moves())
                self.ms_dict[state.__str__()] = score
            return self.ms_dict[state.__str__()]
            

def produce_max(L):
    '''(list of objects) -> object
    
    Return the first item in list L.
    >>> L = ((1,'a'), (1, 'b'), (1, 'c'))
    >>> any_max = produce_max(L)
    >>> any_max
    (1, 'a')
    '''
    return L[0]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    