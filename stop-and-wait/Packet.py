import pickle
import pprint
from hashlib import sha1
# from termcolor import colored


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
        pprint.pprint(self.packet)
