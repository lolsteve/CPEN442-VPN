import SocketServer

class handler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

class server(SocketServer.TCPServer):

    def __init__(self, server_address, handler_class=EchoRequstHandler, sharedKey):
        self.sharedKey = sharedKey
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return
