import copy
import random
from pieces import avail_move, Piece


class Minimax:
    def __init__(self, color, depth=2, alpha_beta=True):
        self.color = color
        self.depth = depth
        self.alpha_beta = alpha_beta
        self.piece_value = {
            "S": 1,
            "A": 2,
            "E": 2,
            "H": 4,
            "C": 4.5,
            "R": 9,
            "G": 100,
        }

    def update_board(self, game):
        self.board = game.board
        self.pieces = [p for p in game.pieces if p.color == self.color]
        self.all_pieces = game.pieces

    def move(self):
        best_score = float("-inf")
        best_action = None
        history = []

        for piece in self.pieces:
            for move in avail_move(piece, self.board):
                new_board, new_pieces = self.simulate_move(
                    self.board, self.all_pieces, piece, move
                )
                score = (
                    self.minimax(
                        new_board,
                        new_pieces,
                        self.depth - 1,
                        False,
                        float("-inf"),
                        float("inf"),
                    )
                    if self.alpha_beta
                    else self.minimax(new_board, new_pieces, self.depth - 1, False)
                )
                if score > best_score:
                    best_score = score
                    best_action = (piece, move)

        return best_action if best_action else (None, None)

    def minimax(self, board, pieces, depth, maximizing, alpha=None, beta=None):
        color = (
            self.color if maximizing else ("red" if self.color == "black" else "black")
        )
        player_pieces = [p for p in pieces if p.color == color]

        if depth == 0 or not player_pieces:
            return self.evaluate_board(pieces)

        best_score = float("-inf") if maximizing else float("inf")
        for piece in player_pieces:
            for move in avail_move(piece, board):
                new_board, new_pieces = self.simulate_move(board, pieces, piece, move)
                score = (
                    self.minimax(
                        new_board, new_pieces, depth - 1, not maximizing, alpha, beta
                    )
                    if self.alpha_beta
                    else self.minimax(new_board, new_pieces, depth - 1, not maximizing)
                )

                if maximizing:
                    best_score = max(best_score, score)
                    if self.alpha_beta:
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
                else:
                    best_score = min(best_score, score)
                    if self.alpha_beta:
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
        return best_score

    def simulate_move(self, board, pieces, piece, move):
        # Create deep copies of the pieces
        piece_map = {}
        pieces_copy = []
        for p in pieces:
            new_p = Piece(p.name, p.color, p.position)
            piece_map[(p.color, p.position)] = new_p
            pieces_copy.append(new_p)

        # Create a deep copy of the board and replace with new piece objects
        board_copy = [[None for _ in range(10)] for _ in range(11)]
        for p in pieces_copy:
            x, y = p.position
            board_copy[x][y] = p

        # Apply the move
        moved_piece = piece_map[(piece.color, piece.position)]
        old_x, old_y = moved_piece.position
        new_pos, captured_piece = move
        new_x, new_y = new_pos

        board_copy[old_x][old_y] = None
        moved_piece.position = new_pos
        board_copy[new_x][new_y] = moved_piece

        # Remove captured piece if any
        if captured_piece:
            try:
                pieces_copy.remove(
                    piece_map[(captured_piece.color, captured_piece.position)]
                )
            except KeyError:
                pass  # may not exist if the piece wasn't copied because it was already "captured"

        return board_copy, pieces_copy

    def evaluate_board(self, pieces):
        score = 0
        for piece in pieces:
            value = self.piece_value.get(piece.name, 0)
            score += value if piece.color == self.color else -value
        return score
