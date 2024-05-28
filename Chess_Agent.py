import chess
import chess.svg
import chess.polyglot
import chess.pgn
import numpy as np
import time
import chess.engine


pawn_table = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knight_table = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishop_table = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rook_table = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

queen_table = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

king_table = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]

white_king_flag = True
black_king_flag = True

pawn_table = np.array(pawn_table)
knight_table = np.array(knight_table)
bishop_table = np.array(bishop_table)
rook_table = np.array(rook_table)
queen_table = np.array(queen_table)
king_table = np.array(king_table)

def king_safety(board, color):
    king_square = board.king(color)
    safety_score = 0
    
    # Evaluate the number of pawns around the king
    for offset in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        square = king_square + chess.square(offset[0], offset[1])
        if 0 <= square < 64 and board.piece_at(square) == chess.Piece(chess.PAWN, color):
            safety_score += 10
    
    # Evaluate the number of enemy pieces around the king
    offsets = [
        (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
        (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),
        (0, -2), (0, -1), (0, 1), (0, 2),
        (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
        (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)
    ]

    for offset in offsets:
        square = king_square + chess.square(offset[0], offset[1])
        if 0 <= square < 64 and board.piece_at(square) != None and board.piece_at(square).color != color:
            safety_score -= 20
    
    return safety_score

def mobility(board, color):
    score = 0
    for piece_type in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
        piece_squares = board.pieces(piece_type, color)
        score += sum(1 for move in board.legal_moves if move.from_square in piece_squares)
    return score

def centralization(board, color):
    score = 0
    for square in [chess.E4, chess.D4, chess.E5, chess.D5]:
        if board.piece_at(square) != None and board.piece_at(square).color == color:
            score += 20
    return score

def pawn_structure(board, color):
    score = 0
    pawn_squares = board.pieces(chess.PAWN, color)
    
    # Reward pawn advancement
    for square in pawn_squares:
        rank = chess.square_rank(square)
        score += rank if color == chess.WHITE else 7 - rank
    
    # Penalize isolated pawns
    for square in pawn_squares:
        file = chess.square_file(square)
        if file > 0 and not any(pawn_squares & chess.SquareSet(chess.BB_FILES[file - 1])):
            score -= 2
        if file < 7 and not any(pawn_squares & chess.SquareSet(chess.BB_FILES[file + 1])):
            score -= 2
    
    # Penalize doubled pawns
    for file in range(8):
        if sum(1 for square in pawn_squares if chess.square_file(square) == file) > 1:
            score -= 2
    
    return score


def evaluate_board1(board):
    global white_king_flag
    global black_king_flag
    if board.is_checkmate():
        return -9999 if board.turn else 9999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    eval =     100 * (len(board.pieces(chess.PAWN, chess.WHITE)) - len(board.pieces(chess.PAWN, chess.BLACK))) + \
               300 * (len(board.pieces(chess.KNIGHT, chess.WHITE)) - len(board.pieces(chess.KNIGHT, chess.BLACK))) + \
               400 * (len(board.pieces(chess.BISHOP, chess.WHITE)) - len(board.pieces(chess.BISHOP, chess.BLACK))) + \
               600 * (len(board.pieces(chess.ROOK, chess.WHITE)) - len(board.pieces(chess.ROOK, chess.BLACK))) + \
               1000 * (len(board.pieces(chess.QUEEN, chess.WHITE)) - len(board.pieces(chess.QUEEN, chess.BLACK))) +\
           sum(pawn_table[i] for i in board.pieces(chess.PAWN, chess.WHITE)) - \
           sum(pawn_table[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)) + \
           sum(knight_table[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)) - \
           sum(knight_table[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)) + \
           sum(bishop_table[i] for i in board.pieces(chess.BISHOP, chess.WHITE)) - \
           sum(bishop_table[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)) + \
           sum(rook_table[i] for i in board.pieces(chess.ROOK, chess.WHITE)) - \
           sum(rook_table[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)) + \
           sum(queen_table[i] for i in board.pieces(chess.QUEEN, chess.WHITE)) - \
           sum(queen_table[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)) + \
           sum(king_table[i] for i in board.pieces(chess.KING, chess.WHITE)) - \
           sum(king_table[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)) +\
           mobility(board, chess.WHITE) - mobility(board, chess.BLACK) +\
           centralization(board, chess.WHITE) - centralization(board, chess.BLACK) +\
           pawn_structure(board, chess.WHITE) - pawn_structure(board, chess.BLACK) +\
           king_safety(board, chess.WHITE) - king_safety(board, chess.BLACK)    

    # Add a bonus for castled kings
    if white_king_flag and board.king(chess.WHITE) in [chess.G1, chess.C1]:
        white_king_flag = False
        eval += 80

    if black_king_flag and board.king(chess.BLACK) in [chess.G8, chess.C8]:
        black_king_flag = False
        eval -= 80
           
    return eval if board.turn else -eval

def quiesce1(alpha, beta, board):
    stand_pat = evaluate_board1(board)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce1(-beta, -alpha, board)
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        elif board.is_capture(move) and evaluate_board1(board.copy()) == stand_pat:
            board.push(move)
            score = -quiesce1(-beta, -alpha, board)
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

    return alpha


def alphabeta1(alpha, beta, depthleft,board):
    bestscore = -9999
    if (depthleft == 0):
        return quiesce1(alpha, beta,board)
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta1(-beta, -alpha, depthleft - 1,board)
        board.pop()
        if (score >= beta):
            return score
        if (score > bestscore):
            bestscore = score
        if (score > alpha):
            alpha = score
    return bestscore

def selectmove1(max_depth, board, time_limit):
    try:
        move = chess.polyglot.MemoryMappedReader("./human.bin").weighted_choice(board).move
        print("Book move: ", move)
        return move
    
    except:
        start_time = time.time()
        best_move = chess.Move.null()
        best_value = -99999
        alpha = -100000
        beta = 100000
        completed_depths = []
        completed_moves = []
        completed_scores = []

        for depth in range(1, max_depth + 1):
            for move in board.legal_moves:
                if time.time() - start_time > time_limit:
                    print("depth reached: ", depth-1)
                    
                    # If we have completed at least one search depth, return the best move from the last completed depth
                    if completed_depths:
                        return completed_moves[-1]
                    # If we haven't completed any depth, return the best move calculated so far
                    else:
                        return best_move

                board.push(move)
                board_value = -alphabeta1(-beta, -alpha, depth - 1, board)
                board.pop()

                if board_value > best_value:
                    best_value = board_value
                    best_move = move

            # Record the best move and its score for the current completed depth
            completed_depths.append(depth)
            completed_moves.append(best_move)
            completed_scores.append(best_value)

            print("Depth: ", depth, " | Best move: ", best_move, " | Best value: ", best_value)

        # Return the best move from the last completed search depth
        return completed_moves[-1]
    
class group1:
    def __init__(self, color):
        self.color = color

    def makemove(self, board):
        fen = board.fen().split(' ')[0]
        # 2 seconds buffer | should take 20 sec to play
        move = selectmove1(100, board, 18)
        retmove = board.uci(move)
        return retmove
    
class group2:
    def __init__(self, color):
        self.color = color

    def makemove(self, board):
        # 2 seconds buffer | should take 20 sec to play
        move = selectmove1(100, board, 18)
        retmove = board.uci(move)
        return retmove
