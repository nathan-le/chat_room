import socket, sys, select, string
from utils import *


class ChatClient(object):

    def __init__(self, name, address, port):
        self.name = name
        self.address = address
        self.port = int(port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)
        try:
            self.socket.connect((self.address, self.port))
        except:
            print CLIENT_CANNOT_CONNECT
            sys.exit()
        print 'Connected to host as' + self.name
        self.socket.send(self.name)
        self.prompt()

    def prompt(self):
        sys.stdout.write(CLIENT_MESSAGE_PREFIX)
        sys.stdout.flush()

    #Citation: Referenced and modified https://github.com/keyan/python-socket-chat
    def sendMessage(self):
        while True:
            try:
                socket_list = [sys.stdin, self.socket]
                read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        
                for sock in read_sockets:
                    #incoming messages
                    if sock == self.socket:
                        data = sock.recv(4096)
                        if not data:
                            print CLIENT_CANNOT_CONNECT
                            sys.exit()
                        else:
                            sys.stdout.write(data)
                            self.prompt()
                    #outgoing messages    
                    else:
                        msg = sys.stdin.readline()
                        self.socket.send(msg)
                        self.prompt()
            except KeyboardInterrupt:
                msg = SERVER_CLIENT_LEFT_CHANNEL
                self.socket.send(msg)



if __name__ == "__main__":
    args = sys.argv
    if len(args) != 4:
        print "Please supply a name, server address, and port."
        sys.exit()
    client = ChatClient(args[1], args[2], args[3])
    client.sendMessage()

