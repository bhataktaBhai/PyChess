from piece import Piece


class Knight(Piece):

    STEPS = ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2))

    def __init__(self, colour, rank, file):
        super().__init__(colour, rank, file)
        self.symbol = '♘' if colour == 1 else '♞'

    def is_eyeing(self, pos, rank, file):
        return (rank - self.rank, file - self.file) in self.STEPS

    def movable_to(self, pos):
        if pos.check > 1:
            return []
        if pos.pinned(self):
            return []

        squares = []
        if pos.check:
            blocks = pos.blocks()
            for r_jump, f_jump in self.STEPS:
                r = self.rank + r_jump
                f = self.file + f_jump
                if (r, f) in blocks:
                    squares.append((r, f))
            return squares

        for r_jump, f_jump in self.STEPS:
            r = self.rank + r_jump
            f = self.file + f_jump
            if -1 < r < 8 and -1 < f < 8:
                if (pos.board[r][f] is None
                        or pos.board[r][f].colour != self.colour):
                    squares.append((r, f))

        return squares
