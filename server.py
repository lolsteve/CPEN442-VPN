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
            except KeyboardInterrupt:
                print 'Exiting'
                clientsocket.close()
                self.sock.close()
                sys.exit(1)
            except:
                print 'Connection closed'
                clientsocket.close()
                #sys.exit(1)

    #set the key for encryption
    def setKey(self, sharedKey):
        self.sharedKey = sharedKey

    #mutual Auth
    def mutualAuth(self, client, message):
        try:
            # Receive request for authentication from client
            print 'Received:', message.encode('hex')
            Ra = message[-16:]
            print 'Ra:', Ra.encode('hex')

            # Create AES object with shared key
            cipher = AESCipher(self.sharedKey)

            # Server's challenge to client
            Rb = Random.new().read(16)
            print 'Rb:', Rb.encode('hex')

            # Encrypt "name","Ra","Rb" with shared key and send it
            reply = 'Server'+Ra+Rb
            #print 'Encrypting reply:', reply
            cipherText = cipher.encrypt(reply)
            print 'Sending cipher:', cipherText.encode('hex')
            client.send(cipherText)

            # Get response from client and decrypt
            cipherText = client.recv(1024).strip()
            print 'Received:', cipherText.encode('hex')
            plainText = cipher.decrypt(cipherText)
            print 'Decrypted:', plainText

            # Compare received Rb with sent Rb
            if plainText[-16:] != Rb :
                print 'Different Rb received: mutual auth failed'
                client.send('mutual auth failed')
                sys.exit(1)
            else:
                print 'SERVER: mutual auth passed'

            # Tell client we're good to go
            client.send('mutual auth passed')
            return
        except:
            print 'Mutual auth failed'
            client.close()

    #server key exchange
    def DH(self, client):
        myDH = DiffieHellman()

        # Receive value from client
        publicVal = client.recv(1024).strip()
        print 'Received g^a mod p:', publicVal
        print 'Sending g^b mod p:', str(myDH.public_key)
        # Send computed DH to client
        client.send(str(myDH.public_key))

        # Compute shared key
        myDH.calc_shared_key(long(publicVal))

        print 'Calculated session key:', myDH.key

        self.sessionKey = myDH.key

    #send and recieve messages from client
    def talk_to_it(self, client):
        #establish cipher used in this session
        sessionCipher = AESCipher(str(self.sessionKey))
        while True:
            try:
                #get message from client
                print 'Waiting for reply'
                cipherText = client.recv(1024).strip()
                print 'Encrypted message received:', cipherText.encode('hex')
                #decrypt the cipherText
                plainText = sessionCipher.decrypt(cipherText)
                print 'Decrypted message:', plainText
                #prompt server for message, encrypt and send to client
                reply = raw_input('Please enter a message to be sent: ')
                message = sessionCipher.encrypt(reply)
                print 'Sending encrypted message:', message.encode('hex')
                client.send(message)
            except:
                print 'Connection closed'
                client.close()
                return
