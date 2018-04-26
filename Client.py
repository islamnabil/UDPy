import socket

from Packet import *

SERVER_FOLDER = 'server/'


class Client:
    def __init__(self, ip='-1', port=9999):
        if ip == '-1':
            self.ip, self.port = self.local_address(port)
        else:
            self.ip, self.port = ip, port
        self.address = (self.ip, self.port)

    def request(self, file):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect(self.address)
        print('Connected to', self.address)

        # request file
        request = Packet(request_type='GET', file=file)
        server.send(request.__dumb__())
        print('Check File: ', request)

        # response
        res = Packet(pickled=server.recv(PACKET_SIZE))
        if res.__get__('status') == 'found':
            self.recv_file(file, server)
        else:
            print("Cannot Receive: ", res.__dumb__())

    @staticmethod
    def recv_file(file_name, server):
        file = open(file=file_name, mode='ab')
        while True:
            res = Packet(pickled=server.recv(PACKET_SIZE))
            print(res.__dumb__())
            if len(res.__dumb__()) == 0:
                break
            if res.__validate__():
                file.write(res.__get__('data'))
                server.send(Packet(seq_num=res.__get__('seq_num'), ack='+').__dumb__())
            else:
                server.send(Packet(seq_num=res.__get__('seq_num'), ack='-').__dumb__())
        file.close()
        server.close()

    @staticmethod
    def local_address(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.168.1.1", 80))
        return s.getsockname()[0], port


requested_file = input("File name: ") or 'file.pdf'
client = Client()
client.request(requested_file)
