#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from twisted.protocols import basic
from twisted.web.websockets import WebSocketsResource, \
WebSocketsProtocol, lookupProtocolForFactory
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.application import service, internet
from twisted.internet.protocol import Factory


class ChatProtocol(basic.LineReceiver):
    def connectionMade(self):

        self.registered = False
        self.name = ""
        self.chat_id = ""

    def dataReceived(self, msg):
        data = json.loads(msg)

        if self.registered:
            response = {
                'ServerInfo': False,
                'text': True,

                'from': self.name,
                'msg': data['msg']
            }
            self.broadcast(json.dumps(response))
        else:
            self.name = data.get('name', False)
            self.chat_id = data.get('join', False)
            if self.name and self.chat_id:
                if self.chat_id in self.factory.chats:
                    self.factory.chats[self.chat_id].append(self)
                else:
                    #TODO: Check if chat actually exists in database
                    self.factory.chats[self.chat_id] = [self]
                self.registered = True
                response = {
                    'ServerInfo': True,
                    'text': False,

                    'msg': 'Server: {0} has joined the chat'.format(self.name)
                }
                self.broadcast(json.dumps(response))
            else:
                self.transport.loseConnection()

    def connectionLost(self, reason):
        if self.registered:
            self.factory.chats[self.chat_id].remove(self)
            response = {
                'ServerInfo': True,
                'text': False,

                'msg': 'Server: {0} has left the chat'.format(self.name)
            }
            self.broadcast(json.dumps(response))


    def message(self, msg):
        self.transport.write(msg + '\n')

    def broadcast(self, msg):
        for client in self.factory.chats[self.chat_id]:
            client.message(msg)


class ChatFactory(Factory):
    protocol = ChatProtocol
    chats = {}

resource = WebSocketsResource(lookupProtocolForFactory(ChatFactory()))
root = Resource()
root.putChild("", resource)
application = service.Application("chatserver")
internet.TCPServer(1025, Site(root)).setServiceParent(application)

# twistd -n -y WSServer.py
