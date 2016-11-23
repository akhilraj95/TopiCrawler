import socket
import sys
from AntSystem import graph
import Queue as Q
import threading

# q.put(10)
# q.put(1)
# q.put(5)
# while not q.empty():
# 	print q.get(),

PQUEUE = Q.PriorityQueue()

#********************************************************************
#      GLOBAL SLAVE AVAILABILITY INFORMATION
#
#   Note: Use get_free_slave() to access a slaves
#         On completion call unblock slave
#********************************************************************
SLAVES_LIST = []

def init_slave(slaves):
    for i in slaves:
        i.append(0)
        SLAVES_LIST.append(i)

def block_slave(index):
    SLAVES_LIST[index][2]=1

def unblock_slave(objlist):
    for i in SLAVES_LIST:
        if(i[0]==objlist[0] and i[1]==objlist[1]):
            i[2]=0

def get_free_slave():
    for i in range(0,len(SLAVES_LIST)):
        if(SLAVES_LIST[i][2]==0):
            block_slave(i)
            return SLAVES_LIST[i];
    return []

#********************************************************************
#          UTILITY FUNCTIONS
#********************************************************************
def send_slave_hyperlink(HYPERLINK,KEYWORDS,PORT,HOST,slave):
    """
        On request of the master code,
            Sends : hyperlink to slave
            Returns: Data from slave

        usage : send_slave_hyperlink(HYPERLINK,KEYWORDS,PORT,HOST)

    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, int(PORT)))
        KEYWORDS= "_".join(KEYWORDS)
        sock.sendall(HYPERLINK +"||"+KEYWORDS+"\n")
        print "Sent:{}     {}".format(HOST,HYPERLINK)
        data_received = sock.recv(10000000)
        #print "Received: {}".format(data_received)
        if(data_received != "Invalid"):
            data_received = data_received.split("||")
            links = data_received[0].split("{}")
            score = 1
            content = ""
            try:
                score = data_received[1]
                content = data_received[2]
            except:
                print("SOCKET_ERROR(hanled): DATA NOT OVERFLOW")
            for i in links:
                PQUEUE.put((score,i))
    finally:
        sock.close()
        unblock_slave(slave)

def call_error(i = 0):
    if(i==2):
        print("""
            INITIALIZING ERROR:
                Couldn't initalize the slave info from slave_info.txt.
                The file might be opened by another process.
        """)
    if(i==1):
        print("""
    SYNTAX ERROR: arguments aren't right
        python master.py <SEEDPAGE> <KEYWORD1> <KEYWORD2> <KEYWORD3> . . .
        """)
    elif(i==0):
        print "UNIDENTIFIED ERROR: try again."


class slaveCallThread (threading.Thread):
    def __init__(self,hyperlink,keywords,port,host,slave):
        threading.Thread.__init__(self)
        self.hyperlink = hyperlink
        self.keywords = keywords
        self.port = port
        self.host = host
        self.slave = slave
    def run(self):
        print "Starting slave scrape:" + self.hyperlink
        send_slave_hyperlink(self.hyperlink,self.keywords,self.port,self.host,self.slave)
        print "Done slave scrape: " + self.hyperlink


def pQueue(G,SEEDPAGE,KEYWORDS):
    """
        Traversing the graph with PriorityQueue
            Priority = Score of the page
    """
    PQUEUE.put((1,SEEDPAGE))

    while 1:
        if not PQUEUE.empty():
            slave = get_free_slave()
            if len(slave)!=0:
                hyperlink = PQUEUE.get()
                t = slaveCallThread(hyperlink[1],KEYWORDS,slave[1],slave[0],slave)
                t.start()



#********************************************************
#           MAIN FUNCTION - MASTER
#*******************************************************
if __name__ == "__main__":
    SEEDPAGE = ""
    KEYWORDS = []
    LINKS = []
    SLAVES = []
    #---------------------------------------------------
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
    #--------------------------------------------------
    print "\nInitializing SLAVES from slave_info.txt."
    try:
        # Reading the slave information from slave_info.txt
        with open("slave_info.txt","r") as f:
            text = f.readlines()
            for line in text:
                SLAVES.append(line.split())
        f.close()
        print "Slaves  : {} ".format(SLAVES)
        init_slave(SLAVES)
    except:
        call_error(2)
        exit()
    #--------------------------------------------------
    # Setting up the Graph
    print "\nInitializing hyperlink graph."
    GRAPH = graph.init(SEEDPAGE)
    #--------------------------------------------------
    #PriorityQueue Technique
    pQueue(GRAPH,SEEDPAGE,KEYWORDS)
