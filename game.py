import numpy as np
import random as r

class Game:
    def __init__(self, len_matrix):
        self.len_matrix = len_matrix
        self.enemys_number = int((len_matrix*len_matrix)*0.30)
        self.board = np.zeros((len_matrix, len_matrix))
        self.generate_enemys()
    
    def get_board(self): #Retorna el tablero 
        return self.board
    
    def give_empty_pos(self): #Da una posicion aleatoria disponible en el mapa
        x = r.randint(0,self.len_matrix-1)
        y = r.randint(0,self.len_matrix-1)
        if self.board[x][y] == 0:
            return (x,y)
        else:
            while self.board[x][y] == 0:
                x = r.randint(0,self.len_matrix-1)
                y = r.randint(0,self.len_matrix-1)
            return (x,y)
        
    def make_move(self, x,y,mark):
        self.board[x][y] = mark #Hace el movimiento

    def validate_move(self, move):
        if move == -1:
            return (False, False)#No es valido, alguien no digito una tecla valida
        x = move[0]
        y = move[1]
        if -1 < x < self.len_matrix and -1 < y < self.len_matrix :
            #aca validariamos el punto, por el momento solo hice si es un movimiento valido
            if self.board[x][y] == 2:
                return (True,True) #Si el movimiento es valido y hay una persona, se salva
            else: 
                return (True, False)#Si el movimiento es valido y NO hay una persona, NO se salva
        else:
            return (False, False)#No es valido
    
    def create_enemys(self):
        enemys = []
        i = 0
        while i != self.enemys_number:
            x = r.randint(1,self.len_matrix-1)
            y = r.randint(1,self.len_matrix-1)
            if (x,y) not in enemys:
                enemys.append((x,y))
                i += 1
        return enemys
    
    def generate_enemys(self):
        enemys = self.create_enemys()
        for i in enemys:
            self.make_move(i[0], i[1], 2)




