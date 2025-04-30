import random
from pieces import *


class Naive:
  def __init__(self, color = "black"):
    self.color = color
    self.piece_value = {
        "S": 1,    # Soldier before crossing the river
        "A": 2,    # Advisor
        "E": 2,    # Elephant
        "H": 4,    # Horse (Knight)
        "C": 4.5,  # Cannon
        "R": 9,    # Chariot (Rook)
        "G": 100   # General (still set high to prioritize survival)
    }
  
  def update_board(self,game):
    self.board = game.board
    self.pieces = [piece for piece in game.pieces if piece.color == self.color]

  def move(self):
      return self.random_move()



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
    return None, None # no move available

  
  # After implementing a new clever_move function, remember to change "move" function to update the behavior
  # piece is an object defined in pieces.py
  # move is a tuple of (new_position, killed_piece), for instance ((1,2), Piece("R","red",(1,2)))
  # the update_board function is already called in the main function, so you don't need to call it again
  # so the new clever_move functions should have access to self.pieces and self.board
  # self.board is a 2D array of pieces, where None denotes an empty position, and occupied positions with a Piece object,
  # see the Board class for more info
  # self.pieces is a list of pieces that are alive and belongs to the bot