import random
from pieces import avail_move
from pieces import Piece


class Greedy1:
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
      # return self.random_move()
      return self.greedy_move()


  def random_move(self):
    # Select a random piece and a random move
    all_moves = []
    for piece in self.pieces:
        moves = avail_move(piece, self.board)
        for move in moves:
            all_moves.append((piece, move))
    if len(all_moves) > 0:
        (piece, move) = random.choice(all_moves)
        print(f"AI selected {piece.name} at {piece.position} to move to {move[0]} and kill {move[1]}")
        return piece, move
    return None, None # no move available

  def greedy_move(self):
        best_score = 0
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
  

class Greedy2:
  def __init__(self, color = "black", steps = 2):
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
    self.bot = _Greedy2_pos(color, self.piece_value)
    self.steps = steps
  
  def update_board(self,game):
    self.bot.update_board(game.board)


  def move(self):
      # return self.random_move()
      return self.bot.greedy_move(steps=self.steps)
  

class _Greedy2_pos:
    def __init__(self, color = "black", piece_value = None):
      self.color = color
      self.piece_value = piece_value 
    
    def update_board(self,board):
      self.board = board
      overall_pieces = []
      for row in board:
          for piece in row:
              if piece is not None:
                  overall_pieces.append(piece)
      self.pieces = [piece for piece in overall_pieces if piece.color == self.color]
      self.enemy_pieces = [piece for piece in overall_pieces if piece.color != self.color]

    def move(self):
        # return self.random_move()
        return self.greedy_move()


    def random_move(self):
      # Select a random piece and a random move
      all_moves = []
      for piece in self.pieces:
          moves = avail_move(piece, self.board)
          for move in moves:
              all_moves.append((piece, move))
      if len(all_moves) > 0:
          (piece, move) = random.choice(all_moves)
          print(f"AI selected {piece.name} at {piece.position} to move to {move[0]} and kill {move[1]}")
          return piece, move
      return None, None # no move available
    

    def evaluate_board(self,board):
          score = 0
          for row in board:
              for piece in row:
                  if piece is not None:
                      if piece.color == self.color:
                          score += self.piece_value.get(piece.name, 0)
                      else:
                          score -= self.piece_value.get(piece.name, 0)

          return score
    
    def _other_color(self):
        if self.color == "red":
            return "black"
        else:
            return "red"

    def greedy_move(self, steps = 5):
          if steps == 1:
            best_score = 0
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
                return piece, move

            # fallback if no "best" move
            return self.random_move()
          
          if steps == 2:
            best_score = 0
            best_move = None
            for piece in self.pieces:
                moves = avail_move(piece, self.board)
                for move in moves:
                    new_board = self._move_piece(self.board, piece, move)
                    oppo = _Greedy2_pos(self._other_color(), self.piece_value)
                    oppo.update_board(new_board)
                    piece_oppo, move_oppo = oppo.greedy_move(steps=1)
                    new_new_board = oppo._move_piece(new_board, piece_oppo, move_oppo)
                    score = self.evaluate_board(new_new_board)
                    if score > best_score:
                        best_score = score
                        best_move = (piece, move)
                    del oppo, new_board, new_new_board

            if best_move:
                piece, move = best_move
                return piece, move
            # fallback if no "best" move
            return self.random_move()
          
          else:
            best_score = 0
            best_move = None
            for piece in self.pieces:
                moves = avail_move(piece, self.board)
                for move in moves:
                    new_board = self._move_piece(self.board, piece, move)
                    oppo = _Greedy2_pos(self._other_color(), self.piece_value)
                    oppo.update_board(new_board)
                    piece_oppo, move_oppo = oppo.greedy_move(steps= steps - 1)
                    new_new_board = oppo._move_piece(new_board, piece_oppo, move_oppo)
                    score = self.evaluate_board(new_new_board)
                    if score > best_score:
                        best_score = score
                        best_move = (piece, move)
                    del oppo, new_board, new_new_board

            if best_move:
                piece, move = best_move
                return piece, move
            # fallback if no "best" move
            return self.random_move()
                    
              
    def _move_piece(self, board, piece, move):
        # create a new board object
        # Update the board with the move
        # need to deepcopy the board to avoid modifying the original, as well as the pieces

        new_board = []
        for row in board:
            new_row = []
            for cell in row:
                if isinstance(cell, Piece):
                    new_row.append(Piece.duplicate(cell))
                else:
                    # None
                    new_row.append(cell)
            new_board.append(new_row)

        new_board[piece.position[0]][piece.position[1]] = None
        new_board[move[0][0]][move[0][1]] = Piece.duplicate(piece)
        new_board[move[0][0]][move[0][1]].position = move[0]
        return new_board

    
