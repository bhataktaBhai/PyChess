from piece import Piece


class Rook(Piece):

    STEPS = ((0, 1), (1, 0), (0, -1), (-1, 0))

    def __init__(self, colour, rank, file, has_moved):
        super().__init__(colour, rank, file)
        self.has_moved = has_moved
        self.symbol = '♖' if colour == 1 else '♜'

    def is_eyeing(self, pos, rank, file):
        if rank == self.rank and file == self.file:
            return False

        def sign(x): return -1 if x < 0 else 1 if x > 0 else 0
        if rank == self.rank:
            r_jump = 0
            f_jump = sign(file - self.file)
        elif file == self.file:
            r_jump = sign(rank - self.rank)
            f_jump = 0
        else:
            return False

        r = self.rank + r_jump
        f = self.file + f_jump
        while r != rank or f != file:
            if pos.board[r][f] is not None:
                return False
            r += r_jump
            f += f_jump
        return True
