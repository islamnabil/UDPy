import os
import socket
import time
from threading import Thread

from Packet import *

SERVER_FOLDER = 'server/'


class Server:
    def __init__(self, port=9999):
        self.ip, self.port = self.local_address(port)
        self.address = (self.ip, self.port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.address)
        self.thread_count = 0

    def listen(self):
        self.sock.listen()
        print('[Listening on ]', self.address)
        while True:
            connection, address = self.sock.accept()
            print('Got Connection', connection, address)
            connection.settimeout(10)
            thread = Thread(target=self.serve_client, args=(connection, address))
            thread.start()
            self.thread_count += 1
            print('Thread ' + str(self.thread_count))

    @staticmethod
    def local_address(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.168.1.1", 80))
        return s.getsockname()[0], port

    @staticmethod
    def serve_client(connection, address):
        request = Packet(pickled=connection.recv(PACKET_SIZE))
        print('Request File: ', request.__dumb__())

        file = SERVER_FOLDER + request.__get__('file')
        if os.path.isfile(file):
            print('Sending file to', address)
            pkt = Packet(status='found')
            connection.send(pkt.__dumb__())

            seq_num = 0
            f = open(file, 'rb')
            while True:
                data = f.read(CHUNK_SIZE)
                if len(data) == 0:
                    f.close()
                    break
                pkt = Packet(seq_num=seq_num, data=data)
                connection.send(pkt.__dumb__())
                seq_num += 1
        else:
            pkt = Packet(status='not_found')
            connection.send(pkt.__dumb__())
        time.sleep(1)
        connection.close()


if __name__ == "__main__":
    port_num = 9999
    # while True:
    # port_num = input("Port? ")
    # try:
    #     port_num = int(port_num)
    #     break
    # except ValueError:
    #     pass
    Server(port_num).listen()
