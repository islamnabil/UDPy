import pickle
import pprint
from hashlib import sha1
from termcolor import colored


class Packet:
    def __init__(self, pickled=None, seq_num=0, data=b'',
                 ack='', file='', status=''):
        if pickled is not None:
            self.packet = pickle.loads(pickled)
        else:
            self.packet = {
                "status": status,
                "file": file,
                "ack": ack,
                "seq_num": seq_num,
                "checksum": sha1(data).hexdigest() if data else '',
                "data": data
            }

    def __dumb__(self):
        return pickle.dumps(self.packet)

    def __validate__(self):
        return self.packet['checksum'] == sha1(self.packet['data']).hexdigest()

    def __get__(self, field):
        return self.packet[field]

    def __print__(self):
        status = self.__get__('status')
        file = self.__get__('file')
        ack = self.__get__('ack')
        seq_num = str(self.__get__('seq_num'))

        if ack == '+':
            print(colored('Positive Ack ' + seq_num, color='green'))
        elif ack == '-':
            print(colored('Negative Ack ' + seq_num, color='red'))
        elif file:
            print(colored('Requesting file: ' + file, color='cyan'))
        elif status == 'found':
            print(colored('File is found, recieving', color='green'))
        elif status == 'not_found':
            print(colored('File not found', color='red'))
        else:
            print(colored('Recieved Packet ' + seq_num, color='yellow'))
        # pprint.pprint(self.packet)
