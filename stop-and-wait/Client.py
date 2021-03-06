from Server import *
from socket import timeout
from random import randint
from termcolor import colored

from Shared import *


class Client:
    def __init__(self, ip='localhost', port=9999):
        self.ip, self.port = ip, port
        self.server_address = (self.ip, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def request(self, file):
        # Connect to server
        self.socket.connect(self.server_address)
        self.socket.settimeout(TIME_OUT_SEC)
        print('Connected to', self.server_address)

        # Send file request and wait for response
        timeout_trials = CLIENT_TIMEOUT_TRIALS
        while timeout_trials:
            # Send file request
            pkt = Packet(file=file)
            self.socket.send(pkt.__dumb__())
            try:
                res = self.socket.recv(PACKET_SIZE)
                if not res:
                    print('Disconnected from', self.server_address)
                    break

                pkt = Packet(pickled=res)
                pkt.__print__()
                if pkt.__get__('status') == 'found':
                    break
                elif pkt.__get__('status') == 'not_found':
                    print('File Not Found')
                    break
                else:
                    print('Bad response')
                    break
            except timeout:
                print('File request timeout')
                timeout_trials -= 1

        if timeout_trials:
            self.recv_file(file)

    def recv_file(self, file):
        self.socket.settimeout(None)

        received_file = CLIENT_FOLDER + file
        open(file=received_file, mode='wb').close()
        f = open(file=received_file, mode='ab')

        while True:
            try:
                res = self.socket.recv(PACKET_SIZE)
                if not res:
                    print('Disconnected from', self.server_address)
                    break

                pkt = Packet(pickled=res)
                pkt.__print__()
                # Simulating packet corruption
                if randint(1, 100) > CORRUPTION_PROBABILITY:
                    f.write(pkt.__get__('data'))
                    # Send positive ack
                    ack = Packet(seq_num=pkt.__get__('seq_num'), ack='+')
                    self.socket.send(ack.__dumb__())
                else:  # Send negative ack
                    print(
                        colored(
                            'Simulating packet corruption (Negative Ack): ' +
                            pkt.__get__('seq_num'), color='red')
                    )
                    ack = Packet(seq_num=pkt.__get__('seq_num'), ack='-')
                    self.socket.send(ack.__dumb__())
            except Exception as e:
                print(e)
                break
        f.close()
        self.socket.close()


requested_file = '1.pdf'
c = Client(ip='172.16.3.205', port=9998)
c.request(requested_file)
