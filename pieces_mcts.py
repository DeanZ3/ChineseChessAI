# In coding positions, we will use the standard notation/abbreviations from Wiki:
# A = 仕/士 (Advisor)
# C = 砲/炮 (Cannon)
# R = 俥/車 (Chariot)
# E = 相/象 (Elephant)
# G = 帥/將 (General)
# H = 傌/馬 (Horse)
# S = 兵/卒 (Soldier)
# Positions are encoded as a tuple (x,y), where x denotes the row and y denotes
# the column.


class Piece:
    def __init__(self,name,color,position):
        self.name = name
        self.color = color
        self.position = position

    def __eq__(self,other):
        if not isinstance(other, Piece):
            return False
        return self.name == other.name and self.color == other.color and self.position == other.position
    def __repr__(self):
        return f"Piece({self.name}, {self.color},{self.position})"

def verify(pos):
    return pos[0] in range(1,11) and pos[1] in range(1,10)

def avail_move(piece, board):
    # return a list of tuples:
    # the first element of the tuple is the position of the piece (another tuple)
    # the second element of the tuple is None if the position is empty, otherwise \
    # it is the enemy piece occupying the position
    assert board[piece.position[0]][piece.position[1]] == piece
    if piece.name == "A":
        return avail_move_advisor(piece, board)
    elif piece.name == "E":
        return avail_move_elephant(piece, board)
    elif piece.name == "C":
        return avail_move_cannon(piece, board)
    elif piece.name == "R":
        return avail_move_chariot(piece, board)
    elif piece.name == "G":
        return avail_move_general(piece, board)
    elif piece.name == "H":
        return avail_move_horse(piece, board)
    elif piece.name == "S":
        return avail_move_soldier(piece, board)
    else:
        raise ValueError("Invalid piece name")



def avail_move_advisor(piece, board):
    if piece.color == "red":
        all_possible_pos = [(10,4),(10,6),(9,5),(8,4),(8,6)]
    else:
        all_possible_pos = [(1,4),(1,6),(2,5),(3,4),(3,6)]
    assert piece.position in all_possible_pos
    # check if the position is occupied by the same color
    all_directions =  [(piece.position[0]+1, piece.position[1]+1), \
                (piece.position[0]+1, piece.position[1]-1), \
                  (piece.position[0]-1, piece.position[1]+1), \
                    (piece.position[0]-1, piece.position[1]-1)]
    # filter out cases when going out of the palace
    all_directions = [pos for pos in all_directions if pos in all_possible_pos]
    # filter out cases when the position is occupied by the same color
    all_directions = [pos for pos in all_directions if board[pos[0]][pos[1]] == None or board[pos[0]][pos[1]].color != piece.color]
    possible_moves = []
    for pos in all_directions:
        assert verify(pos)
        if board[pos[0]][pos[1]] == None:
            possible_moves.append((pos, None))
        else:
            possible_moves.append((pos, board[pos[0]][pos[1]]))
    
    return possible_moves

def avail_move_general(piece, board):
    if piece.color ==  "red":
        all_possible_pos = [(x,y) for x in range(8,11) for y in range(4,7)]
    else:
        all_possible_pos = [(x,y) for x in range(1,4) for y in range(4,7)]
    assert piece.position in all_possible_pos
    all_directions =  [(piece.position[0]+1, piece.position[1]), \
                (piece.position[0]-1, piece.position[1]), \
                  (piece.position[0], piece.position[1]+1), \
                    (piece.position[0], piece.position[1]-1)]
    # filter out cases when going out of the palace
    all_directions = [pos for pos in all_directions if pos in all_possible_pos]
    # filter out cases when the position is occupied by the same color
    all_directions = [pos for pos in all_directions if board[pos[0]][pos[1]] == None \
                      or board[pos[0]][pos[1]].color != piece.color]
    # IMPORTANT: the general cannot face each other, in the specific case when the generals are facing each other,
    # the general is able to kill the other general
    if piece.color == "red":
        # identify the piece that is right in front of the general
        for i in range(piece.position[0]-1,0, -1):
            target = board[i][piece.position[1]]
            if target != None and target.name == "G" and target.color == "black":
                all_directions.append((i,piece.position[1]))
                break
            elif target != None:
                break
    else:
        for i in range(piece.position[0]+1,11):
            target = board[i][piece.position[1]]
            if target != None and target.name == "G" and target.color == "red":
                all_directions.append((i,piece.position[1]))
                break
            elif target != None:
                break
    possible_moves = []
    for pos in all_directions:
        assert verify(pos)
        if board[pos[0]][pos[1]] == None:
            possible_moves.append((pos, None))
        else:
            possible_moves.append((pos, board[pos[0]][pos[1]]))
    return possible_moves

