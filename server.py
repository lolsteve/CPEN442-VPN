import SocketServer
from AESCipher import AESCipher
from Crypto.Random import random

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
        if self.data[:6] == 'Client' :
            mutualAuth()
        
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())
            
    def __init__(self, request, client_address, server, sharedKey):
    
        self.sharedKey = sharedKey
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        return
  
    def mutualAuth(self):
        Ra = self.data[:-16]
        cipher = AESCipher(self.sharedKey)
        Rb = random.getrandbits(128)
        cipherText = cipher.encrypt('Server'+Ra+Rb)
        self.request.sendall(cipherText)
        
        cipherText= self.request.recv(1024).strip()

        plainText = cipher.decrypt(cipherText)
        if plainText[-16:] != Rb :
            print 'mutual Auth failed'
            self.request.sendall('mutual auth failed')
            sys.exit(1)

        self.request.sendall('mutual auth passed')
        return


class server(SocketServer.TCPServer):

    def __init__(self, server_address, handler_class=EchoRequstHandler, sharedKey):
        self.sharedKey = sharedKey
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return
