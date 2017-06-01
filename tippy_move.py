from move import Move


class TippyMove(Move):
    ''' A move in the game of Tippy.

    coord: (int, int) -- The row number and column number of the spot the
    player would like to occupy.
    '''

    def __init__(self, coord):
        ''' (TippyMove, tuple of ints) -> NoneType

        Initialize a new TippyMove self for occupying the tile with 
        coordinates coord.

        Assume: coord represents a valid and empty tile on the game board.
        '''
        self.coord = coord

    def __repr__(self):
        ''' (TippyMove) -> str

        Return a string representation of this TippyMove.
        >>> m1 = TippyMove((0, 0))
        >>> m1
        TippyMove((0, 0))
        '''
        return 'TippyMove({})'.format(self.coord)

    def __str__(self):
        ''' (TippyMove) -> str

        Return a string representation of this TippyMove that is suitable for 
        users to read.

        >>> m1 = TippyMove((0, 0))
        >>> print(m1)
        Occupy tile (0, 0)
        '''

        return 'Occupy tile {}'.format(self.coord)

    def __eq__(self, other):
        ''' (TippyMove, object) -> bool

        Return True iff this TippyMove is equivalent to other.

        >>> m1 = TippyMove((1, 2))
        >>> m2 = TippyMove((1, 2))
        >>> m3 = TippyMove((3, 4))
        >>> print(m1 == m2)
        True
        >>> print(m1 == m3)
        False
        '''
        return (isinstance(other, TippyMove) and 
                self.coord == other.coord)


if __name__ == '__main__':
    import doctest
    doctest.testmod()