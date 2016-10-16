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
    clientTest.mutAuthClient(sharedKey)
    #key excahnge
    #DHkeyClient(clientTest)
    clientTest.DH()
    #enter text

    # Message
    sessionCipher = AESCipher(str(clientTest.sessionKey))
    while True:
        try:
            dataCl = click.prompt('Please enter message to be sent', type=str)
            dataCl = str(dataCl)
            print dataCl
            cipherText = sessionCipher.encrypt(dataCl)
            print 'sending cipher', cipherText
            clientTest.send(cipherText)
            reply = clientTest.waitToRec()
            plainText = sessionCipher.decrypt(reply)
            print 'Server', plainText
        except KeyboardInterrupt:
            pass
        except:
            clientTest.close()
            return


    # Send data from client to server
    #clientTest = client(addressCl, portCl)
    clientTest.close()

def callServer():
    # Port
    portSv = click.prompt('Please enter a valid port number', type=int)
    #portSv = 1234
    # Address
    addressSv = click.prompt('Please enter an address; default is', default='0.0.0.0')
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

