import os
import argparse
import sys

from server import Sender
from server import SocketError
from server import FileNotExistError
from server import WindowSizeError


def ServerApp():
    # Arguments
    senderIP = "localhost"
    senderPort = int (raw_input("Port Number: "))
    sequenceNumberBits = int (raw_input("SequenceNumberBits : "))
    windowSize = int (raw_input("windowSize : "))
    bitError = float (raw_input("bitError: "))
    maxSegmentSize = 1500
   
   
    # Create 'Sender' object
    sender = Sender(senderIP,
                    senderPort,
                    sequenceNumberBits,
                    windowSize,
                    maxSegmentSize)

    try:
        while 1:
            
        # Create sending UDP socket
           
            sender.open(bitError)
            
            # # Send file to receiver
            print >>sys.stderr, 'SEEEEEEEEEEEEEEEEEEEEND'
            
            #********************************* you will need it
            # Close sending UDP socket

            sender.close()
            print >>sys.stderr, 'Closeeeeeeed'


    except SocketError as e:
        print("Unexpected exception in sending UDP socket!!")
        print(e)
    except FileNotExistError as e:
        print("Unexpected exception in file to be sent!!")
        print(e)
    except WindowSizeError as e:
        print("Unexpected exception in window size!!")
        print(e)
    except Exception as e:
        print("Unexpected exception!")
        print(e)
    finally:
        sender.close()


if __name__ == "__main__":
    # Run Server Application
    ServerApp()