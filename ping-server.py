#! /usr/bin/env python3
# Echo Server
"""
Programming language and version: Python 3.8.1
Testing Environment:
    OS: Windows
    IDE with entrance file: N/A
    Command Lines:
        python ping-server.py 127.0.0.1 12000
"""

import sys, socket, time, random, struct

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# type of message (2) since it will be the response
messageType = 2

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort))

# loop forever listening for incoming UDP messages
while True:
    data, address = serverSocket.recvfrom(1024)

    # unpacking the data received from the socket, format as big-endian
    received = struct.unpack('!II', data)

    # selecting the message I received from the socket
    message = received[1]

    # packing the a message to be send, format as big-endian, the type of message, and the message itself
    toSend = struct.pack('!II', messageType, message)

    # creating a random number to similuate a no response from the server side
    randomNumber = random.randint(0, 10)

    # simulating a no response from server
    if randomNumber < 4:
        print("Message with sequence number " + str(message) + " dropped")
        time.sleep(0.2)

    # responding back to the client
    else:
        print("Responding to ping request with sequence number " + str(message))

        # Echo back to client
        serverSocket.sendto(toSend, address)
