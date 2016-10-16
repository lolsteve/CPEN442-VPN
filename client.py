import sys
import socket
from DiffieHellman import DiffieHellman
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
        #wait on socket to get data
	try:
            return self.sock.recv(1024)
        except:
            self.sock.close()

    #key exchange for client
    def DH(self):

	#generate key to send to server
	myDiffieHellman = DiffieHellman()
	print 'Key sent to server: ',myDiffieHellman.public_key
	
	#send key to server
	self.send(str(myDiffieHellman.public_key))
	reply= self.waitToRec()
	print 'got client key: ', reply
	
	#calculate session key
	myDiffieHellman.calc_shared_key(long(reply))
	print "sessionKey: ", myDiffieHellman.key
	self.sessionKey = myDiffieHellman.key

    def sendMessage(self):
	#generate cipher for session
	sessionCipher = AESCipher(str(self.sessionKey))
	while True:
	    try:
		#prompt client for message
                dataCl = raw_input('Please enter a message to be sent: ')
		
		#encrypt message
		cipherText = sessionCipher.encrypt(dataCl)
		print 'The encrypted client message is: ', cipherText
		
		#send message to server
		print 'sending ciphertext'
		self.send(cipherText)
		
		#wait to hear back from server
		print 'waiting for message'
		reply = self.waitToRec()
		print 'The encrypted cipherText', reply
		
		#decrypt message gotten from server
		plainText = sessionCipher.decrypt(reply)
		print 'Server plaintext: ', plainText

	    except:
                self.close()
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

