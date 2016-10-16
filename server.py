import socket
import sys
from DiffieHellman import DiffieHellman
from AESCipher import AESCipher
from Crypto import Random

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
                    self.DH(clientsocket)
            except:
                print 'bad'
                sys.exit(1)

    def setKey(self, sharedKey):
        self.sharedKey = sharedKey

    def mutualAuth(self, client, message):

        # Receive request for authentication from client
        print 'msg', message
        Ra = message[-16:]
        print 'Ra', Ra

        # Create AES object with shared key
        cipher = AESCipher(self.sharedKey)

        # Server's challenge to client
        Rb = Random.new().read(16)
        print 'Rb', Rb

        # Encrypt "name","Ra","Rb" with shared key and send it
        print "encrypting cipher"
        cipherText = cipher.encrypt('Server'+Ra+Rb)
        print "sending cipher"
        print cipher.decrypt(cipherText)
        client.send(cipherText)
        print 'sent'

        # Get response from client and decrypt
        cipherText= client.recv(1024).strip()
        plainText = cipher.decrypt(cipherText)
        print 'plainText', plainText

        # Compare received Rb with sent Rb
        if plainText[-16:] != Rb :
            print 'mutual Auth failed'
            client.send('mutual auth failed')
            sys.exit(1)
        else:
            print 'SERVER: mutual auth passed'

        # Tell client we're good to go
        client.send('mutual auth passed')
        return

    def DH(self, client):
        myDH = DiffieHellman()

        print 'waiting for value from clinet'
        # Receive value from client
        publicVal = client.recv(1024).strip()
        print publicVal
        print 'sending computed dh value to client'
        # Send computed DH to client
        client.send(str(myDH.public_key))

        print 'getting session key'
        # Compute shared key
        myDH.calc_shared_key(long(publicVal)) 

        print myDH.key

        self.sessionKey = myDiffieHellman.key
