import socket


def get_local_address(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("192.168.1.1", 80))
    address = (s.getsockname()[0], port)
    s.close()
    return address


def read_args():
    args = {}
    with open("input.txt") as input:
        for line in input:
            (key, val) = line.strip().split('=')
            args[key] = val
    return args


args = read_args()
FILENAME = args['FILENAME']
SERVER_PORT = int(args['SERVER_PORT'])
SERVER_ADDRESS = args['SERVER_ADDRESS']  # get_local_address(SERVER_PORT)
LOSS_PROBABILITY = int(args['LOSS_PROBABILITY'])
CORRUPTION_PROBABILITY = int(args['CORRUPTION_PROBABILITY'])

TIME_OUT_SEC = 2
SERVER_FOLDER = 'server/'
CLIENT_FOLDER = 'client/'
CLIENT_TIMEOUT_TRIALS = 50000

PACKET_SIZE = 3 * 1024
CHUNK_SIZE = 2 * 1024
