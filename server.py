import socket
import sys
from AESCipher import AESCipher
from Crypto.Random import random

class server(object):

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sharedKey = ''

    def serve(self, host, port):
        address = (host, port)
        self.sock.bind(address)
        self.sock.listen(1)
        while True:
            try:
                clientsocket, address = self.sock.accept()
                data = clientsocket.recv(1024).strip()
                if data[:6] == 'Client':
                    self.mutualAuth(clientsocket, data)
            except:
                print 'bad'
                sys.exit(1)

    def setKey(self, sharedKey):
        self.sharedKey = sharedKey

    def mutualAuth(self, client, message):
        print 'msg', message
        Ra = message[-16:]
        print 'Ra', Ra
        cipher = AESCipher(self.sharedKey)
        Rb = str(random.getrandbits(128))
        print 'Rb', Rb
        cipherText = cipher.encrypt('Server'+Ra+Rb)
        client.send(cipherText)

        cipherText= self.request.recv(1024).strip()

        plainText = cipher.decrypt(cipherText)
        print 'plainText', plainText
        if plainText[-16:] != Rb :
            print 'mutual Auth failed'
            client.send('mutual auth failed')
            sys.exit(1)

        client.send('mutual auth passed')
        return
