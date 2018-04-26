import pickle
from hashlib import sha1

CHUNK_SIZE = 2 * 1024
PACKET_SIZE = 4 * 1024


class Packet:
    def __init__(self, pickled=None, seq_num=0, data=b'', ack='', request_type='', file='', status=''):
        if pickled is not None and len(pickled) > 0:
                self.packet = pickle.loads(pickled)
        else:
            self.packet = {
                "status": status,
                "file": file,
                "request_type": request_type,
                "ack": ack,
                "seq_num": str(seq_num),
                "checksum": sha1(data).hexdigest().encode(),
                "data": data
                # "size": len(data)
            }

    def __dumb__(self):
        return pickle.dumps(self.packet)

    def __validate__(self):
        return self.packet['checksum'] == sha1(self.packet['data']).hexdigest().encode()

    def __get__(self, field):
        return self.packet[field]