def avail_move_elephant(piece, board):
    if piece.color == "red":
        all_possible_pos = [(10,3),(10,7),(8,1),(8,5),(8,9),(6,3),(6,7)]
    else:
        all_possible_pos = [(1,3),(1,7),(3,1),(3,5),(3,9),(5,3),(5,7)]
    assert piece.position in all_possible_pos
    # check if the directions are blocked by other pieces
    all_directions = []
    if (piece.position[0]+2, piece.position[1]+2) in all_possible_pos and \
      board[piece.position[0]+1][piece.position[1]+1] == None:
        all_directions += [(piece.position[0]+2, piece.position[1]+2)]
    if (piece.position[0]+2, piece.position[1]-2) in all_possible_pos and \
      board[piece.position[0]+1][piece.position[1]-1] == None:
        all_directions += [(piece.position[0]+2, piece.position[1]-2)]
    if (piece.position[0]-2, piece.position[1]+2) in all_possible_pos and \
      board[piece.position[0]-1][piece.position[1]+1] == None:
        all_directions += [(piece.position[0]-2, piece.position[1]+2)]
    if (piece.position[0]-2, piece.position[1]-2) in all_possible_pos and \
      board[piece.position[0]-1][piece.position[1]-1] == None:  
        all_directions += [(piece.position[0]-2, piece.position[1]-2)] 
    # filter out cases when the position is occupied by the same color
    all_directions = [pos for pos in all_directions if board[pos[0]][pos[1]] == None \
                      or board[pos[0]][pos[1]].color != piece.color]
    possible_moves = []
    for pos in all_directions:
        assert verify(pos)
        if board[pos[0]][pos[1]] == None:
            possible_moves.append((pos, None))
        else:
            possible_moves.append((pos, board[pos[0]][pos[1]]))
    return possible_moves

def avail_move_chariot(piece, board):
    all_directions = []
    # check the right direction
    for i in range(piece.position[1]+1,10):
        if board[piece.position[0]][i] == None:
            all_directions.append((piece.position[0],i))
        else:
            all_directions.append((piece.position[0],i))
            break
    # check the left direction
    for i in range(piece.position[1]-1,0,-1):
        if board[piece.position[0]][i] == None:
            all_directions.append((piece.position[0],i))
        else:
            all_directions.append((piece.position[0],i))
            break
    # check the up direction
    for i in range(piece.position[0]-1,0,-1):
        if board[i][piece.position[1]] == None:
            all_directions.append((i,piece.position[1]))
        else:
            all_directions.append((i,piece.position[1]))
            break
    # check the down direction
    for i in range(piece.position[0]+1,11):
        if board[i][piece.position[1]] == None:
            all_directions.append((i,piece.position[1]))
        else:
            all_directions.append((i,piece.position[1]))
            break
    # filter out cases when the position is occupied by the same color
    all_directions = [pos for pos in all_directions if board[pos[0]][pos[1]] == None \
                      or board[pos[0]][pos[1]].color != piece.color]
    possible_moves = []
    for pos in all_directions:
        assert verify(pos)
        if board[pos[0]][pos[1]] == None:
            possible_moves.append((pos, None))
        else:
            possible_moves.append((pos, board[pos[0]][pos[1]]))
    return possible_moves 

def avail_move_cannon(piece, board):
    all_directions = []
    # check the right direction
    attack = False
    for i in range(piece.position[1]+1,10):
        if board[piece.position[0]][i] == None and not attack:
            all_directions.append((piece.position[0],i))
        elif board[piece.position[0]][i] != None and not attack:
            attack = True
        elif board[piece.position[0]][i] != None and attack:
            if board[piece.position[0]][i].color != piece.color:
                # fire
                all_directions.append((piece.position[0],i))
                break
            else:
                # blocked
                break
        elif board[piece.position[0]][i] == None and attack:
            pass
    attack = False
    # check the left direction
    for i in range(piece.position[1]-1,0,-1):
        if board[piece.position[0]][i] == None and not attack:
            all_directions.append((piece.position[0],i))
        elif board[piece.position[0]][i] != None and not attack:
            attack = True
        elif board[piece.position[0]][i] != None and attack:
            if board[piece.position[0]][i].color != piece.color:
                # fire
                all_directions.append((piece.position[0],i))
                break
            else:
                # blocked
                break
        elif board[piece.position[0]][i] == None and attack:
            pass
    attack = False
    # check the up direction
    for i in range(piece.position[0]-1,0,-1):
        if board[i][piece.position[1]] == None and not attack:
            all_directions.append((i,piece.position[1]))
        elif board[i][piece.position[1]] != None and not attack:
            attack = True
        elif board[i][piece.position[1]] != None and attack:
            if board[i][piece.position[1]].color != piece.color:
                # fire
                all_directions.append((i,piece.position[1]))
                break
            else:
                # blocked
                break
        elif board[i][piece.position[1]] == None and attack:
            pass
    attack = False
    # check the down direction
    for i in range(piece.position[0]+1,11):
        if board[i][piece.position[1]] == None and not attack:
            all_directions.append((i,piece.position[1]))
        elif board[i][piece.position[1]] != None and not attack:
            attack = True
        elif board[i][piece.position[1]] != None and attack:
            if board[i][piece.position[1]].color != piece.color:
                # fire
                all_directions.append((i,piece.position[1]))
                break
            else:
                # blocked
                break
        elif board[i][piece.position[1]] == None and attack:
            pass
            
    possible_moves = []
    for pos in all_directions:
        assert verify(pos)
        if board[pos[0]][pos[1]] == None:
            possible_moves.append((pos, None))
        else:
            possible_moves.append((pos, board[pos[0]][pos[1]]))
    return possible_moves

