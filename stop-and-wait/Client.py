from Server import *
from socket import timeout
from random import randint
from Shared import CLIENT_TIMEOUT_TRIALS


class Client:
    def __init__(self, ip='localhost', port=9999):
        self.ip, self.port = ip, port
        self.server_address = (self.ip, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def request(self, file):
        # Connect to server
        self.socket.connect(self.server_address)
        self.socket.settimeout(4)
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
        received_file = CLIENT_FOLDER + file
        open(file=received_file, mode='wb').close()
        f = open(file=received_file, mode='ab')

        timeout_trials = CLIENT_TIMEOUT_TRIALS
        while timeout_trials:
            res = self.socket.recv(PACKET_SIZE)
            if not res:
                print('Disconnected from', self.server_address)
                break

            pkt = Packet(pickled=res)
            pkt.__print__()
            # Check for corruption
            if pkt.__validate__() and randint(1, 100) > CORRUPTION_PROBABILITY:
                f.write(pkt.__get__('data'))
                # Send positive ack
                ack = Packet(seq_num=pkt.__get__('seq_num'), ack='+')
                self.socket.send(ack.__dumb__())
            else:  # Send negative ack
                ack = Packet(seq_num=pkt.__get__('seq_num'), ack='-')
                self.socket.send(ack.__dumb__())
        f.close()
        self.socket.close()


requested_file = input('File name: ') or 'text.txt'
c = Client(port=SERVER_PORT)
c.request(requested_file)
