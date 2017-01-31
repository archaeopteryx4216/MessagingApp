#!/usr/bin/env python
from Message import *
from socket import *
from threading import *
import pickle

def textInput(client):
    while True:
        text = input(client.prompt)
        if len(text) != 0:
            if text[0] != "\\":
                message = ClientMessage(text,client.name,"")
                sendString = pickle.dumps(message)
                client.socket.sendall(sendString)
            else:
                words = text.split(" ")
                if words[0] == "\\pm":
                    message = ClientMessage(" ".join(words[2:]),client.name,words[1])
                    sendString = pickle.dumps(message)
                    client.socket.sendall(sendString)
                elif words[0] == "\\quit":
                    client.socket.close()
                    return
                elif words[0] == "\\prompt":
                    client.prompt = " ".join(words[1:]) + " "
                elif words[0] == "\\users":
                    message = ServerMessage("\\users",[],client.name,"server")
                    sendString = pickle.dumps(message)
                    client.socket.sendall(sendString)
                elif words[0] == "\\whoami":
                    print(client.name)
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

def socketInput(client):
    try:
        while True:
            data = client.socket.recv(1024)
            message = pickle.loads(data)
            print(message)
            print(client.prompt,end="",flush=True)
    finally:
        client.socket.close()
        return

class Client:
# Constructor for the class
    def __init__(self,socket):
        self.socket = socket
        self.prompt = '>>> '
        self.requestName()
        self.textInputThread = Thread(target=textInput,args=(self,))
        self.socketInputThread = Thread(target=socketInput,args=(self,))
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

def main():
    sock = socket(AF_INET,SOCK_STREAM)
    sock.connect(('73.242.73.117',8881))
    client = Client(sock)
    client.startShell()

if __name__ == "__main__": main()
