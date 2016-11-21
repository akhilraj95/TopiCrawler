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

def call_error(i = 0):
    if(i==1):
        print("""
    SYNTAX ERROR: arguments aren't right
        python master.py <SEEDPAGE> <KEYWORD1> <KEYWORD2> <KEYWORD3> . . .
        """)
    elif(i==0):
        print "UNIDENTIFIED ERROR: try again."

if __name__ == "__main__":
    SEEDPAGE = ""
    KEYWORDS = []
    # checking the command line arguments
    # arguments = {seed page , list [ keywords ]}
    if(len(sys.argv)<3):
        call_error(1)
        exit()
    SEEDPAGE = sys.argv[1]
    print "\nSeed page : {} ".format(SEEDPAGE)
    for i in range(2,len(sys.argv)):
        KEYWORDS.append(sys.argv[i])
    print "Keywords  : {} ".format(KEYWORDS)
