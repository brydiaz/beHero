import numpy as np
import random as r
class Game:
    def __init__(self, len_matrix):
        self.len_matrix = len_matrix
        self.board = np.zeros((len_matrix, len_matrix))
    
    def get_board(self):
        return self.board
    
    def give_empty_pos(self):
        x = r.randint(1,self.len_matrix-1)
        y = r.randint(1,self.len_matrix-1)
        if self.board[x][y] == 0:
            return (x,y)
        else:
            while self.board[x][y] == 0:
                x = r.randint(1,self.len_matrix-1)
                y = r.randint(1,self.len_matrix-1)
            return (x,y)
        
    def make_move(self, x,y):
        if self.board[x][y] != 3:
            #Aca hariamos algo si es una persona solo cambiar !=  por ==
            self.board[x][y] = 1
