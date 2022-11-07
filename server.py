import socket
import threading
import numpy as np, sys
import time
class Server:

    def __init__(self, game):
        self.game = game
        self.host = '127.0.0.1'
        self.port = 55557

        # Starting Server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        # Lists For Clients and Their Nicknames
        self.clients = []
        self.nicknames = []
        self.nicks_and_pos = []
        act_views = threading.Thread(target=self.send_views)
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
                if self.game.validate_move(future_pos):
                    client.send(str(future_pos).encode('ascii'))
                    self.game.make_move(actual_pos[0],actual_pos[1],0)
                    self.make_move(future_pos, nick)


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
            print("...esperando conexiones!")
            client, address = self.server.accept()
            print("Se ha unido {}".format(str(address)))
            # pedimos el nick
            client.send('NICK'.encode('ascii'))
            #Guardamos el nick y el cliente
            nickname = client.recv(1024).decode('ascii')
            self.nicknames.append(nickname)
            self.clients.append(client)
            #prints uno al server, y luego avisamos a todos
            print("con user name: {}".format(nickname))
            #le damos una posicion libre al azar
            pos = self.game.give_empty_pos()
            client.send(str(pos).encode('ascii'))
            self.nicks_and_pos.append([nickname, pos])
            print([nickname, pos])
            self.game.make_move(pos[0],pos[1],1)
            # Start Handling Thread For Client
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    def send_views(self):
        #Mandamos a todos el estado actual del board
        while True:
            self.broadcast(str(self.game.get_board()).encode('ascii'))
            time.sleep(1)
    
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

