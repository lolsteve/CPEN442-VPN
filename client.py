import sys
import socket
from AESCipher import AESCipher
from Crypto import Random

class client(object):

    def send(self, data):

        try:
            # Connect to server and send data
            self.sock.sendall(data + "\n")
        except:
            self.sock.close()


    def close(self):
        self.sock.close()

    def __init__(self, address, port):
        self.sessionKey = ""
	self.address = address, port

        # Create a socket (SOCK_STREAM means a TCP socket)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server and send data
            self.sock.connect(self.address)
        except:
            self.sock.close()


    # Wait to receive
    def waitToRec(self):
        try:
            return self.sock.recv(1024)
        except:
            self.sock.close()

    def DH(self):
	myDiffieHellman = DiffieHellman()
	self.send(myDiffieHellman.public_key)
	reply= self.waitToRec()
	print 'got client'
	self.sessionKey = myDiffieHellman.calc_shared_key(reply)
	print "sessionKey: ", self.sessionKey
	return

    def mutAuthClient(self, sharedKey):

        # Create AES object with shared key
        cipher = AESCipher(sharedKey)

        # Client's challenge to server
        Ra = Random.new().read(16)
        message= 'Client'+ Ra
        print 'msg', message
        self.send(message)

        # Wait for response from server
        reply = self.waitToRec()
        print "got a reply"

        # Decrypt response
        plainText = cipher.decrypt(reply)
        print 'plaintext', plainText

        # Obtain Ra and Rb from response
        RaTest = plainText[-32:-16]
        print 'Ra', RaTest
        Rb=plainText[-16:]
        print 'Rb', Rb

        # Compare received Ra with sent Ra
        if RaTest!= Ra:
            print 'mutual Auth failed'
            self.close()
            sys.exit(1)

        # Encrypt "name","Rb" with shared key and send it
        self.send(cipher.encrypt('Client'+ Rb))

        # Wait for response from server
        replyauth = self.waitToRec()
        if replyauth == 'mutual auth failed':
            print 'mutual Auth failed'
            self.close()
            sys.exit(1)
        else:
            print 'CLIENT: mutual auth passed'

