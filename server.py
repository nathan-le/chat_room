import socket
import sys

class BasicServer(object):

    def __init__(self, port):
        self.address = 'localhost'
        self.port = int(port)
        self.socket = socket.socket()
        self.channels = {}

    def receive(self):
        self.socket.bind((self.address, self.port))
        self.socket.listen(5)
        while True:
        	c, addr = self.socket.accept()
        	print ('Got connection from', addr)
        	if c.recv(1024) == "create":
        		self.createChannel()
        	elif c.recv(1024) == "join":
        		self.addClient()
        	elif c.recv(1024) == "list":
        		print(self.channel)
        	else:
        		print(c.recv(1024))

    def createChannel():

   	def addClient():

   	def listClient():
        


args = sys.argv
if len(args) != 2:
    print ("Please supply a server address")
    sys.exit()
client = BasicServer(args[1])
client.receive()