import socket
import sys

def send_slave_hyperlink(HYPERLINK,KEYWORDS,PORT,HOST):
    """
        On request of the master code,
            Sends : hyperlink to slave
            Returns: Data from slave
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        KEYWORDS= "_".join(KEYWORDS)
        sock.sendall(HYPERLINK +"||"+KEYWORDS+"\n")
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
