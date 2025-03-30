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


class Piece:
  def __init__(self,name,color,position):
    self.name = name
    self.color = color
    self.position = position

class Side:
  def __init__(self,color):
    self.color = color
    self.pieces = self.init_pieces()
  def init_pieces(self):
    if self.color == "red":
      return [
        Piece("R","red",(1,1)),
        Piece("H","red",(2,1)),
        Piece("E","red",(3,1)),
        Piece("A","red",(4,1)),
        Piece("G","red",(5,1)),
        Piece("A","red",(6,1)),
        Piece("E","red",(7,1)),
        Piece("H","red",(8,1)),
        Piece("R","red",(9,1)),
        Piece("C","red",(2,2)),
        Piece("C","red",(8,2)),
        Piece("S","red",(1,4)),
        Piece("S","red",(3,4)),
        Piece("S","red",(5,4)),
        Piece("S","red",(7,4)),
        Piece("S","red",(9,4)),
      ]
    else:
      return [
        Piece("R","black",(1,10)),
        Piece("H","black",(2,10)),
        Piece("E","black",(3,10)),
        Piece("A","black",(4,10)),
        Piece("G","black",(5,10)),
        Piece("A","black",(6,10)),
        Piece("E","black",(7,10)),
        Piece("H","black",(8,10)),
        Piece("R","black",(9,10)),
        Piece("C","black",(2,8)),
        Piece("C","black",(8,8)),
        Piece("S","black",(1,7)),
        Piece("S","black",(3,7)),
        Piece("S","black",(5,7)),
        Piece("S","black",(7,7)),
        Piece("S","black",(9,7)),
      ]