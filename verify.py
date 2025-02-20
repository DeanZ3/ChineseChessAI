from pieces import Side
from pieces import Piece

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

def verify(move):
  [piece,cur_col,cur_row,new_col,new_row] = move.replace(',', ' ').split()
  cur_col = int(cur_col)
  cur_row = int(cur_row)
  new_col = int(new_col)
  new_row = int(new_row)
  if piece == "A":
    verify_advisor(cur_col,cur_row,new_col,new_row)
  elif piece == "E":
    verify_elephant(cur_col,cur_row,new_col,new_row)
  elif piece == "C":
    verify_cannon(cur_col,cur_row,new_col,new_row)
  elif piece == "R":
    verify_chariot(cur_col,cur_row,new_col,new_row)
  elif piece == "G":
    verify_general(cur_col,cur_row,new_col,new_row)
  elif piece == "H":
    verify_horse(cur_col,cur_row,new_col,new_row)
  else: # piece == "S"
    verify_soldier(cur_col,cur_row,new_col,new_row)



def verify_advisor(cur_col,cur_row,new_col,new_row):
  pass
def verify_general(cur_col,cur_row,new_col,new_row):
  pass
def verify_elephant(cur_col,cur_row,new_col,new_row):
  pass
def verify_cannon(cur_col,cur_row,new_col,new_row):
  pass
def verify_chariot(cur_col,cur_row,new_col,new_row):
  pass
def verify_horse(cur_col,cur_row,new_col,new_row):
  pass
def verify_soldier(cur_col,cur_row,new_col,new_row):
  pass

verify("A 1,4 2,5")