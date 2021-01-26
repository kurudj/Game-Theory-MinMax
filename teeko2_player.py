import random
import copy
import sys

class Teeko2Player:
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    dropPhase = True
    maxDepth = 2

    def __init__(self):
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def succ(self,state):
          successors = []
          count = 0
          value = self.my_piece
          for i in state:
              count+=i.count(self.my_piece)
          if count<4:
              self.dropPhase = True
          else:
              self.dropPhase = False
          if self.dropPhase:
              if len(state[0])==5:
                  for i in range(5):
                      for j in range(5):
                          stateCopy = copy.deepcopy(state)
                          if state[i][j]==' ' and count<4:
                              stateCopy[i][j] = value
                              tuple = ((i,j),stateCopy)
                              successors.append(tuple)
          else:
              for i in range(5):
                  stateCopy = copy.deepcopy(state)
                  for j in range(5):
                      stateCopy = copy.deepcopy(state)
                      if state[i][j]!=value:
                          continue
                      if state[i][j]==value:
                          if j+1<5:
                              if stateCopy[i][j+1] == ' ':
                                stateCopy[i][j+1] = value
                                stateCopy[i][j] = ' '
                                tuple = ((i,j+1),(i,j),stateCopy)
                                successors.append(tuple)
                                stateCopy = copy.deepcopy(state)
                          if j-1>=0:
                              if stateCopy[i][j-1] == ' ':
                                stateCopy[i][j-1] = value
                                stateCopy[i][j] = ' '
                                tuple = ((i,j-1),(i,j),stateCopy)
                                successors.append(tuple)
                                stateCopy = copy.deepcopy(state)
                          if i+1<5 and j+1<5:
                              if stateCopy[i+1][j+1] == ' ':
                                stateCopy[i+1][j+1] = value
                                stateCopy[i][j] = ' '
                                tuple = ((i+1,j+1),(i,j),stateCopy)
                                successors.append(tuple)
                                stateCopy = copy.deepcopy(state)
                          if i+1<5 and j-1>=0:
                              if stateCopy[i+1][j-1] == ' ':
                                  stateCopy[i+1][j-1] = value
                                  stateCopy[i][j] = ' '
                                  tuple = ((i+1,j-1),(i,j),stateCopy)
                                  successors.append(tuple)
                                  stateCopy = copy.deepcopy(state)
                          if i-1>=0 and j+1<5:
                              if stateCopy[i-1][j+1] == ' ':
                                  stateCopy[i-1][j+1] = value
                                  stateCopy[i][j] = ' '
                                  tuple = ((i-1,j+1),(i,j),stateCopy)
                                  successors.append(tuple)
                                  stateCopy = copy.deepcopy(state)
                          if i-1>=0 and j-1>=0:
                              if stateCopy[i-1][j-1] == ' ':
                                stateCopy[i-1][j-1] = value
                                stateCopy[i][j] = ' '
                                tuple = ((i-1,j-1),(i,j),stateCopy)
                                successors.append(tuple)
                                stateCopy = copy.deepcopy(state)
                          if i-1>=0 and j+1<5:
                              if stateCopy[i-1][j+1] == ' ':
                                  stateCopy[i-1][j+1] = value
                                  stateCopy[i][j] = ' '
                                  tuple = ((i-1,j+1),(i,j),stateCopy)
                                  successors.append(tuple)
                                  stateCopy = copy.deepcopy(state)
                          if i-1>=0:
                              if stateCopy[i-1][j] == ' ':
                                  stateCopy[i-1][j] = value
                                  stateCopy[i][j] = ' '
                                  tuple = ((i-1,j),(i,j),stateCopy)
                                  successors.append(tuple)
                                  stateCopy = copy.deepcopy(state)
                          if i+1<5:
                              if stateCopy[i+1][j] == ' ':
                                  stateCopy[i+1][j] = value
                                  stateCopy[i][j] = ' '
                                  tuple = ((i+1,j),(i,j),stateCopy)
                                  successors.append(tuple)
                                  stateCopy = copy.deepcopy(state)
          return successors

    def opponent_move(self, move):
        if len(move) > 1:    # validate input
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        self.place_piece(move, self.opp)   # make move

    def place_piece(self, move, piece):
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        for row in state:        # check horizontal wins
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        for col in range(5):        # check vertical wins
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        for col in range(2):        # check \ diagonal wins
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col+1] == state[i+2][col+2] == state[i+3][col+3]:
                    return 1 if state[i][col]==self.my_piece else -1

        for col in range(3,5):        # check / diagonal wins
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col-1] == state[i+2][col-2] == state[i+3][col-3]:
                    return 1 if state[i][col]==self.my_piece else -1

        for col in range(1,4):        # check diamond wins
            for i in range(0,3):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col-1] == state[i+2][col] == state[i+1][col+1] and state[i+1][col]==' ':
                    return 1 if state[i][col]==self.my_piece else -1
        return 0

    def heuristic_game_value(self,state):
        if self.game_value(state)==1 or self.game_value(state)==-1: #terminal
            return 0
        else:
            h=0
            for col in range(1,4): # three in a diamond with one open winning spot
                value = self.my_piece
                exit = False
                for i in range(0,3):
                    a = (state[i][col] == value and state[i][col] == state[i+1][col-1] == state[i+2][col] and state[i+1][col+1]==' ')
                    b = (state[i][col] == value and state[i][col] == state[i+1][col+1] == state[i+2][col] and state[i+1][col-1]==' ')
                    c = (state[i+1][col+1] == value and state[i+1][col+1] == state[i+2][col] == state[i+1][col-1] and state[i][col] == ' ')
                    d = (state[i+1][col+1] == value and state[i+1][col+1] == state[i][col] == state[i+1][col-1] and state[i+2][col] == ' ')
                    if a or b or c or d:
                        h=0.75
                        exit = True
                if(exit):
                  break
            if exit==False: # three in a diamond with one closed winning spot
                value = self.my_piece
                for col in range(1,4):
                    exit = False
                    for i in range(0,3):
                        a = (state[i][col] == value and state[i][col] == state[i+1][col-1] == state[i+2][col] and state[i+1][col+1]!=value)
                        b = (state[i][col] == value and state[i][col] == state[i+1][col+1] == state[i+2][col] and state[i+1][col-1]!=value)
                        c = (state[i+1][col+1] == value and state[i+1][col+1] == state[i+2][col] == state[i+1][col-1] and state[i][col] != value)
                        d = (state[i+1][col+1] == value and state[i+1][col+1] == state[i][col] == state[i+1][col-1] and state[i+2][col] != value)
                        if a or b or c or d:
                            h = -0.25
                            exit = True
                    if(exit):
                        break
            if exit==False: # two in a diamond with two open winning spots
                 for col in range(1,4):
                     exit = False
                     for i in range(0,3):
                         a = (state[i][col] == value and state[i][col] == state[i+1][col-1] and state[i+1][col+1]==state[i+2][col]==' ')
                         b = (state[i][col] == value and state[i][col] == state[i+1][col+1] and state[i+2][col]==state[i+1][col-1]==' ')
                         c = (state[i+1][col-1] == value and state[i+1][col-1] == state[i+2][col] and state[i][col]==state[i+1][col+1]==' ')
                         d = (state[i+1][col+1] == value and state[i+1][col+1] == state[i+2][col] and state[i][col]==state[i+1][col-1]==' ')
                         if a or b or c or d:
                             h=0.5
                             exit = True
                     if(exit):
                         break
            if exit==False: # two in a diamond with two closed winning spots
                 for col in range(1,4):
                     exit = False
                     for i in range(0,3):
                         a = (state[i][col] == value and state[i][col] == state[i+1][col-1] and state[i+1][col+1]==state[i+2][col]!=value)
                         b = (state[i][col] == value and state[i][col] == state[i+1][col+1] and state[i+2][col]==state[i+1][col-1]!=value)
                         c = (state[i+1][col-1] == value and state[i+1][col-1] == state[i+2][col] and state[i][col]==state[i+1][col+1]!=value)
                         d = (state[i+1][col+1] == value and state[i+1][col+1] == state[i+2][col] and state[i][col]==state[i+1][col-1]!=value)
                         if a or b or c or d:
                             h=-0.5
                             exit = True
                     if(exit):
                         break
            if exit==False: # horizontal or vertical two in a diamond with two open winning spots
                for col in range(1,4):
                    exit = False
                    for i in range(0,3):
                        a = (state[i][col]==value and state[i][col]==state[i+2][col] and state[i+1][col-1]==state[i+1][col+1]==' ')
                        b = (state[i][col]==' ' and state[i+1][col-1]==state[i+1][col+1]==value and state[i][col]==state[i+2][col])
                        if a or b:
                            h = 0.25
                            exit = True
                    if(exit):
                        break
            if exit==False: # horizontal or vertical two in a diamond with two closed winning spots
                value = self.my_piece
                for col in range(1,4):
                    exit = False
                    for i in range(0,3):
                        a = (state[i][col]==value and state[i][col]==state[i+2][col] and state[i+1][col-1]==state[i+1][col+1]!=' ' and state[i+1][col-1]!=value)
                        b = (state[i+1][col-1]==state[i+1][col+1]==value and state[i][col]==state[i+2][col]!=' ' and state[i][col]!=value)
                        if a or b:
                            h = -0.75
                            exit = True
                    if(exit):
                        break
            if exit==False: #three in a row horizontally with one open winning space
                value = self.my_piece
                for col in range(5):
                    exit = False
                    a = (state[0][col]==value) and (state[1][col]==value) and (state[2][col]==value) and (state[3][col]==' ')
                    b = (state[0][col]==value) and (state[1][col]==value) and (state[2][col]==' ') and (state[3][col]==value)
                    c = (state[0][col]==value) and (state[1][col]==' ') and (state[2][col]==value) and (state[3][col]==value)
                    d = (state[0][col]==' ') and (state[1][col]==value) and (state[2][col]==value) and (state[3][col]==value)
                    e = (state[1][col]==value) and (state[2][col]==value) and (state[3][col]==value) and (state[4][col]==' ')
                    f = (state[1][col]==value) and (state[2][col]==value) and (state[3][col]==' ') and (state[4][col]==value)
                    g = (state[1][col]==value) and (state[2][col]==' ') and (state[3][col]==value) and (state[4][col]==value)
                    h = (state[1][col]==' ') and (state[2][col]==value) and (state[3][col]==value) and (state[4][col]==value)
                    if a or b or c or d or e or f or g or h:
                        h = 0.75
                        exit = True
                    if(exit):
                        break
            if exit==False: #three in a row horizontally with two open winning spaces
                value = self.my_piece
                for col in range(5):
                    exit = False
                    if (state[0][col]==' ') and (state[1][col]==value) and (state[2][col]==value) and (state[3][col]==value) and (state[4][col]==' '):
                        h = 0.9
                        exit = True
                    if(exit):
                        break
            if exit==False: #three in a row vertically with one open winning space
                value = self.my_piece
                for i in range(5):
                    exit = False
                    a = (state[i][0]==value) and (state[i][1]==value) and (state[i][2]==value) and (state[i][3]==' ')
                    b = (state[i][0]==value) and (state[i][1]==value) and (state[i][2]==' ') and (state[i][3]==value)
                    c = (state[i][0]==value) and (state[i][1]==' ') and (state[i][2]==value) and (state[i][3]==value)
                    d = (state[i][0]==' ') and (state[i][1]==value) and (state[i][2]==value) and (state[i][4]==value)
                    e = (state[i][1]==value) and (state[i][2]==value) and (state[i][3]==value) and (state[i][4]==' ')
                    f = (state[i][1]==value) and (state[i][2]==value) and (state[i][3]==' ') and (state[i][4]==value)
                    g = (state[i][1]==value) and (state[i][2]==' ') and (state[i][3]==value) and (state[i][4]==value)
                    h = (state[i][1]==' ') and (state[i][2]==value) and (state[i][3]==value) and (state[i][4]==value)
                    if a or b or c or d or e or f or g or h:
                        h = 0.75
                        exit = True
                    if(exit):
                        break
            if exit==False: #three in a row vertically with two open winning spaces
                value = self.my_piece
                for i in range(5):
                    exit = False
                    if (state[i][0]==' ') and (state[i][1]==value) and (state[i][2]==value) and (state[i][3]==value) and (state[i][4]==' '):
                        h = 0.9
                        exit = True
                    if(exit):
                        break
            if exit==False: #three in a row diagonally with two open winning space
                value = self.my_piece
                a = (state[1][1]==value) and (state[2][2]==value) and (state[3][3]==value) and (state[0][0]==state[4][4]==' ')
                b = (state[1][3]==value) and (state[2][2]==value) and (state[3][1]==value) and (state[4][0]==state[0][4]==' ')
                if a or b:
                    h = 0.9
                    exit = True
            if exit==False: #three in a row diagonally with one open winning space
                value = self.my_piece
                for i in range(2):
                    exit = False
                    for col in range(2):
                        a = (state[i][col]==value) and (state[i+1][col+1]==value) and (state[i+2][col+2]==value) and (state[i+3][col+3]==' ')
                        b = (state[i][col]==value) and (state[i+1][col+1]==value) and (state[i+2][col+2]==' ') and (state[i+3][col+3]==value)
                        c = (state[i][col]==value) and (state[i+1][col+1]==' ') and (state[i+2][col+2]==value) and (state[i+3][col+3]==value)
                        d = (state[i][col]==' ') and (state[i+1][col+1]==value) and (state[i+2][col+2]==value) and (state[i+3][col+3]==value)
                        if a or b or c or d:
                            h = 0.75
                            exit = True
                    if(exit):
                        break
                for i in range(2):
                    exit = False
                    for col in range(3,5):
                        a = (state[i][col]==value) and (state[i+1][col-1]==value) and (state[i+2][col-2]==value) and (state[i+3][col-3]==' ')
                        b = (state[i][col]==value) and (state[i+1][col-1]==value) and (state[i+2][col-2]==' ') and (state[i+3][col-3]==value)
                        c = (state[i][col]==value) and (state[i+1][col-1]==' ') and (state[i+2][col-2]==value) and (state[i+3][col-3]==value)
                        d = (state[i][col]==' ') and (state[i+1][col-1]==value) and (state[i+2][col-2]==value) and (state[i+3][col-3]==value)
                        if a or b or c or d:
                            h = 0.75
                            exit = True
                    if(exit):
                        break
                for i in range(3,5):
                    exit = False
                    for col in range(2):
                        a = (state[i][col]==value) and (state[i-1][col+1]==value) and (state[i-2][col+2]==value) and (state[i-3][col+3]==' ')
                        b = (state[i][col]==value) and (state[i-1][col+1]==value) and (state[i-2][col+2]==' ') and (state[i-3][col+3]==value)
                        c = (state[i][col]==value) and (state[i-1][col+1]==' ') and (state[i-2][col+2]==value) and (state[i-3][col+3]==value)
                        d = (state[i][col]==' ') and (state[i-1][col+1]==value) and (state[i-2][col+2]==value) and (state[i-3][col+3]==value)
                        if a or b or c or d:
                            h = 0.75
                            exit = True
                    if(exit):
                        break
                for i in range(3,5):
                    exit = False
                    for col in range(3,5):
                        a = (state[i][col]==value) and (state[i-1][col-1]==value) and (state[i-2][col-2]==value) and (state[i-3][col-3]==' ')
                        b = (state[i][col]==value) and (state[i-1][col-1]==value) and (state[i-2][col-2]==' ') and (state[i-3][col-3]==value)
                        c = (state[i][col]==value) and (state[i-1][col-1]==' ') and (state[i-2][col-2]==value) and (state[i-3][col-3]==value)
                        d = (state[i][col]==' ') and (state[i-1][col-1]==value) and (state[i-2][col-2]==value) and (state[i-3][col-3]==value)
                        if a or b or c or d:
                            h = 0.75
                            exit = True
                    if(exit):
                        break
            if exit==False:
                h=0.00001
            return h

    def Max_Value(self, state, depth):
        nextMoveArr = []
        nextMove = ()
        succTuples = copy.deepcopy(self.succ(state))#list of tuples of a move associated with a successor state
        succArr = [] #a list of successors
        alpha = 0
        for i in succTuples:
            if self.dropPhase:
                nextMoveArr.append(i[0])
                succArr.append(i[1])
            else:
                tuple = (i[0],i[1])
                nextMoveArr.append(tuple)
                succArr.append(i[2])
        bestState = succArr[0]
        for i in range(len(succArr)):
            if self.heuristic_game_value(succArr[i])>self.heuristic_game_value(bestState):
                bestState = succArr[i]
                nextMove = nextMoveArr[i]
        if depth==self.maxDepth:
            return (nextMove, self.heuristic_game_value(state))
        alpha = float('-inf')
        for i in range(len(succArr)):
            alpha = max(alpha, self.Min_Value(succArr[i], depth+1)[1])
            nextMove = nextMoveArr[i]
        return (nextMove,alpha)

    def Min_Value(self, state, depth):
        nextMoveArr = []
        nextMove = ()
        succTuples = copy.deepcopy(self.succ(state))
        succArr = []
        beta = 0
        for i in succTuples:
            if self.dropPhase:
                nextMoveArr.append(i[0])
                succArr.append(i[1])
            else:
                tuple = (i[0],i[1])
                nextMoveArr.append(tuple)
                succArr.append(i[2])
        bestState = succArr[0]
        for i in range(len(succArr)):
            if self.heuristic_game_value(succArr[i])>self.heuristic_game_value(bestState):
                bestState = succArr[i]
                nextMove = nextMoveArr[i]
        if depth==self.maxDepth:
            return (nextMove, self.heuristic_game_value(state))
        beta = float('inf')
        for i in range(len(succArr)):
            beta = min(beta, self.Max_Value(succArr[i], depth+1)[1])
            nextMove = nextMoveArr[i]
        return (nextMove,beta)

    def make_move(self, state):
        count = 0
        for i in state:
            count+=i.count(' ')
        if count>17:
            self.dropPhase = True
        self.currDepth = 0
        if not self.dropPhase:
            move = []
            move.insert(0, self.Max_Value(state, 0)[0][0])
            move.insert(1, self.Max_Value(state, 0)[0][1])
            return move
        move = []
        move.insert(0, self.Max_Value(state, 0)[0]) # ensure the destination (row,col) tuple is at the beginning of the move list
        return move
