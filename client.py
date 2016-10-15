import sys
import socket

class client(object):

	def send(self, data):

		try:
		    # Connect to server and send data
		    self.sock.sendall(data + "\n")
		
		    # Receive data from the server and shut down
		    received = self.sock.recv(1024)
		finally:
		    self.sock.close()

		print "Sent:     {}".format(data)
		print "Received: {}".format(received)

	def close(self):
		self.sock.close()


	def __init__(self, address, port):
		self.address = address, port
		
		# Create a socket (SOCK_STREAM means a TCP socket)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# Connect to server and send data
		self.sock.connect(self.address)
		

