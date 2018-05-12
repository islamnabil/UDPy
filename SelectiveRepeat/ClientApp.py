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
    sequenceNumberBits = int (raw_input('sequenceNumberBits: '))
    windowSize = int (raw_input('Windows size: '))
    receiverIP = '127.0.0.1'
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
    
   
    ClientApp()
