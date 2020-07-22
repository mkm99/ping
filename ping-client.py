#! /usr/bin/env python3
# Echo Client
"""
Programming language and version: Python 3.8.1
Testing Environment:
    OS: Windows
    IDE with entrance file: N/A
    Command Lines:
        python ping-client.py 127.0.0.1 12000
"""

import sys, socket, time, struct

# Get the server hostname, port as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])

# message type (1) since it will be the request
messageType = 1

# this will be the message that will be send, it will increment by 1 in each loop
messageNumber = 1

# var to hold the packages sent
sentPackages = 0

# var to hold the packages received
receivedPackages = 0

# var to hold the rtt in each loop
rtt = 0

# var to hold min RTT
minRTT = 2

# var to hold max RTT
maxRTT = 0

# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Pinging  " + host + ", " + str(port) + ": ")

for i in range(10):
    # packing the data that will be send
    data = struct.pack('!II', messageType, messageNumber)

    # sending the data
    clientsocket.sendto(data, (host, port))

    # timestamp when data was sent
    sendingTime = time.time()

    # sleep to simulate delay in response
    time.sleep(0.000001)

    print("Ping message number " + str(messageNumber), end=" ")

    try:
        # set up how long the client has to wait for a response
        clientsocket.settimeout(1)

        # Receive the server response
        dataEcho, address = clientsocket.recvfrom(sys.getsizeof(data))

        # timestamp when client got a response
        receiveTime = time.time()

        # calculating the RTT
        rtt = float(receiveTime) - float(sendingTime)
        print("RTT:  %6f secs" % (rtt))

        # keeping track how many messages were received
        receivedPackages += 1

    except socket.timeout:
        print("timed out")

    # Increment to continue the numbering of messages to be sent
    messageNumber += 1

    # keeping track how many messages were sent
    sentPackages += 1

    # update the min RTT
    if rtt < minRTT:
        minRTT = rtt

    # update the max RTT
    if rtt > maxRTT:
        maxRTT = rtt

# Close the client socket
clientsocket.close()

'''
Statistics section
'''
# var that holds the result of the lost packages
lostPackages = sentPackages - receivedPackages

# var that holds the loss rate
lostRate = (lostPackages * 100) / sentPackages

print("\n-------------- Ping Statistics for " + str(host) + " --------------")
print("Packages: Sent = " + str(sentPackages) +
      ", Received = " + str(receivedPackages) +
      ", Lost = " + str(lostPackages) +
      " (" + str(lostRate) + "% loss)")
print("RTT: Minimum =  %6f secs" % minRTT, end="")
print(", Maximum = %6f secs" % maxRTT)
