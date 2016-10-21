import click
import time
import SocketServer
import sys
import threading
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
    # Address
    addressCl = click.prompt('Please enter an address to connect to; default is', default='localhost')
    # Port
    portCl = click.prompt('Please enter a valid port number', type=int)

    # create new client
    clientTest = client(addressCl, portCl)

    #shared key
    sharedKey = click.prompt('Please enter a shared key', type=str)
    sharedKey = str(sharedKey)

    #mutual authen
    clientTest.mutAuthClient(sharedKey)
    #key excahnge
    clientTest.DH(sharedKey)

    # Message
    # creating new threads
    t1 = threading.Thread(name='clientSend', target=clientTest.sendMessage)
    t2 = threading.Thread(name='clientWait', target=clientTest.waitForMessage)

    t1.setDaemon(True)
    t2.setDaemon(True)

    t1.start()
    t2.start()
    
    while True:
    	time.sleep(1)

    t1.join()
    t2.join()

    clientTest.close()

def callServer():
    # Address
    addressSv = click.prompt('Please enter an address to listen on; default is', default='0.0.0.0')
    # Port
    portSv = click.prompt('Please enter a valid port number', type=int)

    #shared key
    sharedKey = click.prompt('Please enter a shared key', type=str)
    sharedKey = str(sharedKey)

    #create new server
    serverSv = server()
    #set mut auth key
    serverSv.setKey(sharedKey)
    serverSv.serve(addressSv, portSv)

if __name__ == "__main__":
   main()

