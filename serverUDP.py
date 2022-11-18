import socket
import threading
from protocol import DataType, Protocol

class Server:
    def __init__(self,ip):
            self.ip = ip
            self.port = 55556
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.bind((self.ip, self.port))
            self.clients = {}
            self.clientCharId = {}
            threading.Thread(target=self.receive).start()

    def receive(self):   
        print('Esuchamos a nuestros Heroes en: '+str(self.ip)+':'+ str(self.port))
        while True:
            try:
                data, addr = self.s.recvfrom(1025)
                message = Protocol(datapacket=data)
                self.handle(message, addr)
            except socket.timeout:
                pass

    def handle(self, message, addr):
        if self.clients.get(addr, None) is None:
            try:
                if message.DataType != DataType.Handshake:
                    return
                name = message.data.decode(encoding='UTF-8')
                self.clients[addr] = name
                self.clientCharId[addr] = len(self.clients)
                print('{} bienvenido heroe {}!'.format(name, addr))
                ret = Protocol(dataType=DataType.Handshake, data='ok'.encode(encoding='UTF-8'))
                self.s.sendto(ret.out(), addr)
            except:
                pass
            return
        if message.DataType == DataType.ClientData:
            self.broadcast(addr, message)

    def broadcast(self, parent, data):
        data.head = self.clientCharId[parent]
        for client in self.clients:
            if client != parent:
                try:
                    self.s.sendto(data.out(), client)
                except:
                    pass

