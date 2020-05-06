from piece import Piece


class Pawn(Piece):

    STEPS = ()

    def __init__(self, colour, rank, file):
        super().__init__(colour, rank, file)
        self.symbol = '♙' if colour == 1 else '♟'
        self.relative_rank = rank if colour == 1 else 7 - rank

    def is_eyeing(self, pos, rank, file):
        del pos
        if rank == self.rank + self.colour:
            if file - self.file in (-1, 1):
                return True
        return False

    def movable_to(self, pos):
        desire = self.file == 7
        if pos.check > 1:
            return []
        colour, rank, file = self.colour, self.rank, self.file
        pinned = pos.pinned(self)
        if pinned:
            if (0, 1) in pinned:
                return []
            steps = pinned
        else:
            steps = ((colour, 0), (colour, 1), (colour, -1))

        squares = []

        def moves(r, f):
            if self.relative_rank < 6:
                return [(r, f)]
            else:
                return [(r, f, 'Q'), (r, f, 'R'),
                        (r, f, 'B'), (r, f, 'N')]

        forward = rank + colour
        left = file - colour
        right = file + colour

        if pos.check:
            if pinned:
                return []
            if pos.checker == pos.double_mover:
                if (self.rank == pos.double_mover.rank
                        and abs(self.file - pos.double_mover.file) == 1):
                    return [(forward, pos.double_mover.file)]
            blocks = pos.blocks()
            if (forward, file) in blocks:
                if pos.board[forward][file] is None:
                    squares += moves(forward, file)
            elif self.relative_rank == 1 and pos.board[forward][file] is None:
                if (forward + colour, file) in blocks:
                    if pos.board[forward + colour][file] is None:
                        squares += [(forward + colour, file)]

            if (forward, left) in blocks:
                if pos.board[forward][left] is not None:
                    squares += moves(forward, left)
            if (forward, right) in blocks:
                if pos.board[forward][right] is not None:
                    squares += moves(forward, right)

            return squares

        if (colour, 0) in steps:
            if pos.board[forward][file] is None:
                squares += moves(forward, file)
                if self.relative_rank == 1 and pos.board[forward + colour][file] is None:
                    squares += moves(forward + colour, file)

        if -1 < left < 8 and (colour, -colour) in steps:
            if pos.board[forward][left] is not None:
                if pos.board[forward][left].colour != self.colour:
                    if desire:
                        print('hi')
                    squares += moves(forward, left)
            elif pos.double_mover is not None and pos.board[self.rank][left] == pos.double_mover:
                squares += [(forward, left)]

        if -1 < right < 8 and (colour, colour) in steps:
            if pos.board[forward][right] is not None:
                if pos.board[forward][right].colour != self.colour:
                    squares += moves(forward, right)
            elif pos.double_mover is not None and pos.board[self.rank][right] == pos.double_mover:
                squares += [(forward, right)]

        return squares

    def can_promote_to(self, pos, rank, file):
        return (rank, file, 'Q') in self.movable_to(pos)

    def move(self, move):
        import piece, queen, rook, bishop, knight
        if len(move) > 2:
            switch = {
                'Q': queen.Queen(self.colour, move[0], move[1]),
                'R': rook.Rook(self.colour, move[0], move[1], True),
                'B': bishop.Bishop(self.colour, move[0], move[1]),
                'N': knight.Knight(self.colour, move[0], move[1])
            }
            return switch.get(move[2], None)
        else:
            return piece.get_piece(self.symbol, move[0], move[1])
