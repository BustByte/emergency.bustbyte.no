import sys
import json
import random

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from listeners.twitter_listener import *
from database.repository import Repository
from tweet.json_generator import Json
from processor import Processor

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
            if query.type == 'category':
                pass
            else if query.type == 'search':
                self.factory.search(query, self)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):

    def __init__(self, url, twitter_process):
        WebSocketServerFactory.__init__(self, url)
        print("Booting tweet processor...")
        self.processor = Processor()
        print("Tweet processor successfully booted")
        self.clients = []
        self.twitter_process = twitter_process
        self.check_for_tweets()

    def check_for_tweets(self):
        if (self.twitter_process.poll()):
            self.save_and_broadcast_tweet(self.twitter_process.recv())
        # Check for new tweets every second
        reactor.callLater(1, self.check_for_tweets)

    def save_and_broadcast_tweet(self, tweet):
        position_tweet = self.processor.process(tweet)
        json_tweet = Json.generate_json([position_tweet])
        self.broadcast(json.dumps({'tweets': json_tweet}))
        print("Broadcasting %s to %d clients" % (position_tweet, len(self.clients)))

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
        tweets = Repository.search(query)
        json_tweets = Json.generate_json(tweets)

        print ('Returning %s tweets on query "%s" between %s and %s.' %
            (
                len(tweets),
                query.get('query'),
                query.get('startDate'),
                query.get('endDate')
            )
        )

        client.sendMessage(json.dumps({'tweets': json_tweets}).encode('utf8'))


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
