import socket
import threading




class Client():
    
    def __init__(self):
        # Choosing Nickname
        self.nickname = input("Choose your nickname: ")
        # Connecting To Server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 55559))
        self.x = 0
        self.y = 0
    
        
    # Recibimos PETICIONES del server
    def receive(self):
        while True:
            try:
                # Receive Message From Server
                # If 'NICK' Send Nickname
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('ascii'))
                else:
                    #Aqui el server nos pide que mostremos el board
                    if len(message) > 300:
                        print(message)
                    else: #Si el server no nos manda un boarda, nos manda una posicion
                        my_pos = eval(message)
                        self.x = my_pos[0]
                        self.y = my_pos[1]
            except:
                # Error
                print("An error occured!")
                self.client.close()
                break
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
        write_thread.start()
client = Client()
client.start()