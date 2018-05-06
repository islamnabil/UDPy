import os
from datetime import datetime
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

    def send_window(self, packets, base, client, address):
        end = base + WINDOW_SIZE
        end = end if end < len(packets) else len(packets)

        # Send Window packets
        for pkt in packets[base:end]:
            if randint(1, 100) > LOSS_PROBABILITY:
                pkt.__print__(to_address=address)
                client.send(pkt.__dump__())
            else:
                print(colored('Simulating Packet Loss: ' +
                              pkt.__get__('seq_num'), 'red'))

    # Send packet to the client & wait for positive ack
    # Returns 1 on success else 0
    def begin_transimission(self, packets, client, address):
        base = 0
        self.send_window(packets, base, client, address)

        client_timeout_count = CLIENT_TIMEOUT_TRIALS
        while client_timeout_count:
            if base >= len(packets):
                break

            end = base + WINDOW_SIZE
            end = end if end < len(packets) else len(packets)

            client.settimeout(TIME_OUT_SEC)
            try:  # Wait for response or timeout
                res = client.recv(PACKET_SIZE)
                if not res:
                    break
                pkt = Packet(res=res)
                pkt.__print__(from_address=address)
                seq_num = int(pkt.__get__('seq_num'))
                if base <= seq_num <= base + WINDOW_SIZE:
                    if pkt.__get__('ack') == '+':
                        client.settimeout(None)
                        free_slots = int(pkt.__get__('seq_num')) - base + 1
                        nEnd = end + free_slots
                        nEnd = nEnd if nEnd < len(packets) else len(packets)
                        new_pkts = packets[end:nEnd]
                        for pkt in new_pkts:
                            if randint(1, 100) > LOSS_PROBABILITY:
                                pkt.__print__(to_address=address)
                                client.send(pkt.__dump__())
                            else:
                                print(colored('Simulating Packet Loss: ' +
                                              pkt.__get__('seq_num'), 'red'))
                        base += free_slots
                else:
                    print(colored('Ack out of window, discard ' +
                                  str(seq_num) + ' => from: ' + str(address),
                                  color='blue'))
            except timeout:
                print(colored('Timeout, resending window. => to: ' +
                              str(address), color='red'))
                self.send_window(packets, base, client, address)
                client_timeout_count -= 1
        # Retrun number of timeouts
        return CLIENT_TIMEOUT_TRIALS - client_timeout_count

    # return file request packet or zero after time out
    def wait_for_request(self, client, address):
        client_timeout_count = CLIENT_TIMEOUT_TRIALS
        while client_timeout_count:
            try:
                request = client.recv(PACKET_SIZE)
                if request:
                    pkt = Packet(res=request)
                    pkt.__print__(from_address=address)
                    return pkt
                else:
                    print('Client disconnected, address:', address)
                    break
            except timeout:
                client_timeout_count -= 1
        return 0

    def serve_client(self, client, address):
        total_time = datetime.now()
        pkt = self.wait_for_request(client, address)
        if not pkt:
            return 1
        file = SERVER_FOLDER + pkt.__get__('file')
        if os.path.isfile(file):  # if file is found on the server
            pkt = Packet(status='found')
            client.send(pkt.__dump__())
            # Logic goes here
            f = open(file=file, mode='rb')
            data = f.read()
            bits = len(data) * 8
            # Build packet
            packets = [
                Packet(data=data[i: i + CHUNK_SIZE],
                       seq_num=i // CHUNK_SIZE)
                for i in range(0, len(data), CHUNK_SIZE)
            ]

            timeout_count = self.begin_transimission(
                packets=packets, client=client, address=address)

            total_time = (datetime.now() - total_time).total_seconds()

            print('Sent ' + str(bits) + ' bits, in ' +
                  str(total_time) + ' secs, with ' +
                  str(timeout_count) + ' timeouts')

            with open('GBNlog.txt', 'a') as log:
                run_metrics = DELIMITER.decode() + '\n'
                run_metrics += 'TYPE=GBN\n'
                run_metrics += 'THROUGHPUT=' + \
                    str(bits / total_time) + '\n'
                run_metrics += 'PACKET_LOSS=' + \
                    str(LOSS_PROBABILITY) + '\n'

                log.write(run_metrics)

        else:  # if file not found, send not found packet
            pkt = Packet(status='not_found')
            client.send(pkt.__dump__())

        print('Client disconnected, address: ', address)
        client.close()


if __name__ == '__main__':
    Server(port=SERVER_PORT).listen()
