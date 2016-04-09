import sys
import json
import random

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from listeners.twitter_listener import *

from multiprocessing import Process, Pipe

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol, \
    listenWS


class BroadcastServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        if not isBinary:
            query = json.loads(payload.decode('utf8'))
            print(query.get('query'))
            print(query.get('start'))
            print(query.get('end'))
            self.factory.search(query, self)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):

    def __init__(self, url, twitter_process):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []
        self.twitter_process = twitter_process
        self.check_for_tweets()

    def check_for_tweets(self):
        if (self.twitter_process.poll()):
            tweet = self.twitter_process.recv()

            # Use random coordinates until we can get coords from db.
            lat = random.uniform(58.1, 70.1)
            lng = random.uniform(4.6, 30.1)

            self.broadcast(json.dumps({'tweets': [{'position': {'lat': lat, 'lng': lng}, 'id': tweet.id}]}))
            print("Broadcasting %s to %d clients" % (tweet, len(self.clients)))
        # Check for new tweets every second
        reactor.callLater(1, self.check_for_tweets)


    def register(self, client):
        if client not in self.clients:
            print("Registered client %s" % (client.peer))
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print("Unregistered client %s" % (client.peer))
            self.clients.remove(client)

    def broadcast(self, msg):
        for c in self.clients:
            c.sendMessage(msg.encode('utf8'))

    def search(self, query, client):
        # The user now enters search mode, and will no longer receive live updates.
        self.unregister(client)
        # SEARCH IN DATABASE HERE BASED ON QUERY (searchString, startDate, endDate).
        # Return a maximum number to avoid overfilling the map?
        
        lat = random.uniform(58.1, 70.1)
        lng = random.uniform(4.6, 30.1)
        tweet_id = "508967802481704960"
        client.sendMessage(json.dumps({'tweets': [{'position': {'lat': lat, 'lng': lng}, 'id': tweet_id}]}).encode('utf8'))


def listen_for_tweets(child_process):
    listener = TwitterListener()
    listener.listen_to_twitter(child_process)


if __name__ == '__main__':

    log.startLogging(sys.stdout)

    ServerFactory = BroadcastServerFactory

    # Listen for tweets in a subprocess
    parent_process, child_process = Pipe()
    p = Process(target=listen_for_tweets, args=(child_process,))
    p.start()
    print("Twitter listener started as a subprocess.")

    factory = ServerFactory(u"ws://127.0.0.1:9000", parent_process)
    factory.protocol = BroadcastServerProtocol
    listenWS(factory)

    webdir = File("./src/webserver")
    web = Site(webdir)
    reactor.listenTCP(9090, web)
    reactor.run()
