from strategy import Strategy
from subtract_square_state import SubtractSquareState
from tippy_game_state import TippyGameState


class StrategyMinimaxMyopic(Strategy):
    ''' Interface to suggest a move producing the best possible outcome for
    a player assuming both players have all the information to make the best
    possible move from any game state, and are only looking a maximum of 3
    steps into the future.
    
    Inherits __init__ method from parent class Strategy
    '''
    
    def __repr__(self):
        '''(StrategyMinimaxMyopic) -> str

        Return a string representation of StrategyMinimax self
        that evaluates to an equivalent strategy.

        >>> S = StrategyMinimaxMyopic()
        >>> S
        StrategyMinimaxMyopic()
        '''
        return 'StrategyMinimaxMyopic()'

    def __str__(self):
        '''(StrategyMinimaxMyopic) -> str

        Return a convenient string representation of strategy self.

        >>> S = StrategyMinimaxMyopic()
        >>> print(S)
        The current strategy is Minimax myopia.
        '''
        return 'The current strategy is Minimax myopia.'

    #  StrategyMinimaxMyopic does not require an __eq__ method, since it does 
    #  not have any attributes to compare.
    
    def suggest_move(self, state):
        '''(StrategyMinimaxMyopic, GameState) -> Move
        
        Returns a move that would result in a best possible outcome from the
        present game state state using Strategy self.
        
        Overrides suggest_move method in parent class.
        
        >>> S = StrategyMinimaxMyopic()
        >>> b = [['o', 'o', 'o'], ['-', '-', '-'], ['x', 'x', 'x']]
        >>> t = TippyGameState('p2', board = b)
        >>> S.suggest_move(t)
        TippyMove((1, 1))
        >>> q = SubtractSquareState('p1', current_total = 12)
        >>> S.suggest_move(q)
        SubtractSquareMove(9)
        '''
        score_moves = []
        for move in state.possible_next_moves():
            score = (-1) * (self.find_score(state.apply_move(move)))
            score_moves.append((score, move))
        return max(score_moves, key=produce_max)[1]

    # helper function for suggest_move
    def find_score(self, state, depth=3):
        '''(StrategyMinimaxMyopic, GameState, int) -> float
        
        Returns the score of the best possible outcome from the present game
        state state using strategy self, looking a maximum of 3 steps ahead.
        
        >>> S = StrategyMinimaxMyopic()
        >>> q1 = SubtractSquareState('p1', current_total = 7)
        >>> S.find_score(q1)
        -1.0
        >>> q2 = SubtractSquareState('p1', current_total = 12)
        >>> S.find_score(q2)
        -0.0
        >>> q3 = SubtractSquareState('p1', current_total = 21)
        >>> S.find_score(q3)
        1.0
        '''
        
        if state.over:
            return state.outcome()
        elif depth == 0:
            return state.rough_outcome()
        else:
            return max(self.find_score(state.apply_move(move), depth - 1) * 
                       (-1) for move in state.possible_next_moves())


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