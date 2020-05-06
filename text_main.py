from position import Position
from piece import get_piece
from king import King
from queen import Queen
from rook import Rook
from bishop import Bishop
from knight import Knight
from pawn import Pawn
from re import fullmatch


def prep(move_input):
    if fullmatch('0-0(-0)?', move_input.replace('O', '0')):
        return move_input
    if len(move_input) < 2:
        return None
    if move_input[0] in 'abcdefgh':
        move_input = 'P' + move_input
    elif move_input[0] not in 'NBRQK':
        return None
    move_input = move_input.replace('x', '')
    move_input = move_input.replace('=', '')
    while move_input[-1] not in '12345678NBRQK':
        move_input = move_input[:-1]
    return move_input


def move(move_input):
    if move_input is None:
        print('Illegal syntax.')
        return False
    normal_move = bool(fullmatch('[PNBRQK][a-h]?[1-8]?[a-h][1-8]', move_input))
    promotion = bool(fullmatch('P[a-h]?[1-8]?[a-h][18][NBRQ]', move_input))
    castling = bool(fullmatch('0-0(-0)?', move_input.replace('O', '0')))

    if not (castling or promotion or normal_move):
        print('Invalid syntax')
        return False

    if normal_move or promotion:
        if promotion:
            promotion_piece = move_input[-1]
            move_input = move_input[:-1]
        rank = int(move_input[-1]) - 1
        file = ord(move_input[-2]) - ord('a')
        origin_rank = origin_file = None
        if len(move_input) == 4:
            if move_input[1] in 'abcdefgh':
                origin_file = ord(move_input[1]) - ord('a')
            else:
                origin_rank = int(move_input[1]) - 1

        switch = {
            'P': Pawn,
            'N': Knight,
            'B': Bishop,
            'R': Rook,
            'Q': Queen,
            'K': King
        }
        movable_pieces = []
        for piece in pieces:
            if type(piece) == switch[move_input[0]] and piece.colour == turn:
                if origin_rank is not None and piece.rank != origin_rank:
                    continue
                if origin_file is not None and piece.file != origin_file:
                    continue
                if promotion:
                    if piece.can_promote_to(position, rank, file):
                        movable_pieces.append(piece)
                elif piece.can_move_to(position, rank, file):
                    movable_pieces.append(piece)

        if len(movable_pieces) == 0:
            print('Illegal move.')
            return False
        elif len(movable_pieces) == 1:
            pieces.remove(movable_pieces[0])
            if promotion:
                moved_piece = movable_pieces[0].move((rank, file, promotion_piece))
                pieces.append(moved_piece)
            elif type(movable_pieces[0]) == King and abs(file - movable_pieces[0].file) == 2:
                castling = True
                move_input = '0-0' if file == 6 else '0-0-0'
                pieces.append(movable_pieces[0])
            else:
                moved_piece = movable_pieces[0].move((rank, file))
                pieces.append(moved_piece)
                    
            if position.board[rank][file] is not None:
                pieces.remove(position.board[rank][file])
                global num_of_moves
                num_of_moves = 0
            elif type(movable_pieces[0]) == Pawn:
                num_of_moves = 0
                if moved_piece.file != movable_pieces[0].file:
                    pieces.remove(position.board[rank - turn][file])
                elif abs(moved_piece.rank - movable_pieces[0].rank) == 2:
                    global double_mover
                    double_mover = moved_piece
        else:
            print(f'Ambiguity: {len(movable_pieces)} pieces are qualified for the move')
            return False

    if castling:
        king = position.king
        if len(move_input) == 3:
            file, rook_file = 6, 5
            rook = position.board[king.rank][7]
        else:
            file, rook_file = 2, 3
            rook = position.board[king.rank][0]

        if not king.can_castle(position, file):
            print('Illegal move.')
            return False

        pieces.remove(king)
        pieces.remove(rook)
        pieces.append(king.move((king.rank, file)))
        pieces.append(rook.move((rook.rank, rook_file)))
    
    return True


def threefold_repetition(all_positions, position):
    all_positions[position] = all_positions.get(position, 0) + 1
    return all_positions[position] > 2


def init():
    global pieces, turn, position, all_positions, double_mover, num_of_moves
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


def play():
    global turn, position, pieces, num_of_moves
    end = stuck = checkmate = threefold = fifty = insufficient = False
    while not end:
        print(position)
        if position.check:
            print('CHECK!');
        if turn == 1:
            move_input = input('Move for White: ')
        else:
            move_input = input('Move for Black: ')
        if not move(prep(move_input)):
            continue
        num_of_moves += 1
        turn = -turn
        position = Position(pieces, turn, double_mover)
        stuck = position.stuck()
        checkmate = stuck and position.check
        threefold = threefold_repetition(all_positions, position)
        fifty = num_of_moves >= 100
        insufficient = position.insufficient_material()
        end = stuck or threefold or fifty or insufficient

    print(position)
    if checkmate:
        if turn == 1:
            print('Black wins by checkmate!\n0-1')
        else:
            print('White wins by checkmate!\n1-0')
    else:
        if stuck:
            print('Draw by stalemate.')
        elif threefold:
            print('Draw by threefold repetition.')
        elif fifty:
            print('Draw by the Fifty Move Rule.')
        elif insufficient:
            print('Draw by insufficient material.')
        print('0.5-0.5')


init()

print('''Hello and welcome to PyChess!
This is a primitive text-based chess program, with a fully white Unicode chessboard.
Moves are entered in (case-sensitive) algebraic notation.
Two-player games are the only feature currently available.

To initiate a two-player game, enter 1.
For a tutorial on algebraic notation, enter 2.
To quit, enter any other number: ''', end='')

choice = int(input())
if choice == 1:
    play()
elif choice == 2:
    for i in range(1, 9):
        with open(f'tutorial_part_{i}.txt', 'r', encoding='utf-8') as tutorial:
            print(tutorial.read())
            if i < 8:
                ch = input("Press enter to continue or 'q' to quit the tutorial: ").lower()
                if ch == 'q':
                    break
    else:
        print('You are now ready to play!')
    print('-----------------------------------------------------------------------------')
    play()

print('See you next time.')