def avail_move_horse(piece, board):
    all_directions = []
    # check the right direction
    right_pos = (piece.position[0],piece.position[1]+1)
    if verify(right_pos) and board[right_pos[0]][right_pos[1]] == None:
        pos1 = (piece.position[0]+1,piece.position[1] + 2)
        pos2 = (piece.position[0]-1,piece.position[1] + 2)
        if verify(pos1) and (board[pos1[0]][pos1[1]] == None or board[pos1[0]][pos1[1]].color != piece.color):
            all_directions.append(pos1)
        if verify(pos2) and (board[pos2[0]][pos2[1]] == None or board[pos2[0]][pos2[1]].color != piece.color):
            all_directions.append(pos2)
    # check the left direction
    left_pos = (piece.position[0],piece.position[1]-1)
    if verify(left_pos) and board[left_pos[0]][left_pos[1]] == None:
        pos1 = (piece.position[0]+1,piece.position[1] - 2)
        pos2 = (piece.position[0]-1,piece.position[1] - 2)
        if verify(pos1) and (board[pos1[0]][pos1[1]] == None or board[pos1[0]][pos1[1]].color != piece.color):
            all_directions.append(pos1)
        if verify(pos2) and (board[pos2[0]][pos2[1]] == None or board[pos2[0]][pos2[1]].color != piece.color):
            all_directions.append(pos2)
    # check the up direction
    up_pos = (piece.position[0]-1,piece.position[1])
    if verify(up_pos) and board[up_pos[0]][up_pos[1]] == None:
        pos1 = (piece.position[0]-2,piece.position[1] + 1)
        pos2 = (piece.position[0]-2,piece.position[1] - 1)
        if verify(pos1) and (board[pos1[0]][pos1[1]] == None or board[pos1[0]][pos1[1]].color != piece.color):
            all_directions.append(pos1)
        if verify(pos2) and (board[pos2[0]][pos2[1]] == None or board[pos2[0]][pos2[1]].color != piece.color):
            all_directions.append(pos2)
    # check the down direction
    down_pos = (piece.position[0]+1,piece.position[1])
    if verify(down_pos) and board[down_pos[0]][down_pos[1]] == None:
        pos1 = (piece.position[0]+2,piece.position[1] + 1)
        pos2 = (piece.position[0]+2,piece.position[1] - 1)
        if verify(pos1) and (board[pos1[0]][pos1[1]] == None or board[pos1[0]][pos1[1]].color != piece.color):
            all_directions.append(pos1)
        if verify(pos2) and (board[pos2[0]][pos2[1]] == None or board[pos2[0]][pos2[1]].color != piece.color):
            all_directions.append(pos2)
    possible_moves = []
    for pos in all_directions:
        assert verify(pos)
        if board[pos[0]][pos[1]] == None:
            possible_moves.append((pos, None))
        else:
            possible_moves.append((pos, board[pos[0]][pos[1]]))
    return possible_moves


def avail_move_soldier(piece, board):
    if piece.color == "red":
        # check if this soldier has passed the river
        if piece.position[0] > 5:
            all_directions = [(piece.position[0]-1, piece.position[1])]
        else:
            all_directions = [(piece.position[0]-1, piece.position[1]), \
                              (piece.position[0], piece.position[1]+1), \
                              (piece.position[0], piece.position[1]-1)]
    else:
        if piece.position[0] < 6:
            all_directions = [(piece.position[0]+1, piece.position[1])]
        else:
            all_directions = [(piece.position[0]+1, piece.position[1]), \
                              (piece.position[0], piece.position[1]+1), \
                              (piece.position[0], piece.position[1]-1)]
    # filter out cases when the position is occupied by the same color
    all_directions = [pos for pos in all_directions if pos[0] >= 1 and pos[0] <= 10 and pos[1] >=1 and pos[1]<10 and (board[pos[0]][pos[1]] == None \
                      or board[pos[0]][pos[1]].color != piece.color)]
    possible_moves = []
    for pos in all_directions:
        if not verify(pos):
            continue
        if board[pos[0]][pos[1]] == None:
            possible_moves.append((pos, None))
        else:
            possible_moves.append((pos, board[pos[0]][pos[1]]))
    return possible_moves
            