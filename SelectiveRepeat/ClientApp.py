#!/usr/bin/python

import os
import argparse
import sys
from client import Receiver
from client import SocketError
from client import FileIOError
from client import WindowSizeError


def ClientApp():
    # Arguments
    senderIP =raw_input('Server IP: ')
    senderPort = int (raw_input('Server Port number: '))
    receiverPort = int (raw_input('Client port number: '))
    filename = raw_input('File Name: ')
    windowSize = int (raw_input('Windows size: '))
    receiverIP = '127.0.0.1'
    sequenceNumberBits = 2
    timeout = 10
    www = os.path.join(os.getcwd(), "data", "receiver")

    # Create 'Receiver' object
    receiver = Receiver(receiverIP,
                        receiverPort,senderIP,
                        senderPort,
                        sequenceNumberBits,
                        windowSize,
                        www)
    try:
        # Create receiver UDP socket
        #receiver.open()

        # # Receive file to sender
        receiver.receive(filename,
                         senderIP,
                         senderPort,
                         receiverIP,receiverPort,
                         timeout)

        # Close receiver UDP socket
        receiver.close()


    except SocketError as e:
        print("Unexpected exception in receiver UDP socket!!")
        print(e)
    except FileIOError as e:
        print("Unexpected exception in file to be received!!")
        print(e)
    except WindowSizeError as e:
        print("Unexpected exception in window size!!")
        print(e)
    except Exception as e:
        print("Unexpected exception!")
        print(e)
    finally:
        receiver.close()


if __name__ == "__main__":
    
    # # Argument parser
    # parser = argparse.ArgumentParser(description='Selective Repeat Protocol Server Application',
    #                                  prog='python \
    #                                        ServerApp.py \
    #                                        -f <filename> \
    #                                        -a <sender_ip> \
    #                                        -b <sender_port> \
    #                                        -x <receiver_ip> \
    #                                        -y <receiver_port> \
    #                                        -m <sequence_number_bits> \
    #                                        -w <window_size> \
    #                                        -t <timeout> \
    #                                        -d <www>')

    # parser.add_argument("-f", "--filename", type=str, default="index.html",
    #                     help="File to be received, default: index.html")
    # parser.add_argument("-a", "--sender_ip", type=str, default="localhost",
    #                     help="Sender IP, default: 127.0.0.1")
    # parser.add_argument("-b", "--sender_port", type=int, default=10000,
    #                     help="Sender Port, default: 8081")
    # parser.add_argument("-x", "--receiver_ip", type=str, default="127.0.0.1",
    #                     help="Receiver IP, default: 127.0.0.1")
    # parser.add_argument("-y", "--receiver_port", type=int, default=8080,
    #                     help="Receiver Port, default: 8080")
    # parser.add_argument("-m", "--sequence_number_bits", type=int, default=2,
    #                     help="Total number of bits used in sequence numbers, default: 2")
    # parser.add_argument("-w", "--window_size", type=int, default=2,
    #                     help="Window size, default: 2")
    # parser.add_argument("-t", "--timeout", type=int, default=10,
    #                     help="Timeout, default: 10")
    # parser.add_argument("-d", "--www", type=str, default=os.path.join(os.getcwd(), "data", "receiver"),
    #                     help="Destination folder for receipt, default: /<Current Working Directory>/data/receiver/")

    # # Read user inputs
    # args = vars(parser.parse_args())

    # Run Server Application
    ClientApp()
