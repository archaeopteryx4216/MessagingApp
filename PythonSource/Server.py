#!/usr/bin/env python3

from Message import *
from socket import *
from select import *

class Server:
    def __init__(self,serverSocket):
        self.socket = serverSocket
        self.listenTo = [serverSocket]
        self.output = []
        self.clients = {}
        self.names = {}
        self.addresses = {}
    def runServer(self):
        try:
            while True:
                i,o,e = select(self.listenTo,self.output,[])
                for event in i:
                    if event is self.socket:
                        newSocket, address = self.socket.accept()
                        print("Connected from: ",address)
                        self.listenTo.append(newSocket)
                        self.addresses[newSocket] = address
                        gotName = False
                        while not gotName:
                            desiredName = newSocket.recv(1024).decode()
                            if desiredName not in self.clients:
                                self.clients[desiredName] = newSocket
                                self.names[newSocket] = desiredName
                                newSocket.sendall("good".encode())
                                gotName = True
                            else:
                                newSocket.sendall("bad".encode())
                        print("Assigned name " + self.names[newSocket] + " to address ",address)
                    else:
                        print("Got message from " + self.names[event])
                        newData = event.recv(1024)
                        print("newData: ",newData)
                        if newData:
                            print("New data!")
                            message = pickle.loads(newData)
                            if message.typeID == "client":
                                print("Client message: ",message)
                                if message.dest == "":
                                    sendString = pickle.dumps(message)
                                    for sock in self.clients.values():
                                        if sock is not event:
                                            sock.sendall(sendString)
                                else:
                                    if message.dest not in self.clients.keys():
                                        errMessage = ClientMessage("Error, no such user {}".format(message.dest),"Server",message.source)
                                        sendString = pickle.dumps(errMessage)
                                        event.sendall(sendString)
                                    else:
                                        sock = self.clients[message.dest]
                                        sendString = pickle.dumps(message)
                                        sock.sendall(sendString)
                            elif message.typeID == "server":
                                print("Server command: ",message.cmd)
                                txt = ""
                                if message.cmd == "\\users":
                                    for u in self.names.values():
                                        txt = txt + " | " + u
                                else:
                                    txt = "Error, no such command " + messaage.cmd
                                response = ClientMessage(txt,"Server",message.source)
                                sendStr = pickle.dumps(response)
                                self.clients[message.source].sendall(sendStr)
                        else:
                            print("Disconnected from: ", self.addresses[event])
                            del self.addresses[event]
                            n = self.names[event]
                            del self.names[event]
                            del self.clients[n]
                            event.close()
                            self.listenTo.remove(event)
        finally:
            self.socket.close()

def main():
    sock = socket(AF_INET,SOCK_STREAM)
    sock.bind(('',8881))
    sock.listen(5)
    serv = Server(sock)
    serv.runServer()

if __name__ == "__main__": main()
