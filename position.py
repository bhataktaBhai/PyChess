from typing import Optional, List

from piece import Piece
from king import King
from knight import Knight
from pawn import Pawn
from queen import Queen
from rook import Rook


class Position:

    # pieces, turn, double_mover, en_passant, board, king, check, checker, short, long
    def __init__(self, pieces, turn, double_mover=None):
        self.pieces = []
        self.turn = turn
        self.double_mover = double_mover
        self.en_passant = False
        self.board = [[None] * 8 for i in range(8)]
        for piece in pieces:
            if type(piece) == King and piece.colour == self.turn:
                self.king = piece
            elif piece == double_mover:
                if piece.file == 0:
                    files = (1,)
                elif piece.file == 7:
                    files = (6,)
                else:
                    files = (piece.file - 1, piece.file + 1)
                for f in files:
                    pawn_suspect = self.board[piece.rank][f]
                    if type(pawn_suspect) == Pawn and pawn_suspect.colour == turn:
                        pinned = self.pinned(pawn_suspect)
                        if not pinned or (turn, piece.file - f) in pinned:
                            self.en_passant = True
                            break
            self.pieces.append(piece)
            self.board[piece.rank][piece.file] = piece
        self.check, self.checker = self.attack_info(self.king.rank, self.king.file)
        self.short_castle = self.king.can_castle(self, 6)
        self.long_castle = self.king.can_castle(self, 2)

    def __str__(self):
        out = ''
        for i in range(7, -1, -1):
            out += f'\n{i+1} |'
            for j in range(8):
                piece = self.board[i][j]
                if piece is None:
                    out += ' |'
                else:
                    out += f'{str(piece)}|'
        out += '\n   a b c d e f g h'
        return out

    def __eq__(self, pos):
        if self.turn != pos.turn:
            return False
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != pos.board[i][j]:
                    # print(self.board[i][j], pos.board[i][j], i, j)
                    return False
        return (self.en_passant == pos.en_passant
                and self.short_castle == pos.short_castle
                and self.long_castle == pos.long_castle)

    def __hash__(self):
        return hash(1)

    def nearest_piece_in(self, direction, rank, file):
        r_jump, f_jump = direction
        r = rank + r_jump
        f = file + f_jump
        while -1 < r < 8 and -1 < f < 8:
            if self.board[r][f] is not None:
                return self.board[r][f]
            r += r_jump
            f += f_jump
        return None

    def under_attack(self, rank, file):
        return self.attack_info(rank, file)[0] > 0

    def attack_info(self, rank, file):
        c = 0
        attacker = None
        for enemy in self.pieces:
            if enemy.colour == self.turn:
                continue
            if enemy.is_eyeing(self, rank, file):
                c += 1
                attacker = enemy
        return c, attacker

    def blocks(self):
        if self.check != 1 or type(self.checker) == Knight:
            return []
        blocks = []
        def sign(x): return -1 if x < 0 else 1 if x > 0 else 0
        r_jump = sign(self.checker.rank - self.king.rank)
        f_jump = sign(self.checker.file - self.king.file)
        r = self.king.rank + r_jump
        f = self.king.file + f_jump
        while True:
            blocks.append((r, f))
            if self.board[r][f] is not None:
                break
            r += r_jump
            f += f_jump
        return blocks

    def pinned(self, piece):
        for direction in Piece.ALL_DIRECTIONS:
            king_suspect = self.nearest_piece_in(direction, piece.rank, piece.file)
            if king_suspect == self.king:
                opp_direction = (-direction[0], -direction[1])
                enemy = self.nearest_piece_in(opp_direction, piece.rank, piece.file)
                if enemy is not None and enemy.colour != self.turn:
                    if direction in enemy.STEPS:
                        return direction, opp_direction
                return False
        return False

    def stuck(self):
        for piece in self.pieces:
            if piece.colour != self.turn:
                continue
            if len(piece.movable_to(self)) != 0:
                # print(f'{piece.symbol} on ({piece.rank},{piece.file}) can move to {piece.movable_to(self)[0]}')
                return False
        return True
    
    def insufficient_material(self):
        if len(self.pieces) > 4:
            return False
        pieces = []
        for piece in self.pieces:
            if type(piece) in (Pawn, Rook, Queen):
                return False
            elif type(piece) != King:
                pieces.append(piece)
        if len(self.pieces) < 4:
            return True
        if type(pieces[0]) == Bishop and type(pieces[1]) == Bishop:
            if ((pieces[0].rank + pieces[0].file) % 2
                == (pieces[1].rank + pieces[1].file) % 2):
                return True
        return False
