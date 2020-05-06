def get_piece(symbol, rank, file, has_moved = False):
    import pawn, knight, bishop, rook, queen, king

    if symbol == ' ':
        return None
    elif symbol > '♙':
        colour = -1
        symbol = chr(ord(symbol) - ord('♚') + ord('♔'))
    else:
        colour = 1

    if symbol == '♔':
        return king.King(colour, rank, file, has_moved)
    elif symbol == '♕':
        return queen.Queen(colour, rank, file)
    elif symbol == '♖':
        return rook.Rook(colour, rank, file, has_moved)
    elif symbol == '♗':
        return bishop.Bishop(colour, rank, file)
    elif symbol == '♘':
        return knight.Knight(colour, rank, file)
    elif symbol == '♙':
        return pawn.Pawn(colour, rank, file)
    else:
        return None


class Piece:

    ALL_DIRECTIONS = ((0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,+1))

    def __init__(self, colour, rank, file):
        self.colour = colour
        self.rank = rank
        self.file = file

    def __str__(self):
        return self.symbol

    def __eq__(self, piece):
        return (type(piece) == type(self) and piece.colour == self.colour
                and piece.rank == self.rank and piece.file == self.file)

    def move(self, move):
        return get_piece(self.symbol, move[0], move[1], True)

    def movable_to(self, pos):
        if pos.check == 2:
            return []
        pinned = pos.pinned(self)
        if pinned:
            steps = pinned
        else:
            steps = self.STEPS

        squares = []
        if pos.check:
            if pinned:
                return []
            blocks = pos.blocks()
            for r_jump, f_jump in steps:
                r = self.rank + r_jump
                f = self.file + f_jump
                while -1 < r < 8 and -1 < f < 8:
                    if (r,f) in blocks:
                        squares.append((r,f))
                        break
                    if pos.board[r][f] is not None:
                        break
                    r += r_jump
                    f += f_jump
            return squares

        for r_jump, f_jump in steps:
            r = self.rank + r_jump
            f = self.file + f_jump
            while -1 < r < 8 and -1 < f < 8:
                if pos.board[r][f] is not None:
                    if pos.board[r][f].colour != self.colour:
                        squares.append((r,f))
                    break
                squares.append((r,f))
                r += r_jump
                f += f_jump
        return squares

    def can_move_to(self, pos, rank, file):
        for move in self.movable_to(pos):
            if move[0:2] == (rank, file):
                return True
