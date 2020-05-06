from position import Position
from piece import get_piece
from king import King
from queen import Queen
from rook import Rook
from bishop import Bishop
from knight import Knight
from pawn import Pawn
import tkinter as tk


def threefold_repetition(all_positions, position):
    all_positions[position] = all_positions.get(position, 0) + 1
    return all_positions[position] > 2


def init():
    global piece, pieces, turn, position, all_positions, double_mover, num_of_moves, squares
    global window
    temp_board = [
        ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖'],
        ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
        ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜']
    ]

    pieces = []
    squares = [[None]*8 for i in range(8)]
    for i in range(8):
        for j in range(8):
            piece = get_piece(temp_board[i][j], i, j)
            if piece is not None:
                pieces.append(piece)
    turn = 1
    double_mover = None
    position = Position(pieces, turn, double_mover)
    all_positions = {position: 1}
    num_of_moves = 0
    piece = None

    window = tk.Tk(className = '---Gooey Chess---')
    window.geometry('400x400')
    for rank in range(7,-1,-1):
        tk.Grid.rowconfigure(window, rank + 1, weight = 1)
        tk.Grid.columnconfigure(window, rank + 1, weight = 1)
        for file in range(8):
            bg_colour = '#96A2B4' if (rank + file) % 2 == 0 else 'white'
            frame = tk.Frame(window, bg = 'black')
            frame.grid(row = 8-rank, column = file+1, sticky = tk.N + tk.S + tk.E + tk.W)
            square = tk.Label(frame, text = temp_board[rank][file], font = ('Monospaced', 40),
                              bg = bg_colour)
            square.bind('<Button-1>', click)
            square.rank = rank
            square.file = file
            # square.pack(fill = tk.BOTH) not filling in y
            square.place(x = 0, y = 0, relheight = 1, relwidth = 1)
            squares[rank][file] = square
    window.mainloop()


def promote(frame, move):
    frame.destroy()
    play(move)


def play(move):
    global pieces, piece, turn, position, num_of_moves, all_positions, squares, window, double_mover
    pieces.remove(piece)
    moved_piece = piece.move(move)
    pieces.append(moved_piece)
    squares[piece.rank][piece.file].config(text = ' ')
    squares[move[0]][move[1]].config(text = str(moved_piece))
    double_mover = None
    if position.board[move[0]][move[1]] is not None:
        pieces.remove(position.board[move[0]][move[1]])
        num_of_moves = 0
        all_positions.clear()
    elif type(moved_piece) == Pawn:
        num_of_moves = 0
        all_positions.clear()
        if move[1] != piece.file:
            pieces.remove(position.board[move[0] - turn][move[1]])
            squares[move[0] - turn][move[1]].config(text = ' ')
        elif abs(move[0] - piece.rank) == 2:
            double_mover = moved_piece
    elif type(piece) == King and abs(move[1] - piece.file) == 2:
        if move[1] == 2:
            rook = position.board[move[0]][0]
            pieces.remove(rook)
            pieces.append(rook.move((move[0], 3)))
            squares[move[0]][0].config(text = ' ')
            squares[move[0]][3].config(text = str(rook))
        else:
            rook = position.board[move[0]][7]
            pieces.remove(rook)
            pieces.append(rook.move((move[0], 5)))
            squares[move[0]][7].config(text = ' ')
            squares[move[0]][5].config(text = str(rook))
    piece = None
    num_of_moves += 1
    turn = -turn
    position = Position(pieces, turn, double_mover)
    stuck = position.stuck()
    checkmate = stuck and position.check
    threefold = threefold_repetition(all_positions, position)
    fifty = num_of_moves >= 100
    insufficient= position.insufficient_material()
    end = stuck or threefold or fifty or insufficient
    if end:
        if checkmate:
            if turn == 1:
                message = 'Black wins!\n0-1'
            else:
                message = 'White wins!\n1-0'
        elif stuck:
            message = 'Stalemate.\n0.5-0.5'
        elif threefold:
            message = 'Threefold repetition.\n0.5-0.5'
        elif fifty:
            message = 'Draw by Fifty Move Rule.\n0.5-0.5'
        elif insufficient:
            message = 'Insufficient material.\n0.5-0.5'
        label = tk.Label(window, text = message)
        label.grid(row = 9, column = 1, columnspan = 8)
        for rank in squares:
            for square in rank:
                square.bind('<Button-1>', lambda event: 0)


def click(event):
    global piece, pieces, turn, position, window
    for rank in squares:
        for square in rank:
            square.config(text = ' ' if square['text'] == '•' else square['text'],
                          fg = 'black')
    rank = event.widget.rank
    file = event.widget.file
    if position.board[rank][file] is None or position.board[rank][file].colour != turn:
        if piece is None:
            return
        if not piece.can_move_to(position, rank, file):
            piece = None
            return
        if type(piece) == Pawn and piece.relative_rank == 6:
            frame = tk.Frame(window)
            plus = 0 if turn == 1 else 6
            tk.Button(frame, text = chr(ord('♕') + plus), font = ('Monospaced', 30), height = 1,
                      command = lambda: promote(frame, (rank, file, 'Q'))).grid(row = 0, column = 0)
            tk.Button(frame, text = chr(ord('♖') + plus), font = ('Monospaced', 30), height = 1,
                      command = lambda: promote(frame, (rank, file, 'R'))).grid(row = 0, column = 1)
            tk.Button(frame, text = chr(ord('♗') + plus), font = ('Monospaced', 30), height = 1,
                      command = lambda: promote(frame, (rank, file, 'B'))).grid(row = 1, column = 0)
            tk.Button(frame, text = chr(ord('♘') + plus), font = ('Monospaced', 30), height = 1,
                      command = lambda: promote(frame, (rank, file, 'N'))).grid(row = 1, column = 1)
            window.update()
            frame.place(x = window.winfo_width() / 8 * 3, y = window.winfo_height() / 8 * 3)
        else:
            play((rank, file))
    elif position.board[rank][file].colour == turn:
        if piece == position.board[rank][file]:
            piece = None
        else:
            piece = position.board[rank][file]
            movable = piece.movable_to(position)
            for move in movable:
                square = squares[move[0]][move[1]]
                square.config(text = '•' if square['text'] == ' ' else square['text'],
                              fg = 'green')


init()
