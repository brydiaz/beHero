import socket
import threading
import numpy as np, sys
import time
class Server:

    def __init__(self, game):
        self.game = game
        self.host = '127.0.0.1'
        self.port = 55559

        # Starting Server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        # Lists For Clients and Their Nicknames
        self.clients = []
        self.nicknames = []

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
                message = client.recv(1024)
                self.broadcast(message)
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
            print(pos)
            self.game.make_move(pos[0],pos[1])
            # Start Handling Thread For Client
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    def send_views(self):
        #Mandamos a todos el estado actual del board
        while True:
            self.broadcast(str(self.game.get_board()).encode('ascii'))
            time.sleep(1)