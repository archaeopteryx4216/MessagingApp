#!/usr/bin/env python3
from Message import *
from socket import *
from threading import *
import pickle

class Client:
# Constructor for the class
    def __init__(self,socket):
        self.socket = socket
        self.prompt = '>>> '
        self.requestName()
        self.textInputThread = Thread(target=self.textInput)
        self.socketInputThread = Thread(target=self.socketInput)
    def startShell(self):
        print("Starting shell...")
        self.textInputThread.start()
        self.socketInputThread.daemon = True
        self.socketInputThread.start()
        self.textInputThread.join()
    def requestName(self):
        gotName = False
        while not gotName:
            desiredName = input("Please enter desired username: ")
            self.socket.sendall(desiredName.encode())
            response = self.socket.recv(1024).decode()
            if response == "good":
                gotName = True
                self.name = desiredName
            else:
                print("Sorry, that name is already in use.")
    def socketInput(self):
        try:
            while True:
                data = self.socket.recv(1024)
                message = pickle.loads(data)
                print(message)
                print(self.prompt,end="",flush=True)
        finally:
            self.socket.close()
            return
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
                        message = ServerMessage("\\users",[],self.name,"server")
                        sendString = pickle.dumps(message)
                        self.socket.sendall(sendString)
                    elif words[0] == "\\whoami":
                        print(self.name)
                    elif words[0] == "\\help":
                        print("\\help: prints this help message")
                        print("\\whoami: prints your username")
                        print("\\quit: exits the shell and closes client")
                        print("\\prompt <your text>: changes the prompt to whatever you enter for <your text>")
                        print("\\pm <name> <your text>: sends <your text> to whoever <name> is, provided they are connected to the server.")
                        print("\\users: prints a list of all users currently connected to the server")
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
    client = Client(sock)
    client.startShell()

if __name__ == "__main__": main()
