import numpy as np
# In coding positions, we will use the standard notation/abbreviations from Wiki:
# A = 仕/士 (Advisor)
# C = 砲/炮 (Cannon)
# R = 俥/車 (Chariot)
# E = 相/象 (Elephant)
# G = 帥/將 (General)
# H = 傌/馬 (Horse)
# S = 兵/卒 (Soldier)
# Positions are encoded as a tuple (x,y), where x denotes the column and y denotes
# the row. 

# board[i][j] denotes the piece at the ith row and jth column, i.e. position (j,i)
# "O" denotes an open position. Otherwise, a position is denoted by the letters above.

class Board:
  def __init__(self):
    self.board = np.full((11, 10), "O", dtype=str)
    self.board = start_board(self.board)
    print(type(self.board))

def start_board(board):
  board[1][1] = "R"
  board[1][2] = "H"
  board[1][3] = "E"
  board[1][4] = "A"
  board[1][5] = "G"
  board[1][6] = "A" 
  board[1][7] = "E"
  board[1][8] = "H"
  board[1][9] = "R"
  board[3][2] = "C"
  board[3][8] = "C"
  board[4][1] = "S"
  board[4][3] = "S"
  board[4][5] = "S"
  board[4][7] = "S"
  board[4][9] = "S"

  board[10][1] = "R"
  board[10][2] = "H"
  board[10][3] = "E"
  board[10][4] = "A"
  board[10][5] = "G"
  board[10][6] = "A" 
  board[10][7] = "E"
  board[10][8] = "H"
  board[10][9] = "R"
  board[8][2] = "C"
  board[8][8] = "C"
  board[7][1] = "S"
  board[7][3] = "S"
  board[7][5] = "S"
  board[7][7] = "S"
  board[7][9] = "S"

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

display_start_board(False)

b = Board()