#!/usr/bin/env python3

from Client import *
import sys

class Admin(Client):
    def __init__(self,sock):
        super().__init__(sock)
        self.password = input("Please enter server's password: ")
        self.verify(self.password)
    def verify(self,password):
        ver = ServerMessage("\\passwd",[self.password],self.name,"server")
        sendString = pickle.dumps(ver)
        self.socket.sendall(sendString)
        retString = self.socket.recv(1024)
        retMessage = pickle.loads(retString)
        print(retMessage)
        print(self.prompt,end="",flush=True)
        if retMessage.text == "fail":
            self.socket.close()
            sys.exit()
    def textInput(self):
        while True:
            text = input(self.prompt)
            if len(text) != 0:
                if text[0] != "\\":
                    message = ClientMessage(text,self.name,"")
                    sendString = pickle.dumps(message)
                    self.socket.sendall(sendString)
                else:
                    words = text.split(" ")
                    if words[0] == "\\pm":
                        message = ClientMessage(" ".join(words[2:]),self.name,words[1])
                        sendString = pickle.dumps(message)
                        self.socket.sendall(sendString)
                    elif words[0] == "\\quit":
                        self.socket.close()
                        return
                    elif words[0] == "\\prompt":
                        self.prompt = " ".join(words[1:]) + " "
                    elif words[0] == "\\users":
                        message = ServerMessage("\\users",[],self.name,"Server")
                        sendString = pickle.dumps(message)
                        self.socket.sendall(sendString)
                    elif words[0] == "\\whoami":
                        print(self.name)
                    elif words[0] == "\\kick":
                        message = ServerMessage("\\kick",[words[1]],self.name,"Server")
                        sendString = pickle.dumps(message)
                        self.socket.sendall(sendString)
                    elif words[0] == "\\kill":
                        message = ServerMessage("\\kill",[],self.name,"Server")
                        sendString = pickle.dumps(message)
                        self.socket.sendall(sendString)
                        pass
                    elif words[0] == "\\help":
                        print("\\help: prints this help message")
                        print("\\whoami: prints your username")
                        print("\\quit: exits the shell and closes client")
                        print("\\prompt <your text>: changes the prompt to whatever you enter for <your text>")
                        print("\\pm <name> <your text>: sends <your text> to whoever <name> is, provided they are connected to the server.")
                        print("\\users: prints a list of all users currently connected to the server")
                        print("\\kick <usernam>: removes username from the server if they are connected")
                        print("\\kill: shuts down the server cleanly")
                        print("If no command is given, then all text is broadcast to all users")
                    else:
                        print("Error, unrecognized command {}".format(words[0]))

def main():
    config = open("Config.txt")
    hostname = "null"
    port = 0
    for line in config:
        if line[0] == '#':
            continue
        words = line.split('=')
        if words[0] == 'hostname':
            hostname = words[1].rstrip()
        elif words[0] == 'port':
            port = int(words[1].rstrip())
    if hostname == "null":
        hostname = input("Please enter hostname/ip-address: ")
    if port == 0:
        port = int(input("Please enter port number: "))
    sock = socket(AF_INET,SOCK_STREAM)
    sock.connect((hostname,port))
    admin = Admin(sock)
    admin.startShell()

if __name__ == "__main__": main()
