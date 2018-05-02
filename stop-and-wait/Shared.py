import socket

SERVER_PORT = 9999
SERVER_LOCAL_ADDRESS = 'localhost'  # local_address(SERVER_PORT)
SERVER_FOLDER = 'server/'

CLIENT_FOLDER = 'client/'
CLIENT_TIMEOUT_TRIALS = 3

LOSS_PROBABILITY = 0.5
PACKET_SIZE = 3 * 1024
CHUNK_SIZE = 2 * 1024


def local_address(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("192.168.1.1", 80))
    address = (s.getsockname()[0], port)
    s.close()
    return address
