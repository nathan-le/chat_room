import socket, select, sys
from thread import *
from utils import *


class ChatServer(object):

    def __init__(self, port):
        self.port = int(port)
        self.users = [] #list of clients on this server
        self.channels = {} #list of chat channels
        self.addr = {} #dictionary of key=addr to value=username
        self.connection_list = [] #list of users' sockets
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendToAll(self, sock, message):
        for socket in self.connection_list:
            #if the socket is not the server or the client from which the message originated
            if socket != self.socket and socket != sock:
                try:
                    socket.send(message)
                except:
                    #if the socket connection is broke, close the socket and remove it
                    socket.close()
                    self.connection_list.remove(socket)

    def start(self):
        self.socket.bind(("0.0.0.0", self.port))
        self.socket.listen(10)
        self.connection_list.append(self.socket)
        print "Chat server started on port " + str(self.port)

        while True:
            read_sockets, write_sockets, error_sockets = select.select(self.connection_list, [], [])
        
            for sock in read_sockets:
                #new connection
                if sock == self.socket:
                    sockfd, addr = self.socket.accept()
                    self.connection_list.append(sockfd)

                    self.addr[addr[1]] = sockfd.recv(RECV_BUFFER)

                    print "%s connected" % self.addr[addr[1]]
                    self.sendToAll(sockfd, "\n%s entered room\n" % self.addr[addr[1]])
                
                #incoming message from client
                else:
                    try:
                        data = sock.recv(RECV_BUFFER)
                        if data:
                            if '/create' == data[0:7]:
                                sock.send("\ncreate\n")
                            elif '/join' == data[0:5]:
                                sock.send("\njoin\n")
                            elif '/list' == data[0:5]:
                                sock.send("\nlist\n")
                            else:
                                self.sendToAll(sock, "\r" + '[' + self.addr[sock.getpeername()[1]] + '] ' + data)
                    
                    except:
                        self.sendToAll(sock, "\n%s is offline\n" % self.addr[addr[1]])
                        sock.close()
                        self.connection_list.remove(sock)
                        continue
    
        self.socket.close()

                
if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print "Please supply a server address" 
        sys.exit()
    server = ChatServer(args[1])
    server.start()
    
    

                