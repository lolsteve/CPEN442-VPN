import click
import SocketServer
from server import server
from client import client

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
	# Message
	dataCl = click.prompt('Please enter message to be sent')

	# Send data from client to server
	clientTest = client(addressCl, portCl)
	clientTest.send(dataCl)
	clientTest.close()

def callServer():
	# Port
	portSv = click.prompt('Please enter a valid port number', type=int)
	# Address
	addressSv = click.prompt('Please enter an address; default is', default='localhost')

	tupleSv = addressSv, portSv
	serverSv = SocketServer.TCPServer(tupleSv, server)
	serverSv.serve_forever()
	

if __name__ == "__main__":
   main()
	
