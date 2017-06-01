from strategy import Strategy
from subtract_square_state import SubtractSquareState
from tippy_game_state import TippyGameState


class StrategyMinimaxPrune(Strategy):
    ''' Interface to suggest a move producing the best possible outcome for
    a player assuming both players have all the information to make the best
    possible move from any game state. Eliminates redundancy by ignoring any 
    potential game states that won't affect the final outcome.
    
    Inherits __init__ method from parent class Strategy
    '''
    
    def __repr__(self):
        '''(StrategyMinimaxPrune) -> str

        Return a string representation of StrategyMinimaxPrune self
        that evaluates to an equivalent strategy.

        >>> S = StrategyMinimaxPrune()
        >>> S
        StrategyMinimaxPrune()
        '''
        return 'StrategyMinimaxPrune()'
    
    def __str__(self):
        '''(StrategyMinimaxPrune) -> str

        Return a convenient string representation of strategy self.

        >>> S = StrategyMinimaxPrune()
        >>> print(S)
        The current strategy is Minimax prune.
        '''
        return 'The current strategy is Minimax prune.'  
    
    #  StrategyMinimaxPrune does not require an __eq__ method, since it does 
    #  not have any attributes to compare.    

    def suggest_move(self, state):
        '''(StrategyMinimaxPrune, GameState) -> Move
        
        Returns a move that would result in a best possible outcome from the
        present game state state using Strategy self.
        
        Overrides suggest_move method in parent class.
        
        >>> S = StrategyMinimaxPrune()
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
        '''(StrategyMinimaxPrune, GameState) -> float
        
        Returns the score of the best possible outcome for the current player
        from the present game state state using strategy self.
        
        >>> S = StrategyMinimaxPrune()
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
        if state.next_player == 'p1':
            return self.minimax(state, -1.0, 1.0)
        else:
            return - self.minimax(state, -1.0, 1.0)
        
    # helper function for find_score based on an absolute score perspective
    def minimax(self, state, p1, p2):
        '''(StrategyMinimaxPrune, GameState, float, float) -> float
        
        Returns the absolute score of the best possible outcome for the next
        player from the present game state state using Strategy self. 
        
        Note: Absolute score does not take the player's perspective when
        determining the score. The higher the score, the better for p1, and 
        the lower the score, the better for p2.
        
        >>> S = StrategyMinimaxPrune()
        >>> b = [['o', 'o', 'o'], ['-', 'o', '-'], ['x', 'x', 'x']]
        >>> t1 = TippyGameState('p2', board = b)
        >>> S.minimax(t1, -1.0, 1.0)
        1.0
        >>> b = [['o', 'o', 'o'], ['-', '-', '-'], ['x', 'x', 'x']]
        >>> t2 = TippyGameState('p2', board = b)
        >>> S.minimax(t2, -1.0, 1.0)
        -1.0
        >>> row1 = ['x', 'x', 'x', 'x']
        >>> row2 = ['o', 'o', 'o', 'o']
        >>> b = [row1, row2, row1, ['o', 'o', 'o', '-']]
        >>> t3 = TippyGameState('p1', dimension = 4, board = b)
        >>> S.minimax(t3, -1.0, 1.0)
        -0.0
        '''        

        best_score = p1 if state.next_player == 'p1' else p2
        # p1: best (highest) value that p1 can secure
        # p2: best (lowest) value that p2 can secure
        if state.over:
            return (state.outcome() if state.next_player == 'p1' 
                    else -state.outcome()) 
        else:
            for move in state.possible_next_moves():
                x = self.minimax(state.apply_move(move), p1, p2)
                best_score = (max(best_score, x) if state.next_player == 'p1' 
                              else min(best_score, x))
                if state.next_player == 'p1' and best_score >= p2:
                    return best_score
                elif state.next_player == 'p2' and best_score <= p1:
                    return best_score
            return best_score


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