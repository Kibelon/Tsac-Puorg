# Peer pyTorrent
# Jesus Gracia & Miquel Sabate
# GEI URV 2016/2017
# Version 2.2
# Last-update 10.05.17

from pyactor.context import set_context, create_host, shutdown, serve_forever, interval, sleep
from random import randint
import random
import sys

class Peer(object):
    _tell = ['get_peers', 'announce', 'init', 'multicast','check_buffer','receive']
    _ask = ['get_counter']
    _ref = ['get_peers']

    group = ""
    tracker=""
    sequencer=""
    neighbors=""
    msg=""
    counter=0
    type_of_peer=""
    buffer =[]
    internal_count=0


    def init(self):
        if type_of_peer != "sequencer":
            self.tracker = host.lookup_url('http://127.0.0.1:1277/tracker', 'Tracker', 'tracker')
            self.sequencer = host.lookup_url('http://127.0.0.1:1500/peer1500', 'Peer', 'peer')
            self.announce()
            sleep(2) #wait for all peers to start
            self.get_peers()
            if type_of_peer == "sec":
                self.interval3 = interval(self.host, 2, self.proxy, "check_buffer")
                self.interval4 = interval(self.host, 4, self.proxy, "multicast")
            elif type_of_peer == "lamp":
                self.interval3 = interval(self.host, 2, self.proxy, "check_buffer")
                #self.interval4 = interval(self.host, 4, self.proxy, "pull")
        else:
            self.counter = 0

    def get_counter(self):
        count=self.counter
        self.counter += 1
        return count

    def multicast(self):
        count = self.sequencer.get_counter()
        for peer in self.neighbors:
            peer.receive ([count, msg])
        self.receive ([count, msg])

    def receive(self, msg):
        if msg[0] == self.internal_count:
            self.process_msg(msg[1])
            self.internal_count += 1
        else:
            self.buffer.append(msg)

    def check_buffer(self):
        for tup in self.buffer:
            if tup[0] == self.internal_count:
                self.process_msg(tup[1])
                self.buffer.remove(tup)
                self.internal_count += 1

    def process_msg(self,msg):
        print msg

    def announce(self):
        self.tracker.announce(self.group, self.proxy)

    def get_peers(self):
        self.neighbors = self.tracker.get_peers(self.group, self.proxy)

if __name__ == "__main__":
    set_context()
    if str(sys.argv[1]) != "sequencer":
        rand = randint(1501, 1999)
        host = create_host('http://127.0.0.1:' + str(rand))
        print 'peer' + str(rand)
        msg = 'peer' + str(rand)
        peer = host.spawn('peer' + str(rand), Peer)
    else:
        rand = 1500
        host = create_host('http://127.0.0.1:' + str(rand))
        print 'peer' + str(rand)
        msg = 'peer' + str(rand)
        peer = host.spawn('peer' + str(rand), Peer)

    if len(sys.argv) > 3:
        print "Error in the argument. Use: python peer.py type_of_peer group"
        shutdown()
        exit()
    if len(sys.argv) < 2:
        print "Error in the argument. Use: python peer.py type_of_peer group"
        shutdown()
        exit()
    if len(sys.argv) == 2:
        type_of_peer = str(sys.argv[1])
    if len(sys.argv) == 3:
        type_of_peer = str(sys.argv[1])
        group = str(sys.argv[2])
    peer.init()

    serve_forever()
