from typing import Tuple

from piece import Piece
from rook import Rook


class King(Piece):

    STEPS = ()

    def __init__(self, colour, rank, file, has_moved):
        super().__init__(colour, rank, file)
        self.has_moved = has_moved
        self.symbol = '♔' if colour == 1 else '♚'

    def is_eyeing(self, pos, rank, file):
        return (rank - self.rank, file - self.file) in Piece.ALL_DIRECTIONS
    
    def movable_to(self, pos):
        squares = []
        for r_jump, f_jump in Piece.ALL_DIRECTIONS:
            if pos.check:
                enemy = pos.nearest_piece_in((-r_jump, -f_jump), self.rank, self.file)
                if (enemy is not None and enemy.colour != self.colour
                        and (r_jump, f_jump) in enemy.STEPS):
                    continue
            r = self.rank + r_jump
            f = self.file + f_jump
            if -1 < r < 8 and -1 < f < 8:
                if pos.board[r][f] is None or pos.board[r][f].colour != self.colour:
                    if not pos.under_attack(r, f):
                        squares.append((r, f))
        if self.can_castle(pos, 6):
            squares.append((self.rank, 6))
        if self.can_castle(pos, 2):
            squares.append((self.rank, 2))
        return squares

    def can_castle(self, pos, file):
        if self.has_moved or pos.check:
            return False
        if file == 2:
            rook = pos.board[self.rank][0]
            if type(rook) != Rook or rook.has_moved:
                return False
            for f in (1, 2, 3):
                if pos.board[self.rank][f] is not None:
                    return False
            squares = ((self.rank, 2), (self.rank, 3))
        elif file == 6:
            rook = pos.board[self.rank][7]
            if type(rook) != Rook or rook.has_moved:
                return False
            for f in (5, 6):
                if pos.board[self.rank][f] is not None:
                    return False
            squares = ((self.rank, 5), (self.rank, 6))
        else:
            return False

        for r, f in squares:
            if pos.under_attack(r, f):
                return False
        else:
            return True
