from hashlib import sha1
from termcolor import colored

from Shared import *


class Packet:
    def __init__(self, res=None, seq_num=0, data=b'',
                 ack='', file='', status=''):
        self.keys = [
            "status",
            "file",
            "ack",  # 1 byte
            "seq_num",  # 8 bytes
            "checksum",  # 40 bytes
            "data"  # 1900 bytes
        ]
        if res is not None:
            self.packet = self.__load__(res)
        else:
            self.packet = {
                "status": status.encode(),
                "file": file.encode(),
                "ack": ack.encode(),  # 1 byte
                "seq_num": int(seq_num).to_bytes(8, byteorder='little',
                                                 signed=True),  # 8 bytes
                "checksum": sha1(data).hexdigest().encode(),  # 40 bytes
                "data": data if data else b'',  # 1939 bytes
            }

        dummy_bytes = 2000
        for val in self.packet.values():
            dummy_bytes -= len(val)
        self.packet['dummy'] = b'x' * dummy_bytes

    def __dump__(self):
        return DELIMITER.join(self.packet.values())

    def __load__(self, res):
        packet = {}
        values = res.split(DELIMITER)
        for key, val in zip(self.keys, values):
            packet[key] = val
        return packet

    def __validate__(self):
        return self.packet['checksum'] == sha1(
            self.packet['data']).hexdigest().encode()

    def __get__(self, field):
        if field == 'seq_num':
            return str(int.from_bytes((self.packet[field]),
                                      byteorder='little',
                                      signed=True))
        elif field == 'data':
            return self.packet[field]
        else:
            return self.packet[field].decode()

    def __print__(self, from_address='', to_address=''):
        from_address = str(from_address)
        to_address = str(to_address)

        status = self.__get__('status')
        file = self.__get__('file')
        ack = self.__get__('ack')
        seq_num = self.__get__('seq_num')

        if ack == '+':
            print(colored('Positive Ack ' + seq_num +
                          (' => from ' + from_address if from_address else ''),
                          color='green'))
        elif ack == '-':
            print(colored('Negative Ack ' + seq_num +
                          (' => from ' + from_address if from_address else ''),
                          color='red'))
        elif file:
            print(colored('Requesting file: ' + file,
                          color='cyan'))
        elif status == 'found':
            print(colored('File is found, recieving from server',
                          color='green'))
        elif status == 'not_found':
            print(colored('File not found',
                          color='red'))
        else:
            print(colored('Packet ' + seq_num +
                          (' => to ' + to_address if to_address else ''),
                          color='yellow'))
