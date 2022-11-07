import socket
import threading
import help_funcs as hf
from pynput import keyboard


class Client():
    
    def __init__(self):
        # Choosing Nickname
        self.nickname = input("Choose your nickname: ")
        # Connecting To Server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 55555))
        self.score = 0



    
        
    # Recibimos PETICIONES del server
    def receive(self):
        while True:

            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = self.client.recv(1024).decode('ascii')
            if message == 'NICK':
                self.client.send(self.nickname.encode('ascii'))
            else:
                #Aqui el server nos pide que mostremos el board
                if len(message) > 300:
                    hf.clear()
                    print(message[:len(message)-2])
                    print('\n')
                    enemys = message[len(message)-2:]
                    print('Personas restantes por salvar:'+enemys)
                    print('Personas salvadas por '+self.nickname+' '+str(self.score))
                else: #Si el server no nos manda un boarda, nos manda una posicion
                    if message[:5] == 'MYPOS':
                        self.score = int(message[5:])



        # Enviamos mensajes
    def write(self):
        while True:
            message = '{}: {}'.format(self.nickname, input(''))
            self.client.send(message.encode('ascii'))

    def start(self):
        # Starting Threads For Listening And Writing
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)

        #Lee los movimientos
        move_thread = threading.Thread(target=self.read_move)
        move_thread.start()

    def make_move(self, key):
        try:
            key = key.char
            self.client.send((self.nickname+','+key).encode('ascii'))
        except AttributeError:
            pass

    def read_move(self):
        with keyboard.Listener(
            on_press=self.make_move) as listener:
            listener.join()
            
                


client = Client()
client.start()