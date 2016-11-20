import SocketServer
from spider import crawl

class CrawlNodeTCPHandler(SocketServer.BaseRequestHandler):
    """
        On recieving the hyperlink from the Master,
            Data = Runs the crawl.scrap function in the spider package
            Data = { Content, Hyperlinks, RelavanceScore }
            Sends Data back to the master.
    """
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} (MASTER): {}".format(self.client_address[0],self.data)
        Data = crawl.scrape(self.data)
        self.request.sendall(Data)

def start_slave(PORT,HOST = "localhost"):
    "Listens to master for hyperlinks to crawl"
    server = SocketServer.TCPServer((HOST, PORT), CrawlNodeTCPHandler)
    server.serve_forever()