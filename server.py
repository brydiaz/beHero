import socket
import threading
import numpy as np, sys
import time
import help_funcs as hf
class Server:

    def __init__(self, game):
        self.game = game
        self.host = '127.0.0.1'
        self.port = 55555
        self.quamtum = 0.3

        # Starting Server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        # Lists For Clients and Their Nicknames
        self.clients = []
        self.nicknames = []
        self.nicks_and_pos = []
        self.nick_and_score = {}

        act_views = threading.Thread(target=self.act_game)
        act_views.start()

    # enviamos a todos
    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    # manejamos peticiones de los clientes
    def handle(self, client):
        while True:
            try:
                # Aca recibimos el movimiento y actualizamos
                message = client.recv(1024).decode('ascii')
                move = message[len(message)-1] #La peticion luce asi "bryan a" -1 obtenemos "a"
                nick = message[:len(message)-2]# y [:-2] obtenemos "bryan"
                actual_pos = self.actual_pos(nick)
                future_pos = self.calculate_future_pos(move, actual_pos)
                validation = self.game.validate_move(future_pos)
                if validation[0]:
                    self.game.make_move(actual_pos[0],actual_pos[1],0)
                    self.make_move(future_pos, nick)
                    if validation[1]:
                        old = self.nick_and_score[nick] 
                        self.nick_and_score[nick] = old + 1 
                        string_to_send = 'MYPOS'+str(self.nick_and_score[nick])
                        client.send(string_to_send.encode('ascii'))
            except:
                # Removing And Closing Clients
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast('{} left!'.format(nickname).encode('ascii'))
                self.nicknames.remove(nickname)
                break

    # Lo que haremos cada vez que haya un nuevo cliente
    def receive(self):
        while True:
            # Aceptamos conexion
            client, address = self.server.accept()
            # pedimos el nick
            client.send('NICK'.encode('ascii'))
            #Guardamos el nick y el cliente
            nickname = client.recv(1024).decode('ascii')
            self.nicknames.append(nickname)
            self.clients.append(client)
            #prints uno al server, y luego avisamos a todos
            #le damos una posicion libre al azar
            pos = self.game.give_empty_pos()
            client.send(str(pos).encode('ascii'))
            self.nicks_and_pos.append([nickname, pos])
            print([nickname, pos])
            self.game.make_move(pos[0],pos[1],1)
            self.nick_and_score[nickname] = 0
            # Start Handling Thread For Client
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    def act_game(self):
        #Mandamos a todos el estado actual del board
        control = True
        while control:
            enemys = self.check_enemys_in_board() #Validamos enemigos
            self.print_server_status()
            self.broadcast((str(self.game.get_board())+str(enemys)).encode('ascii')) #Enviamos el estado del board y sus enemigos
            time.sleep(self.quamtum) #Nos dormimos, aca mediamos la sincronizacion
            if enemys == 0:
                control = False
            hf.clear() #Limpiamos pantalla
        self.end_game()
        
    
    def actual_pos(self, nick):
        for i in self.nicks_and_pos:
            if i[0] == nick:
                return i[1]
    
    def calculate_future_pos(self, move, actual):
        if move == "a":
            return (actual[0], actual[1]-1)
        elif move == "s":
            return (actual[0]+1, actual[1])
        elif move == "w":
            return (actual[0]-1, actual[1])  
        elif move == "d":
            return (actual[0], actual[1]+1) 
        else:
            return -1
    
    def make_move(self, move, nick):
        
        for i in self.nicks_and_pos:
            if i[0] == nick:
                i[1] = move
        self.game.make_move(move[0],move[1],1)

    def check_enemys_in_board(self):
        enemys = 0
        for i in self.game.get_board():
            for j in i:
                if j == 2:
                    enemys += 1

        return enemys

    
    def print_server_status(self):
        print('--------------------------------------------------------')
        print('BIENVENIDOS A beHERO HOY TENEMOS '+str(self.check_enemys_in_board())+ ' PERSONAS POR SALVAR')
        print(self.game.get_board())
        print('NUESTROS HEROES JUGANDO!:')
        for i in self.nicknames:
            print('--'+i+' PERSONAS SALVADAS: '+str(self.nick_and_score[i])+'--')
    
    def end_game(self):
        
        print("SE HA ACABADO HEROES!!")
        print("TODAS LAS PERSONAS HAN SIDO SALVADAS!!")
        print("Y EL MEJOR HEROE HA SIDO....!")

        print('-----------------------------------------')
        print(max(self.nick_and_score, key=self.nick_and_score.get))
        print('-----------------------------------------')
        print('GRACIAS POR JUGAR!')

        for i in self.clients:
            i.close()
        self.server.close()
        exit()
