import socket
import sys
#
# HOST = "localhost"
# PORT = 5991
# data = " ".join(sys.argv[1:])
#
# # Create a socket (SOCK_STREAM means a TCP socket)
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# try:
#     # Connect to server and send data
#     sock.connect((HOST, PORT))
#     sock.sendall(data + "\n")
#     # Receive data from the server and shut down
#     received = sock.recv(10000000)
# finally:
#     sock.close()



def send_slave_hyperlink(HYPERLINK,PORT,HOST="localhost"):
    """
        On request of the master code,
            Sends : hyperlink to slave
            Returns: Data from slave
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        sock.sendall(HYPERLINK + "\n")
        print "Sent:{}     {}".format(HOST,HYPERLINK)
        data_received = sock.recv(10000000)
        print "Received: {}".format(data_received)
    finally:
        sock.close()


def start_master():
    """
        Main master function
    """
    print("** MASTER STARTED ** \n")
