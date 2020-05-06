from piece import Piece


class Queen(Piece):

    STEPS = Piece.ALL_DIRECTIONS

    def __init__(self, colour, rank, file):
        super().__init__(colour, rank, file)
        self.symbol = '♕' if colour == 1 else '♛'

    def is_eyeing(self, pos, rank, file):
        from rook import Rook
        from bishop import Bishop
        return (Rook.is_eyeing(self, pos, rank, file)
                or Bishop.is_eyeing(self, pos, rank, file))
