import socket

SERVER_PORT = 9999
SERVER_FOLDER = 'server/'
CLIENT_FOLDER = 'client/'

PACKET_SIZE = 3 * 1024
CHUNK_SIZE = 2 * 1024


def local_address(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("192.168.1.1", 80))
    address = (s.getsockname()[0], port)
    s.close()
    return address
