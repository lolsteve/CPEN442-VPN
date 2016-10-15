import click
import SocketServer
import sys
from Crypto import Random
from server import server
from client import client
from AESCipher import AESCipher
from Crypto.Random import random
from DiffieHellman import DiffieHellman

@click.command()
@click.option('--mode', prompt=True, type=click.Choice(['server', 'client']))


def main(mode):
    click.echo('Running in %s mode.' % mode)

    if mode == 'server':
        callServer()
    else:
        callClient()

def callClient():
    # Port
    portCl = click.prompt('Please enter a valid port number', type=int)
    #portCl = 1234
    # Address
    addressCl = click.prompt('Please enter an address; default is', default='localhost')
    #addressCl = 'localhost'
       # Send data from client to server
    clientTest = client(addressCl, portCl)

    #shared key
    sharedKey = click.prompt('Please enter a shared key', type=str)
    #sharedKey = '1234'
    sharedKey = str(sharedKey)
    #mutual authen
    mutAuthClient(sharedKey, clientTest)
    #key excahnge
    #DHkeyClient(clientTest)
    #enter text

    # Message
    dataCl = click.prompt('Please enter message to be sent')

    # Send data from client to server
    #clientTest = client(addressCl, portCl)
    clientTest.send(dataCl)
    clientTest.close()

def mutAuthClient(sharedKey, clientTest):

    # Create AES object with shared key
    cipher = AESCipher(sharedKey)

    # Client's challenge to server
    Ra = Random.new().read(16)
    message= 'Client'+ Ra
    print 'msg', message
    clientTest.send(message)

    # Wait for response from server
    reply = clientTest.waitToRec()
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
        clientTest.close()
        sys.exit(1)

    # Encrypt "name","Rb" with shared key and send it
    clientTest.send(cipher.encrypt('Client'+ Rb))

    # Wait for response from server
    replyauth = clientTest.waitToRec()
    if replyauth == 'mutual auth failed':
        print 'mutual Auth failed'
        clientTest.close()
        sys.exit(1)
    else:
        print 'CLIENT: mutual auth passed'
    return

#def DHkeyClient(clientTest):
#DH = DiffieHellman()



def callServer():
    # Port
    portSv = click.prompt('Please enter a valid port number', type=int)
    #portSv = 1234
    # Address
    addressSv = click.prompt('Please enter an address; default is', default='localhost')
    #addressSv = 'localhost'

    #shared key
    sharedKey = click.prompt('Please enter a shared key', type=str)
    #sharedKey = '1234'
    sharedKey = str(sharedKey)

    serverSv = server()
    serverSv.setKey(sharedKey)
    serverSv.serve(addressSv, portSv)

if __name__ == "__main__":
   main()

