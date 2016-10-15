import sys
import socket

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



        

