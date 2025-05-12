# In coding positions, we will use the standard notation/abbreviations from Wiki:
# A = 仕/士 (Advisor)
# C = 砲/炮 (Cannon)
# R = 俥/車 (Chariot)
# E = 相/象 (Elephant)
# G = 帥/將 (General)
# H = 傌/馬 (Horse)
# S = 兵/卒 (Soldier)

import numpy as np
import pygame
import sys
import random
import math
from pieces_mcts import Piece, avail_move
from collections import deque
import copy

# Initialize pygame
pygame.init()

# Constants
ROWS, COLS = 10, 9
SQUARE_SIZE = 80
WIDTH, HEIGHT = COLS * SQUARE_SIZE, ROWS * SQUARE_SIZE
PIECE_SIZE = SQUARE_SIZE // 2 - 5
POSSIBLE_MOVE_SIZE = SQUARE_SIZE // 3
LINE_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 228, 181)  # light beige
RIVER_TEXT_COLOR = (0, 0, 128)
FONT_SIZE = 36

# Game States
SHOWING_POSSIBLE_MOVES = 0
WAITING_FOR_MOVE = 1
AI_MOVING = 2

# Setup window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chinese Chess Board")
font = pygame.font.Font("NotoSansSC-VariableFont_wght.ttf", FONT_SIZE)


class Piece:
    def __init__(self, name, color, position):
        self.name = name
        self.color = color
        self.position = position
        self.selected_piece = None
        self.selected_avail_moves = []

