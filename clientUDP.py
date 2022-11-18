import socket
import threading
import pyaudio
from protocol import DataType, Protocol

class Client:
    def __init__(self, name, ip):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bufferSize = 4096
        self.connected = False
        self.name = name

        self.target_ip = ip
        self.target_port = 55556
        self.server = (self.target_ip, self.target_port)
        self.connectToServer()
     

        chunk_size = 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)

        # start threads
        receive_thread = threading.Thread(target=self.receive_server_data).start()
        sender = threading.Thread(target=self.send_data_to_server).start()


    def receive_server_data(self):
        while self.connected:
            try:
                data, addr = self.s.recvfrom(1025)
                message = Protocol(datapacket=data)
                if message.DataType == DataType.ClientData:
                    self.playing_stream.write(message.data)
            except:
                pass

    def connectToServer(self):
        if self.connected:
            return True

        message = Protocol(dataType=DataType.Handshake, data=self.name.encode(encoding='UTF-8'))
        self.s.sendto(message.out(), self.server)

        data, addr = self.s.recvfrom(1025)
        datapack = Protocol(datapacket=data)

        if (addr==self.server and datapack.DataType==DataType.Handshake and 
        datapack.data.decode('UTF-8')=='ok'):
            print('Connected to server successfully!')
            self.connected = True
        return self.connected

    def send_data_to_server(self):
        while self.connected:
            try:
                data = self.recording_stream.read(512)
                message = Protocol(dataType=DataType.ClientData, data=data)
                self.s.sendto(message.out(), self.server)
            except:
                pass

