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

import numpy as np
import pygame
import sys

# Initialize pygame
pygame.init()

# Constants

ROWS, COLS = 10, 9
SQUARE_SIZE = 80
WIDTH, HEIGHT = COLS * SQUARE_SIZE,  ROWS  * SQUARE_SIZE

LINE_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 228, 181)  # light beige
RIVER_TEXT_COLOR = (0, 0, 128)
FONT_SIZE = 36

# Setup window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chinese Chess Board")
font = pygame.font.Font("NotoSansSC-VariableFont_wght.ttf", FONT_SIZE)

class Piece:
  def __init__(self,name,color,position):
    self.name = name
    self.color = color
    self.position = position


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


  def init_piece(self):
    pieces = [
        Piece("R","black",(1,1)),
        Piece("H","black",(1,2)),
        Piece("E","black",(1,3)),
        Piece("A","black",(1,4)),
        Piece("G","black",(1,5)),
        Piece("A","black",(1,6)),
        Piece("E","black",(1,7)),
        Piece("H","black",(1,8)),
        Piece("R","black",(1,9)),
        Piece("C","black",(3,2)),
        Piece("C","black",(3,8)),
        Piece("S","black",(4,1)),
        Piece("S","black",(4,3)),
        Piece("S","black",(4,5)),
        Piece("S","black",(4,7)),
        Piece("S","black",(4,9)),
      ] + [
        Piece("R","red",(10,1)),
        Piece("H","red",(10,2)),
        Piece("E","red",(10,3)),
        Piece("A","red",(10,4)),
        Piece("G","red",(10,5)),
        Piece("A","red",(10,6)),
        Piece("E","red",(10,7)),
        Piece("H","red",(10,8)),
        Piece("R","red",(10,9)),
        Piece("C","red",(8,2)),
        Piece("C","red",(8,8)),
        Piece("S","red",(7,1)),
        Piece("S","red",(7,3)),
        Piece("S","red",(7,5)),
        Piece("S","red",(7,7)),
        Piece("S","red",(7,9)),
      ]
    self.pieces = pieces

  def put_piece(self):
    # put the pieces on the board
    for piece in self.pieces:
      x, y = piece.position
      self.board[x][y] = piece

  def get_position(self,x,y):
      # return the position on the pixel graph given a position on the chessboard
      # x denotes the row and y denotes the column, so we need to flip them
      assert 1 <= x <= ROWS and 1 <= y <= COLS
      return y * SQUARE_SIZE - SQUARE_SIZE / 2, x * SQUARE_SIZE - SQUARE_SIZE / 2
  
  def draw_board(self):
      # draw the board
      screen.fill(BACKGROUND_COLOR)
      # first, generate the border of the board
      top_left = self.get_position(1,1)
      top_right = self.get_position(1,9)
      bottom_left = self.get_position(10,1)
      bottom_right = self.get_position(10,9)
      pygame.draw.line(screen, LINE_COLOR, top_left, top_right,5)
      pygame.draw.line(screen, LINE_COLOR, top_right, bottom_right,5)
      pygame.draw.line(screen, LINE_COLOR, bottom_right, bottom_left,5)
      pygame.draw.line(screen, LINE_COLOR, bottom_left, top_left,5)
      # draw the river
      river_tl = self.get_position(5,1)
      river_tr = self.get_position(5,9)
      river_bl = self.get_position(6,1)
      river_br = self.get_position(6,9)
      pygame.draw.line(screen, LINE_COLOR, river_tl, river_tr,5)
      pygame.draw.line(screen, LINE_COLOR, river_bl, river_br,5)
      # draw the river text
      river_text = font.render("楚河", True, RIVER_TEXT_COLOR)
      screen.blit(river_text, (WIDTH / 2 - 2 * SQUARE_SIZE, HEIGHT / 2 - SQUARE_SIZE / 2))
      river_text = font.render("漢界", True, RIVER_TEXT_COLOR)
      screen.blit(river_text, (WIDTH / 2 + SQUARE_SIZE, HEIGHT / 2 - SQUARE_SIZE / 2))
      # draw the horizontal lines
      for i in range(1, ROWS):
          pygame.draw.line(screen, LINE_COLOR, self.get_position(i,1), self.get_position(i,COLS), 2)
      # draw the vertical lines
      for i in range(1, COLS):
          pygame.draw.line(screen, LINE_COLOR, self.get_position(1,i), self.get_position(5,i), 2)
          pygame.draw.line(screen, LINE_COLOR, self.get_position(6,i), self.get_position(10,i), 2)

      # draw the palace
      palace1_tl = self.get_position(1,4)
      palace1_tr = self.get_position(3,4)
      palace1_bl = self.get_position(1,6)
      palace1_br = self.get_position(3,6)
      pygame.draw.line(screen, LINE_COLOR, palace1_tl, palace1_br, 2)
      pygame.draw.line(screen, LINE_COLOR, palace1_tr, palace1_bl, 2)
      palace2_tl = self.get_position(8,4)
      palace2_tr = self.get_position(10,4)
      palace2_bl = self.get_position(8,6)
      palace2_br = self.get_position(10,6)
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
      # draw the pieces on the board
      for piece in self.pieces:
          x, y = piece.position
          color = (255,0,0) if piece.color == "red" else (0,0,0)
          font_color = (0,0,0) if piece.color == "red" else (255,0,0)
          position = self.get_position(x,y)
          pygame.draw.circle(screen, color, position, SQUARE_SIZE / 2 - 5)
          if enable_Chin_chracter:
             name = self.get_Chin_chracter(piece)
          else:
             name = piece.name
          text = font.render(name, True, font_color)
          text_rect = text.get_rect(center=(position[0], position[1]))
          screen.blit(text, text_rect)


def main():
    clock = pygame.time.Clock()
    board = Board()
    board.draw_board()
    board.draw_piece()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        pygame.display.flip()
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
