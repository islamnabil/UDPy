import os
from socket import timeout
from threading import Thread
from random import randint
from termcolor import colored

from Packet import Packet
from Shared import *


class Server:
    def __init__(self, ip='localhost', port=9999):
        self.ip, self.port = ip, port
        self.address = (self.ip, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.address)
        self.threads = []
        self.thread_count = 0

    def listen(self):
        self.socket.listen()
        print('[Listening on ]', self.address)
        while True:
            try:
                client, address = self.socket.accept()
                print('Client connected, address: ', address)
                client.settimeout(TIME_OUT_SEC)  # Client Timeout in sec
                # create new thread to serve the client
                thread = Thread(target=self.serve_client,
                                args=(client, address))
                self.threads.append(thread)
                thread.start()
                self.thread_count += 1
                print('Client No: ' + str(self.thread_count))
            except KeyboardInterrupt:
                print('\nServer Terminated, waiting for all threads to join')
                break

    # Send packet to the client & wait for positive ack
    # Returns 1 on success else 0
    def send_packet(self, packet, client):
        seq_num = packet.__get__('seq_num')
        client_timeout_count = CLIENT_TIMEOUT_TRIALS
        while client_timeout_count:
            if randint(1, 100) > LOSS_PROBABILITY:
                client.send(packet.__dumb__())
            else:
                print(colored('Simulating Packet Loss: ' + seq_num, 'red'))
            try:  # Wait for response or timeout
                res = client.recv(PACKET_SIZE)
                if not res:
                    print('Client Disconnected')
                    return 0
                pkt = Packet(pickled=res)
                pkt.__print__()
                if pkt.__get__('ack') == '+':
                    return 1
                else:
                    print(colored('Negative ack, resending : ' + seq_num,
                                  color='red'))
            except timeout:
                print(colored('Timeout, resending packet: ' + seq_num,
                              color='red'))
                client_timeout_count -= 1
        return 0

    # return file request packet or zero after time out
    def wait_for_request(self, client, address):
        client_timeout_count = CLIENT_TIMEOUT_TRIALS
        while client_timeout_count:
            try:
                request = client.recv(PACKET_SIZE)
                if request:
                    pkt = Packet(pickled=request)
                    pkt.__print__()
                    return pkt
                else:
                    print('Client disconnected, address:', address)
                    break
            except timeout:
                client_timeout_count -= 1
        return 0

    def serve_client(self, client, address):
        pkt = self.wait_for_request(client, address)
        if not pkt:
            return 1
        file = SERVER_FOLDER + pkt.__get__('file')
        if os.path.isfile(file):  # if file is found on the server
            pkt = Packet(status='found')
            client.send(pkt.__dumb__())
            # Logic goes here
            seq_num = 0
            f = open(file=file, mode='rb')
            data = f.read(CHUNK_SIZE)
            while data:
                # Build packet
                pkt = Packet(data=data, seq_num=seq_num)
                # Send and check for success
                if not self.send_packet(pkt, client):
                    break
                seq_num += 1
                data = f.read(CHUNK_SIZE)
        else:  # if file not found, send not found packet
            pkt = Packet(status='not_found')
            client.send(pkt.__dumb__())

        print('Client disconnected, address: ', address)
        client.close()


if __name__ == '__main__':
    Server(port=SERVER_PORT).listen()
