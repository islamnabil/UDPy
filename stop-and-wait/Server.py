import os
from socket import timeout
from threading import Thread

from Packet import Packet
from Shared import *


class Server:
    def __init__(self, port=9999):
        self.ip, self.port = local_address(port)
        self.address = (self.ip, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.address)
        self.threads = []
        self.thread_count = 0

    def listen(self):
        self.socket.listen()
        print('[Listening on ]', self.address)
        while True:
            client, address = self.socket.accept()
            print('Client connected, address: ', address)
            client.settimeout(4)  # Client Timeout in sec

            # create new thread to serve the client
            thread = Thread(target=self.serve_client, args=(client, address))
            self.threads.append(thread)
            thread.start()
            self.thread_count += 1
            print('Thread ' + str(self.thread_count))

    def serve_client(self, client, address):
        request = client.recv(PACKET_SIZE)

        pkt = Packet(pickled=request)
        pkt.__print__()

        file = SERVER_FOLDER + pkt.__get__('file')
        if os.path.isfile(file):  # if file found on the server
            pkt = Packet(status='found')
            client.send(pkt.__dumb__())

            # Logic goes here
            seq_num = 0
            f = open(file=file, mode='rb')
            data = f.read(CHUNK_SIZE)
            while data:

                # Send Packet and block until pos ack is received
                while True:
                    pkt = Packet(data=data, seq_num=seq_num)
                    client.send(pkt.__dumb__())

                    try:  # Wait for response or timeout
                        res = client.recv(PACKET_SIZE)
                        if not res:
                            print('Client Disconnected')
                            break

                        pkt = Packet(pickled=res)
                        pkt.__print__()
                        if pkt.__get__('ack') == '+':
                            break
                        else:
                            print('Negative ack, resending : ' + str(seq_num))
                    except timeout:
                        print('Timeout, resending packet: ' + str(seq_num))

                seq_num += 1
                data = f.read(CHUNK_SIZE)

        else:  # if file not found, send not found packet
            pkt = Packet(status='not_found')
            client.send(pkt.__dumb__())

        print('Client disconnected, address: ', address)
        client.close()


if __name__ == '__main__':
    port_num = 9999
    Server(port_num).listen()
