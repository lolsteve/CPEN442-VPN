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
        #only 1 listener on socket
	self.sock.listen(1)
        while True:
            try:
                #get client socket
		clientsocket, address = self.sock.accept()
                #listen to recieve data
		data = clientsocket.recv(1024).strip()
                #when client is sent start Mut Auth, Key exchange
		if data[:6] == 'Client':
                    self.mutualAuth(clientsocket, data)
                    #key exchange
		    self.DH(clientsocket)
		    #exchange messages with client
                    self.talk_to_it(clientsocket)
            except:
                print 'bad'
                sys.exit(1)

    #set the key for encryption
    def setKey(self, sharedKey):
        self.sharedKey = sharedKey

    #mutual Auth
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

    #server key exchange
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

        self.sessionKey = myDH.key

    #send and recieve messages from client
    def talk_to_it(self, client):
        #establish cipher used in this session
	sessionCipher = AESCipher(str(self.sessionKey))
	while True:
            try:
		#get message from client
                cipherText = client.recv(1024).strip()
                print 'the encrypted message from the client is: ', cipherText
		#decrypt the cipherText
		plainText = sessionCipher.decrypt(cipherText)
                print 'Client message:', plainText
		#prompt server for message, encrypt and send to client
                reply = raw_input('Please enter a message to be sent')
                message = sessionCipher.encrypt(reply)
                client.send(message)
		
            except:
		client.close()
