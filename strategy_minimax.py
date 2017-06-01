from strategy import Strategy
from subtract_square_state import SubtractSquareState
from tippy_game_state import TippyGameState


class StrategyMinimax(Strategy):
    ''' Interface to suggest a move producing the best possible outcome for
    a player assuming both players have all the information to make the best
    possible move from any game state.
    
    Inherits __init__ method from parent class Strategy
    '''
    
    def __repr__(self):
        '''(StrategyMinimax) -> str

        Return a string representation of StrategyMinimax self
        that evaluates to an equivalent strategy.

        >>> S = StrategyMinimax()
        >>> S
        StrategyMinimax()
        '''
        return 'StrategyMinimax()'

    def __str__(self):
        '''(StrategyMinimax) -> str

        Return a convenient string representation of strategy self.

        >>> S = StrategyMinimax()
        >>> print(S)
        StrategyMinimax()
        '''
        return 'StrategyMinimax()'

    #  StrategyMinimax does not require an __eq__ method, since it does not
    #  have any attributes to compare.
    
    def suggest_move(self, state):
        '''(StrategyMinimax, GameState) -> Move
        
        Returns a move that would result in a best possible outcome from the
        present game state state using Strategy self.
        
        Overrides suggest_move method in parent class.
        
        >>> S = StrategyMinimax()
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
        '''(StrategyMinimax, GameState) -> float
        
        Returns the score of the best possible outcome from the present game
        state state using strategy self.
        
        >>> S = StrategyMinimax()
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
            return max(self.find_score(state.apply_move(move)) * (-1) 
                       for move in state.possible_next_moves())


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