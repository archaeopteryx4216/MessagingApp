#!/usr/bin/env python

import pickle

# This is a simple class to represent information sent to and from servers/clients
class MessageBase:
    def __init__(self,source,dest):
        self.source = source
        self.dest = dest
        self.typeID = ""
    def serialize(self):
        return pickle.dumps(self)

# This class represents information to be realyed to another client
class ClientMessage(MessageBase):
    def __init__(self,text,source,dest):
        self.text = text
        self.source = source
        self.dest = dest
        self.typeID = "client"
    def __str__(self):
        return "[{}=>{}]: {}".format(self.source,self.dest,self.text)

# This class represents information to be sent to the server
class ServerMessage(MessageBase):
    def __init__(self,cmd,args,source,dest):
        self.cmd = cmd
        self.args = args
        self.source = source
        self.dest = dest
        self.typeID = "server"
