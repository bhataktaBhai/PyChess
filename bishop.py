from piece import Piece


class Bishop(Piece):

    STEPS = ((1, 1), (1, -1), (-1, -1), (-1, 1))
    
    def __init__(self, colour, rank, file):
        super().__init__(colour, rank, file)
        self.symbol = '♗' if colour == 1 else '♝'

    def is_eyeing(self, pos, rank, file):
        if rank == self.rank and file == self.file:
            return False

        def sign(x): return -1 if x < 0 else 1 if x > 0 else 0
        if rank - file == self.rank - self.file:
            r_jump = f_jump = sign(rank - self.rank)
        elif rank + file == self.rank + self.file:
            r_jump = sign(rank - self.rank)
            f_jump = - r_jump
        else:
            return False

        r = self.rank + r_jump
        f = self.file + f_jump
        while r != rank:
            if pos.board[r][f] is not None:
                return False
            r += r_jump
            f += f_jump
        return True
