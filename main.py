import click

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
	message = click.prompt('Please enter message to be sent')

def callServer():
	# Port
	portSv = click.prompt('Please enter a valid port number', type=int)
	# Address
	addressSv = click.prompt('Please enter an address; default is', default='localhost')
	

if __name__ == "__main__":
   main()
	
