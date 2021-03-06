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
        self.sessionKey = ''
        self.address = address, port

        # Create a socket (SOCK_STREAM means a TCP socket)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server and send data
            self.sock.connect(self.address)
        except:
            self.close()


    # Wait to receive
    def waitToRec(self):
        #wait on socket to get data
        try:
            return self.sock.recv(1024)
        except:
            self.close()

    #key exchange for client
    def DH(self, sharedKey):
        print '\n############### STARTING D-H ##################'
        # Create AES object with shared key
        cipher = AESCipher(sharedKey)

        #generate key to send to server
        myDiffieHellman = DiffieHellman()
        print 'g^a mod p value is: ', myDiffieHellman.public_key

        print '\n'

        #send key to server
        sendDH = cipher.encrypt(str(myDiffieHellman.public_key))
        print 'Sending encrypted value: ', sendDH.encode('hex')
        self.send(str(sendDH))

        print '\n'

        recvDH = self.waitToRec()

        #decrypt received DH value
        reply = cipher.decrypt(recvDH)
        print 'Received encrypted value: ', recvDH.encode('hex')
        print '\n'
        print 'g^b mod p value is: ', reply
        print '\n'

        #calculate session key
        myDiffieHellman.calc_shared_key(long(reply))
        print "Calculated session key:", myDiffieHellman.key
        self.sessionKey = myDiffieHellman.key

        print '################## D-H OVER ###################\n'

    def sendMessage(self):
        #generate cipher for session
        sessionCipher = AESCipher(str(self.sessionKey))

        print 'VPN Connected'
        while True:
            try:
                #prompt client for message
                dataCl = raw_input('')

                #encrypt message
                cipherText = sessionCipher.encrypt(dataCl)

                print '\n############## NOW SENDING MESSAGE ############'
                print 'Sending encrypted message:', cipherText.encode('hex')
                print '############## MESSAGE SENT ###################\n'

                #send message to server
                self.send(cipherText)

            except:
                print 'Exiting'
                self.close()
                sys.exit(1)
                #return


    def waitForMessage(self):
        sessionCipher = AESCipher(str(self.sessionKey))
        while True:
            try:
                reply = self.sock.recv(1024).strip()

                #decrypt message gotten from server
                plainText = sessionCipher.decrypt(reply)
                print '\n$$$$$$$$$$$$$$ RECIEVING MESSAGE $$$$$$$$$$$$$$'
                print 'Encrypted message received: ', reply.encode('hex')
                print 'Decrypted message:', plainText
                print '$$$$$$$$$$$$$$ END OF MESSAGE $$$$$$$$$$$$$$$$$\n'
            except:
                print 'Connection closed'
                return

    def mutAuthClient(self, sharedKey):
        try:
            # Create AES object with shared key
            cipher = AESCipher(sharedKey)

            # Client's challenge to server
            Ra = Random.new().read(16)
            print 'Ra:', Ra.encode('hex')
            message= 'Client'+ Ra
            print 'Sending message:', message
            self.send(message)

            # Wait for response from server
            reply = self.waitToRec()
            print 'Received:', reply.encode('hex')

            # Decrypt response
            plainText = cipher.decrypt(reply)
            print 'Decrypted:', plainText

            # Obtain Ra and Rb from response
            RaTest = plainText[-32:-16]
            print 'Ra received:', RaTest.encode('hex')
            Rb=plainText[-16:]
            print 'Rb received:', Rb.encode('hex')

            # Compare received Ra with sent Ra
            if RaTest!= Ra:
                print 'Different Ra received: mutual auth failed'
                self.close()
                sys.exit(1)

            # Encrypt "name","Rb" with shared key and send it
            finalReply = 'Client' + Rb
            print 'Encrypting reply:', finalReply
            finalCipher = cipher.encrypt(finalReply)
            print 'Sending cipher:', finalCipher.encode('hex')
            self.send(finalCipher)

            # Wait for response from server
            replyauth = self.waitToRec()
            if replyauth == 'mutual auth failed':
                print 'Server denied authentication: mutual auth failed'
                self.close()
                sys.exit(1)
            else:
                print 'CLIENT: mutual auth passed'
        except:
            print 'Mutual auth failed'
            self.close()
            sys.exit(1)