class Board:
    def __init__(self):
        # Initialize the board with all open positions as None, for positions with 0, they are open and would not be used
        # IMPORTANT: board[i][j] denotes the piece at the ith row and jth column
        # IMPORTANT: board[i][j] denotes the piece at the ith row and jth column
        # IMPORTANT: board[i][j] denotes the piece at the ith row and jth column
        # the board would be used for calculations
        self.board = [[None for _ in range(COLS + 1)] for _ in range(ROWS + 1)]
        # initialize all the pieces at the start of the game as alive at their starting positions
        self.init_piece()
        self.dead_pieces = []
        self.put_piece()
        self.game_state = WAITING_FOR_MOVE
        self.turn = "red"
        self.winning = None
        self.bot = Bot("black")

    def custom_init(self,pieces,dead_pieces,turn,bot):
        self.pieces = pieces
        self.dead_pieces = dead_pieces
        self.put_piece()
        self.game_state = WAITING_FOR_MOVE
        self.turn = turn
        self.winning = None
        self.bot = bot

    def _switch_turn(self):
        if self.turn == "red":
            self.turn = "black"
        else:
            self.turn = "red"

    def init_piece(self):
        pieces = [
                     Piece("R", "black", (1, 1)),
                     Piece("H", "black", (1, 2)),
                     Piece("E", "black", (1, 3)),
                     Piece("A", "black", (1, 4)),
                     Piece("G", "black", (1, 5)),
                     Piece("A", "black", (1, 6)),
                     Piece("E", "black", (1, 7)),
                     Piece("H", "black", (1, 8)),
                     Piece("R", "black", (1, 9)),
                     Piece("C", "black", (3, 2)),
                     Piece("C", "black", (3, 8)),
                     Piece("S", "black", (4, 1)),
                     Piece("S", "black", (4, 3)),
                     Piece("S", "black", (4, 5)),
                     Piece("S", "black", (4, 7)),
                     Piece("S", "black", (4, 9)),
                 ] + [
                     Piece("R", "red", (10, 1)),
                     Piece("H", "red", (10, 2)),
                     Piece("E", "red", (10, 3)),
                     Piece("A", "red", (10, 4)),
                     Piece("G", "red", (10, 5)),
                     Piece("A", "red", (10, 6)),
                     Piece("E", "red", (10, 7)),
                     Piece("H", "red", (10, 8)),
                     Piece("R", "red", (10, 9)),
                     Piece("C", "red", (8, 2)),
                     Piece("C", "red", (8, 8)),
                     Piece("S", "red", (7, 1)),
                     Piece("S", "red", (7, 3)),
                     Piece("S", "red", (7, 5)),
                     Piece("S", "red", (7, 7)),
                     Piece("S", "red", (7, 9)),
                 ]
        self.pieces = pieces

    def put_piece(self):
        # put the pieces on the board
        for piece in self.pieces:
            x, y = piece.position
            self.board[x][y] = piece

    def get_position(self, x, y):
        # DRAWING_METHOD: return the position on the pixel graph given a position on the chessboard
        # x denotes the row and y denotes the column, so we need to flip them
        assert 1 <= x <= ROWS and 1 <= y <= COLS
        return y * SQUARE_SIZE - SQUARE_SIZE / 2, x * SQUARE_SIZE - SQUARE_SIZE / 2

    def draw_board(self):
        # draw the board, only need to be called once
        screen.fill(BACKGROUND_COLOR)
        # first, generate the border of the board
        top_left = self.get_position(1, 1)
        top_right = self.get_position(1, 9)
        bottom_left = self.get_position(10, 1)
        bottom_right = self.get_position(10, 9)
        pygame.draw.line(screen, LINE_COLOR, top_left, top_right, 5)
        pygame.draw.line(screen, LINE_COLOR, top_right, bottom_right, 5)
        pygame.draw.line(screen, LINE_COLOR, bottom_right, bottom_left, 5)
        pygame.draw.line(screen, LINE_COLOR, bottom_left, top_left, 5)
        # draw the river
        river_tl = self.get_position(5, 1)
        river_tr = self.get_position(5, 9)
        river_bl = self.get_position(6, 1)
        river_br = self.get_position(6, 9)
        pygame.draw.line(screen, LINE_COLOR, river_tl, river_tr, 5)
        pygame.draw.line(screen, LINE_COLOR, river_bl, river_br, 5)
        # draw the river text
        river_text = font.render("楚河", True, RIVER_TEXT_COLOR)
        screen.blit(river_text, (WIDTH / 2 - 2 * SQUARE_SIZE, HEIGHT / 2 - SQUARE_SIZE / 2))
        river_text = font.render("漢界", True, RIVER_TEXT_COLOR)
        screen.blit(river_text, (WIDTH / 2 + SQUARE_SIZE, HEIGHT / 2 - SQUARE_SIZE / 2))
        # draw the horizontal lines
        for i in range(1, ROWS):
            pygame.draw.line(screen, LINE_COLOR, self.get_position(i, 1), self.get_position(i, COLS), 2)
        # draw the vertical lines
        for i in range(1, COLS):
            pygame.draw.line(screen, LINE_COLOR, self.get_position(1, i), self.get_position(5, i), 2)
            pygame.draw.line(screen, LINE_COLOR, self.get_position(6, i), self.get_position(10, i), 2)

        # draw the palace
        palace1_tl = self.get_position(1, 4)
        palace1_tr = self.get_position(3, 4)
        palace1_bl = self.get_position(1, 6)
        palace1_br = self.get_position(3, 6)
        pygame.draw.line(screen, LINE_COLOR, palace1_tl, palace1_br, 2)
        pygame.draw.line(screen, LINE_COLOR, palace1_tr, palace1_bl, 2)
        palace2_tl = self.get_position(8, 4)
        palace2_tr = self.get_position(10, 4)
        palace2_bl = self.get_position(8, 6)
        palace2_br = self.get_position(10, 6)
        pygame.draw.line(screen, LINE_COLOR, palace2_tl, palace2_br, 2)
        pygame.draw.line(screen, LINE_COLOR, palace2_tr, palace2_bl, 2)

    def get_Chin_chracter(self, piece):
        # return the Chinese character for the piece
        if piece.name == "R":
            return "車"
        elif piece.name == "H":
            return "馬"
        elif piece.name == "E" and piece.color == "red":
            return "相"
        elif piece.name == "E" and piece.color == "black":
            return "象"
        elif piece.name == "A" and piece.color == "black":
            return "士"
        elif piece.name == "A" and piece.color == "red":
            return "仕"
        elif piece.name == "G" and piece.color == "black":
            return "將"
        elif piece.name == "G" and piece.color == "red":
            return "帥"
        elif piece.name == "C" and piece.color == "red":
            return "炮"
        elif piece.name == "C" and piece.color == "black":
            return "砲"
        elif piece.name == "S" and piece.color == "black":
            return "卒"
        elif piece.name == "S" and piece.color == "red":
            return "兵"
        else:
            raise ValueError("Invalid piece name")

    def draw_piece(self, enable_Chin_chracter=True):
        # draw the pieces on the board, this need to be called every update
        for piece in self.pieces:
            x, y = piece.position
            color = (255, 0, 0) if piece.color == "red" else (0, 0, 0)
            font_color = (0, 0, 0) if piece.color == "red" else (255, 0, 0)
            position = self.get_position(x, y)
            pygame.draw.circle(screen, color, position, PIECE_SIZE)
            if enable_Chin_chracter:
                name = self.get_Chin_chracter(piece)
            else:
                name = piece.name
            text = font.render(name, True, font_color)
            text_rect = text.get_rect(center=(position[0], position[1]))
            screen.blit(text, text_rect)

    def draw_turn(self):
        # draw the turn of the player
        text = font.render(f"{self.turn}'s turn", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(text, text_rect)

    def execute_move(self,piece,move):
        if piece is not None and move is not None:
            # move the piece to the new position
            self.board[piece.position[0]][piece.position[1]] = None
            piece.position = move[0]
            self.board[move[0][0]][move[0][1]] = piece
            # check if any enemy piece is killed
            if move[1] is not None:
                self.dead_pieces.append(move[1])
                self.pieces.remove(move[1])
                # check if the game is over
                if move[1].name == "G":
                    self.winning = self.turn
            # print("AI moved")
        else:
            pass
            # print("AI cannot move")

    def AI_move(self):
        print("AI is moving")
        if self.game_state != AI_MOVING:
            return  # AI is not moving
        assert self.turn == self.bot.color
        self.bot.update_board(self)
        piece, move = self.bot.move(self)
        self.execute_move(piece,move)
        # reset the selected piece and possible moves
        self.selected_piece = None
        self.selected_avail_moves = []
        self._switch_turn()
        self.game_state = WAITING_FOR_MOVE
        self.update()


    def deal_with_click(self, x, y):
        if self.game_state == AI_MOVING:
            return  # AI is moving

        if self.game_state == WAITING_FOR_MOVE:
            if self.cannot_move():
                self.winning = "black" if self.turn == "red" else "red"
            # first check which piece is clicked
            for piece in self.pieces:
                if piece.color != self.turn:
                    continue
                x_piece, y_piece = piece.position
                position = self.get_position(x_piece, y_piece)
                if np.sqrt((position[0] - x) ** 2 + (position[1] - y) ** 2) < PIECE_SIZE:
                    self.selected_piece = piece
                    self.selected_avail_moves = avail_move(piece, self.board)
                    self.game_state = SHOWING_POSSIBLE_MOVES
                    return
        elif self.game_state == SHOWING_POSSIBLE_MOVES:
            # check if the click is on the possible moves
            if self.selected_avail_moves == []:
                self.game_state = WAITING_FOR_MOVE
                return
            for moves in self.selected_avail_moves:
                pos = self.get_position(moves[0][0], moves[0][1])
                if np.sqrt((pos[0] - x) ** 2 + (pos[1] - y) ** 2) < POSSIBLE_MOVE_SIZE:
                    # move the piece to the new position
                    self.board[self.selected_piece.position[0]][self.selected_piece.position[1]] = None
                    self.selected_piece.position = moves[0]
                    self.board[moves[0][0]][moves[0][1]] = self.selected_piece
                    # check if any enemy piece is killed
                    if moves[1] is not None:
                        self.dead_pieces.append(moves[1])
                        self.pieces.remove(moves[1])
                        # check if the game is over
                        if moves[1].name == "G":
                            self.winning = self.turn
                    # reset the selected piece and possible moves
                    self.selected_piece = None
                    self.selected_avail_moves = []
                    self._switch_turn()
                    self.game_state = AI_MOVING
                    self.AI_move()
                else:
                    self.game_state = WAITING_FOR_MOVE

    def cannot_move(self):
        total_moves = []
        for piece in self.pieces:
            if piece.color == self.turn:
                total_moves += avail_move(piece, self.board)
        return len(total_moves) == 0

    def draw_possible_moves(self):
        if self.game_state != SHOWING_POSSIBLE_MOVES:
            return
        # first highlight the selected piece, draw a circle around it but not filled
        x, y = self.selected_piece.position
        position = self.get_position(x, y)
        pygame.draw.circle(screen, (255, 255, 255), position, PIECE_SIZE)
        # draw the possible moves
        for moves in self.selected_avail_moves:
            pos = self.get_position(moves[0][0], moves[0][1])
            pygame.draw.circle(screen, (0, 255, 0), pos, POSSIBLE_MOVE_SIZE)

    def update(self):
        # update the board
        self.draw_board()
        self.draw_piece()
        self.draw_possible_moves()
        self.draw_turn()

        pygame.display.flip()


class Node:
    # b is a Board object
    def __init__(self, b, parent, turn):
        self.board = b
        self.parent = parent
        self.children = dict()
        self.num_children = len(self.children)
        self.reward = 0
        self.turn = turn
        self.value = 0
        self.N = 0
        self.n = 0
        self.tried_moves = set()

class Bot:
    def __init__(self, color="black"):
        self.color = color
        self.piece_value = {
            "S": 1,  # Soldier before crossing the river
            "A": 2,  # Advisor
            "E": 2,  # Elephant
            "H": 4,  # Horse (Knight)
            "C": 4.5,  # Cannon
            "R": 9,  # Chariot (Rook)
            "G": 100  # General (still set high to prioritize survival)
        }

    def update_board(self, game):
        self.board = game.board
        self.pieces = [piece for piece in game.pieces if piece.color == self.color]

    def move(self, game):
        # return self.random_move()
        # return self.greedy_move()
        return self.mcts(game)

    def random_move(self):
        # Select a random piece and a random move
        all_moves = []
        for piece in self.pieces:
            moves = avail_move(piece, self.board)
            for move in moves:
                all_moves.append((piece, move))
        print(f"AI has {len(all_moves)} moves")
        if len(all_moves) > 0:
            (piece, move) = random.choice(all_moves)
            print(f"AI selected {piece.name} at {piece.position} to move to {move[0]} and kill {move[1]}")
            return piece, move
        return None, None  # no move available

    def greedy_move(self):
        best_score = -float("inf")
        best_move = None
        for piece in self.pieces:
            moves = avail_move(piece, self.board)
            for move in moves:
                captured_piece = move[1]
                score = self.piece_value.get(captured_piece.name, 0) if captured_piece else 0
                if score > best_score:
                    best_score = score
                    best_move = (piece, move)

        if best_move:
            piece, move = best_move
            print(f"[Greedy AI] Moving {piece.name} at {piece.position} to {move[0]} with score {best_score}")
            return piece, move

        # fallback if no "best" move
        print("[Greedy AI] No good move, falling back to random")
        return self.random_move()

    def swap_turn(self,turn):
        return "black" if turn == "red" else "red"

    def ucb1(self,node,c=2):
        return node.reward/(node.n + 1e-10) + c * math.sqrt(math.log(node.N + math.e + 1e-6)/(node.n + 1e-10))

    def get_all_moves(self,node):
        all_moves = set()
        for piece in node.board.pieces:
            if piece.color == node.turn:
                for move in avail_move(piece,node.board.board):
                    all_moves.add((piece,move))
        return all_moves

    # Need to differentiate between colors/turn?
    def selection(self,node):
        if len(node.children) == 0:
            return node
        max_ucb = 0
        selected_move = None
        for (piece,move) in node.children:
            cur_ucb = self.ucb1(node.children[(piece,move)])
            if max_ucb < cur_ucb:
                max_ucb = cur_ucb
                selected_move = (piece,move)
        return self.selection(node.children[selected_move])

    def expand(self,node):
        untried_moves = self.get_all_moves(node) - node.tried_moves
        rand_move = random.choice(list(untried_moves))
        node.tried_moves.add(rand_move)
        child_board = self.simulate_move(node.board,rand_move[0],rand_move[1])
        child = Node(child_board,node,self.swap_turn(node.turn))
        node.children.update({rand_move : child})
        return child

    def rollout(self,depth, max_depth, node):
        if node.board.winning is not None:
            if node.board.winning == "black":
                return 1
            elif node.board.winning == "red":
                return -1
            else:
                return 0
        if depth >= max_depth:
            return 0.5
        all_moves = self.get_all_moves(node)
        rand_move = random.choice(list(all_moves))
        new_board = self.simulate_move(node.board,rand_move[0],rand_move[1])
        new_node = Node(new_board,node,self.swap_turn(node.turn))
        reward = self.rollout(depth + 1, max_depth, new_node)

        return reward

    def backtrack(self,node,reward):
        node.n += 1
        node.reward += reward
        cur_node = node
        while cur_node.parent is not None:
            cur_node.N += 1
            cur_node = cur_node.parent

    def equals(self,p1,p2):
        return p1.name == p2.name and p1.color == p2.color and p1.position == p2.position

    def tostring(self,p):
        if p is None:
            return "None"
        return f"Piece({p.name}, {p.color},{p.position})"

    def simulate_move(self,game,piece,move):
        # Given the current board (game), and a move (piece,move), creates a new board object after the move is executed.

        # dead_pieces2 is a deep copy of game.dead_pieces
        dead_pieces2 = copy.deepcopy(game.dead_pieces)
        # dead_pieces2 = []
        # for i in range(len(game.dead_pieces)):
        #     dead_pieces2[i] = game.dead_pieces[i]
        pieces2 = copy.deepcopy(game.pieces)

        tmp_piece = piece
        tmp_move = move
        for p in pieces2:
            if self.equals(p,piece):
                tmp_piece = p
            if move[1] is not None:
                if self.equals(p,move[1]):
                    tmp_move = (move[0],p)

        new_board = Board()
        for x in range(ROWS + 1):
            for y in range(COLS + 1):
                new_board.board[x][y] = None

        new_board.custom_init(pieces2,dead_pieces2,game.turn,self)
        new_board.execute_move(tmp_piece,tmp_move)
        new_board.put_piece()
        new_board.turn = self.swap_turn(game.turn)
        return new_board


    def mcts(self, game, num_expand=100, num_rollout=50, rollout_depth = 10):
        # Creates a tree structure with current board (game) as the root with depth num_iter.
        # From a node n1, all possible next moves are simulated, and the resulting board state is stored in the
        # dictionary n1.children

        # game is a Board object
        best_score = -float("inf")
        best_move = None
        q = deque()

        # Do I need a visited set? Not sure...
        visited = set()
        root = Node(game, None, game.turn)
        for piece in game.pieces:
            if piece.color == root.turn:
                moves = avail_move(piece,game.board)
                for move in moves:
                    child_board = self.simulate_move(game,piece,move)
                    child_turn = self.swap_turn(game.turn)
                    child = Node(child_board,root,child_turn)
                    root.children.update({(piece,move) : child})

        for exp_iter in range(num_expand):
            print(exp_iter)
            start_node = self.selection(root)
            new_node = self.expand(start_node)
            net_reward = 0
            old_pieces = new_node.board.pieces
            for rollout_iter in range(num_rollout):
                reward = self.rollout(0, rollout_depth, new_node)
                after_rollout_pieces = new_node.board.pieces
                assert old_pieces == after_rollout_pieces
                old_pieces = after_rollout_pieces
                net_reward += reward

            self.backtrack(new_node,net_reward)

        max_ucb = 0
        selected_move = None
        for (piece,move) in root.children:
            cur_ucb = self.ucb1(root.children[(piece,move)])
            if cur_ucb > max_ucb:
                selected_move = (piece,move)
                max_ucb = cur_ucb

        return selected_move

    # After implementing a new clever_move function, remember to change "move" function to update the behavior
    # piece is an object defined in pieces.py
    # move is a tuple of (new_position, killed_piece), for instance ((1,2), Piece("R","red",(1,2)))
    # the update_board function is already called in the main function, so you don't need to call it again
    # so the new clever_move functions should have access to self.pieces and self.board
    # self.board is a 2D array of pieces, where None denotes an empty position, and occupied positions with a Piece object,
    # see the Board class for more info
    # self.pieces is a list of pieces that are alive and belongs to the bot


def main():
    clock = pygame.time.Clock()
    board = Board()
    board.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                board.deal_with_click(x, y)
                board.update()
            board.update()

        if board.winning is not None:
            print(f"{board.winning} wins!")
            break
        clock.tick(60)


if __name__ == "__main__":
    main()


def display_start_board(flip_board):
    print("Welcome to Chinese Chess! We hope you enjoy!")
    print("\n")
    if flip_board:
        print("1   2   3   4   5   6   7   8   9")
        print("俥-—傌--相--仕--帥--仕--相--傌--俥   1")
        print("|   |   |   |\  |  /|   |   |   |")
        print("|   |   |   | \ | / |   |   |   |")
        print("|   |   |   |  \|/  |   |   |   |")
        print("+---+---+---+---+---+---+---+---+    2")
        print("|   |   |   |  /|\  |   |   |   |")
        print("|   |   |   | / | \ |   |   |   |")
        print("|   |   |   |/  |  \|   |   |   |")
        print("+--炮---+---+---+---+---+---炮--+    3")
        print("|   |   |   |   |   |   |   |   |")
        print("|   |   |   |   |   |   |   |   |")
        print("|   |   |   |   |   |   |   |   |")
        print("兵--+---兵--+---兵--+---兵--+--兵    4")
        print("|   |   |   |   |   |   |   |   |")
        print("|   |   |   |   |   |   |   |   |")
        print("|   |   |   |   |   |   |   |   |")
        print("+---+---+---+---+---+---+---+---+    5")
        print("|                               |")
        print("|    楚河                楚河   |")
        print("|                               |")
        print("+---+---+---+---+---+---+---+---+    6")
        print("|   |   |   |   |   |   |   |   |")
        print("|   |   |   |   |   |   |   |   |")
        print("|   |   |   |   |   |   |   |   |")
        print("卒--+---卒--+---卒--+---卒--+--卒    7")
        print("|   |   |   |   |   |   |   |   |")
        print("|   |   |   |   |   |   |   |   |")
        print("|   |   |   |   |   |   |   |   |")
        print("+--砲---+---+---+---+---+---砲--+    8")
        print("|   |   |   |\  |  /|   |   |   |")
        print("|   |   |   | \ | / |   |   |   |")
        print("|   |   |   |  \|/  |   |   |   |")
        print("+---+---+---+---+---+---+---+---+    9")
        print("|   |   |   |  /|\  |   |   |   |")
        print("|   |   |   | / | \ |   |   |   |")
        print("|   |   |   |/  |  \|   |   |   |")
        print("車-—馬--象--士--將--士--象--馬--車   10")
        print("1   2   3   4   5   6   7   8   9")
    else:
        print("1   2   3   4   5   6   7   8   9")
        print("車-—馬--象--士--將--士--象--馬--車   10")
        print("|   |   |   |\  |  /|   |   |   |")
        print("|   |   |   | \ | / |   |   |   |")
        print("|   |   |   |  \|/  |   |   |   |")
        print("+---+---+---+---+---+---+---+---+    9")
        print("|   |   |   |  /|\  |   |   |   |")
        print("|   |   |   | / | \ |   |   |   |")
        print("|   |   |   |/  |  \|   |   |   |")
        print("+--砲---+---+---+---+---+---砲--+    8")
        print("|   |   |   |   |   |   |   |   |")
        print("|   |   |   |   |   |   |   |   |")
        print("|   |   |   |   |   |   |   |   |")
        print("卒--+---卒--+---卒--+---卒--+--卒    7")
        print("|   |   |   |   |   |   |   |   |")
        print("|   |   |   |   |   |   |   |   |")
        print("|   |   |   |   |   |   |   |   |")
        print("+---+---+---+---+---+---+---+---+    6")
        print("|                               |")
        print("|    楚河                楚河   |")
        print("|                               |")
        print("+---+---+---+---+---+---+---+---+    5")
        print("|   |   |   |   |   |   |   |   |")
        print("|   |   |   |   |   |   |   |   |")
        print("|   |   |   |   |   |   |   |   |")
        print("兵--+---兵--+---兵--+---兵--+--兵    4")
        print("|   |   |   |   |   |   |   |   |")
        print("|   |   |   |   |   |   |   |   |")
        print("|   |   |   |   |   |   |   |   |")
        print("+--炮---+---+---+---+---+---炮--+    3")
        print("|   |   |   |\  |  /|   |   |   |")
        print("|   |   |   | \ | / |   |   |   |")
        print("|   |   |   |  \|/  |   |   |   |")
        print("+---+---+---+---+---+---+---+---+  2")
        print("|   |   |   |  /|\  |   |   |   |")
        print("|   |   |   | / | \ |   |   |   |")
        print("|   |   |   |/  |  \|   |   |   |")
        print("俥-—傌--相--仕--帥--仕--相--傌--俥   1")
        print("1   2   3   4   5   6   7   8   9")