import numpy as np
import pygame
import sys
import random
import math
from pieces import Piece, avail_move
import copy
from collections import deque
from mcts import *
from board import Board

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

class MCTSAI:
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