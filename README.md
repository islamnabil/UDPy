# Computer Networks
# Reliable Data Transfer

---

## Ahmed Lotfy Siam | 4129
## Islam Nabil | 3680

---

Implementing a Reliable Data Transport Protocol with Python using different reliable data transfer techniques:
    - Go-back-N.
    - Stop and Wait.
    - Selectiverepeat.


## - Stop And Wait
Referred to as alternating bit protocol, is a method in telecommunications to send information between two connected devices. It ensures that information is not lost due to dropped packets and that packets are received in the correct order. It is the simplest automatic repeat-request (ARQ) mechanism. A stop-and-wait ARQ sender sends one frame at a time; it is a special case of the general sliding window protocol with transmit and receive window sizes equal to one and greater than one respectively. After sending each frame, the sender doesn't send any further frames until it receives an acknowledgement (ACK) signal. After receiving a valid frame, the receiver sends an ACK. If the ACK does not reach the sender before a certain time, known as the timeout, the sender sends the same frame again. The timeout countdown is reset after each frame transmission. The above behavior is a basic example of Stop-and-Wait.

- **Scenario**

    1. Client Requests file `x` from the server and blocks for response, if no response received, then it throws a timeout exception and resends the request
    2. Server receives request from client and reply with response
    3. Server sends a datagram and blocks for ack from client, or timeout

- **Packet Definition**

```python
class Packet:
    def __init__(self, pickled=None, seq_num=0,
                 data=b'', ack='', file='', status=''):

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

```

- **Sample runs**

    - Client Side Simulatin Corrupt Packets
    - ![Simulating Corrupt Packets](https://i.imgur.com/7sYzM58.png)
    - Server Side Handling timeouts and simulating packet drop
    - ![](https://i.imgur.com/86iFzkY.png)


## - Go-Back-N


- **Scenario**

    1. The Sender sents multiple data frames
    2. The receiver process keeps track of the sequence number of the next frame it expects to receive, and sends that number with every ACK it sends.
    3. The receiver will discard any frame that does not have the exact sequence number it expects (either a duplicate frame it already acknowledged, or an out-of-order frame it expects to receive later) and will resend an ACK for the last correct in-order frame.
    4. Once the sender has sent all of the frames in its window, it will detect that all of the frames since the first lost frame are outstanding, and will go back to the sequence number of the last ACK it received from the receiver process and fill its window starting with that frame and continue the process over again.

- **Packet Definition**

```python
class Packet:
    def __init__(self, res=None, seq_num=0, data=b'',
                 ack='', file='', status=''):
        self.keys = [
            "status",
            "file",
            "ack",  # 1 byte
            "seq_num",  # 8 bytes
            "checksum",  # 40 bytes
            "data"
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
```

- **Sample Runs**

    - Client receiving and simulating corrupt packets
    - ![](https://i.imgur.com/eCAHfTh.png)
    - Server Sending & Simulating NACK
    - ![](https://i.imgur.com/yyNx1UI.png)


## - Selective Repeat
 **HOW TO RUN :**
 open the terminal to run the server 
    ```
    cd SelectiveRepaet
    python ServerApp.py
    ```
 open another terminal tab for client (Client Port = 8080)
 ```
    python ClientApp.py
 ```
 **Sample Runs**
 **SERVER**
    ![](https://i.imgur.com/HGYpLfO.png)
    ![](https://i.imgur.com/DUFuNgg.png)
 **Client**
    [](https://i.imgur.com/lE2Vgxa.png)
    [](https://i.imgur.com/wtmNCT9.png)
## - Comparison

Comparing these techniques over [1, 2, 3, 4, 5, 10, 30] % PLP
![](https://i.imgur.com/g0zbuP3.png)
