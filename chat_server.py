import socket, select, sys
from thread import *
from utils import *


class ChatServer(object):

    def __init__(self, port):
        self.port = int(port)
        self.users = {} #dictionary of key=name to value=channel
        self.channels = {} #dictionary of key=channels to value=list of username
        self.addr = {} #dictionary of key=addr to value=username
        self.connection_list = [] #list of users' sockets
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendToAll(self, sock, message, channel):
        for socket in self.connection_list:
            #if the socket is not the server or the client from which the message originated
            if socket != self.socket and socket != sock:
                name = self.addr[socket.getpeername()[1]]
                if name in channel:
                    try:
                        socket.send(message)
                    except:
                        #if the socket connection is broke, close the socket and remove it
                        socket.close()
                        self.connection_list.remove(socket)
                        channel.remove(name)


    def switch(self, user, index):
        for channel in self.channels:
            if user in self.channels[channel]:
                self.channels[channel].remove(user)
                # self.send()
        self.channels[index].append(user)

    def checkCreate(self, chname, con):
        for check in self.channels.keys():
            if chname == check:
                con.send('\n' + SERVER_CHANNEL_EXISTS.format(chname) + '\n')
                return False
        return True

    def checkJoin(self, chname, con):
        for check in self.channels.keys():
            if chname == check:
                return True
        con.send('\n' + SERVER_NO_CHANNEL_EXISTS.format(chname) + '\n')
        return False

    def removeUser(self, sock):
        try:
            channel = None

            for ch in self.channels.keys():
                if user in self.channels[ch]:
                    channel = ch
            # self.channels.pop(user, None)
            # self.channels.pop(addr, None)
            self.channels[channel].remove(user)
        except:
            return

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
                    self.users[self.addr[addr[1]]] = None
                    print "%s connected" % self.addr[addr[1]]
                    # self.sendToAll(sockfd, "\n%s entered room\n" % self.addr[addr[1]])
                
                #incoming message from client
                else:
                    try:
                        user_addr = sock.getpeername()[1]
                        name = self.addr[user_addr]
                        data = sock.recv(RECV_BUFFER)
                        if data:
                            if '/create' == data[0:7]:
                                if self.checkCreate(data[8:], sock):
                                    self.channels[data[8:]] = []
                                    self.switch(name, data[8:])
                                    self.users[name] = data[8:]
                                    self.sendToAll(sock, 
                                        '\n'+SERVER_CLIENT_JOINED_CHANNEL.format(name)+'\n', 
                                        self.channels[self.users[name]])


                            elif '/join' == data[0:5]:
                                if self.checkJoin(data[6:], sock):
                                    self.switch(name, data[6:])
                                    self.users[name] = data[6:]
                                    self.sendToAll(sock, 
                                        '\n'+SERVER_CLIENT_JOINED_CHANNEL.format(name)+'\n', 
                                        self.channels[self.users[name]])

                            elif '/list' == data[0:5]:
                                sock.send("\n%s\n" % self.channels.keys())
                            else:
                                if self.users[name]:
                                    self.sendToAll(sock, 
                                        "\r" + '[' + self.addr[user_addr] + '] ' + data, 
                                        self.channels[self.users[name]])
                                else:
                                    sock.send('\n' + SERVER_CLIENT_NOT_IN_CHANNEL + '\n')
                    
                    except:
                        self.sendToAll(sock,
                            '\n'+SERVER_CLIENT_LEFT_CHANNEL.format(name)+'\n', 
                            self.channels[self.users[name]])

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
    
    

                