import click
import SocketServer
import sys
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
    # Address
    addressCl = click.prompt('Please enter an address; default is', default='localhost')
       # Send data from client to server
    clientTest = client(addressCl, portCl)

    #shared key
    sharedKey = click.prompt('Please enter a shared key')
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
    cipher = AESCipher(sharedKey)
    Ra = str(random.getrandbits(128))
    message= 'Client'+ Ra
    print 'msg', message
    clientTest.send(message)
    reply = clientTest.waitToRec()
    plainText = cipher.decrypt(reply)
    print 'plaintext', plainText
    RaTest = plainText[-32:-16]
    print 'Ra', RaTest
    Rb=plainText[-16:]
    print 'Rb', Rb
    if RaTest!= Ra:
        print 'mutual Auth failed'
        clientTest.close()
        sys.exit(1)
    clientTest.send(cipher.encrypt('Client'+ Rb))
    replyauth = clientTest.waitToRec()
    if replyauth == 'mutual auth failed':
        print 'mutual Auth failed'
        clientTest.close()
        sys.exit(1)
    return

#def DHkeyClient(clientTest):
#DH = DiffieHellman()



def callServer():
    # Port
    portSv = click.prompt('Please enter a valid port number', type=int)
    # Address
    addressSv = click.prompt('Please enter an address; default is', default='localhost')

    #shared key
    sharedKey = click.prompt('Please enter a shared key')

    serverSv = server()
    serverSv.setKey(sharedKey)
    serverSv.serve(addressSv, portSv)

if __name__ == "__main__":
   main()

