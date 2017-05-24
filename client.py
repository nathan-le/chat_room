import socket
import sys

class BasicClient(object):

    def __init__(self, name, address, port):
    	self.name = name
        self.address = address
        self.port = int(port)
        self.socket = socket.socket()
        self.socket.connect((self.address, self.port))
        self.channel = None

    def send(self, message):
        self.socket.send(str.encode(message))

    def create():

    def join():

   	def listMembers():
        

args = sys.argv
if len(args) != 4:
    print ("Please supply a name, server address, and port.")
    sys.exit()
client = BasicClient(args[1], args[2], args[3])
while True:
	msg = input()
	if msg == "join":
		client.join()
	elif msg == "create":
		client.create
	elif msg == "list":
		client.listMembers
	else:
		client.send(msg)