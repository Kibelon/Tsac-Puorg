# Peer pyTorrent
# Jesus Gracia & Miquel Sabate
# GEI URV 2016/2017
# Version 2.1
# Last-update 15.03.17

from pyactor.context import set_context, create_host, shutdown, serve_forever, interval
from random import randint
import random
import sys

class Peer(object):
    _tell = ['get_peers', 'announce', 'set_hash', 'init', 'missatge', 'push', 'pull', 'pull_recived']
    _ask = ['request']
    _ref = ['get_peers', 'push', 'pull']

    torrent_hash = ""
    tracker=""
    neighbors=""
    data=""
    lenData=0
    type_of_peer=""
    data_left=[]
    data_recived=[]

    def init(self):
        self.tracker = host.lookup_url('http://127.0.0.1:1277/tracker', 'Tracker', 'tracker')
        self.interval1 = interval(self.host, 5, self.proxy, "announce")
        # peer will send an announce every 5 seconds to tracker
        self.interval2 = interval(self.host, 2, self.proxy, "get_peers")
        # peer will do the method get_peers every 2 seconds
        if type_of_peer == "push":
            self.interval3 = interval(self.host, 4, self.proxy, "push")
        elif type_of_peer == "pull":
            self.interval3 = interval(self.host, 4, self.proxy, "pull")
        elif type_of_peer == "pull-push":
            self.interval3 = interval(self.host, 4, self.proxy, "push")
            self.interval4 = interval(self.host, 4, self.proxy, "pull")

    def announce(self):
        self.tracker.announce(self.torrent_hash, self.proxy)

    def get_peers(self):
        self.neighbors = self.tracker.get_peers(self.torrent_hash, self.proxy)
        print "".join(data)


    def push(self):
        if self.neighbors != []:
            if data_recived != []:
                rndm = random.choice(self.neighbors)
                index = random.choice(data_recived)
                rndm.missatge(data[index], index)

    def missatge(self, msg, index):
        if (data[index] == ''):
            if (msg != ''):
                data[index] = msg
                data_left.remove(index)
                data_recived.append(index)

    def pull(self):
        if data_left != []:
            if self.neighbors != []:
                rndm = random.choice(self.neighbors)
                index = random.choice(data_left)
                future = rndm.request(index, future=True)
                future.add_callback('pull_recived')

    def pull_recived (self, future):
        result = future.result()
        data[result[1]] = result[0]
        if (data[result[1]] != ''):
            data_left.remove(result[1])
            data_recived.append(result[1])

    def request(self, index):
        return [data[index], index]


if __name__ == "__main__":
    set_context()
    rand = randint(1000, 1999)
    host = create_host('http://127.0.0.1:' + str(rand))

    print 'peer' + str(rand)

    peer = host.spawn('peer' + str(rand), Peer)

    if len(sys.argv) > 5:
        print "Error in the argument. Use: python peer.py type_of_peer torrent_hash length [seedFile]"
        shutdown()
        exit()
    if len(sys.argv) < 4:
        print "Error in the argument. Use: python peer.py type_of_peer torrent_hash length [seedFile]"
        shutdown()
        exit()
    if len(sys.argv) == 4:
        type_of_peer = str(sys.argv[1])
        torrent_hash = str(sys.argv[2])
        lenData = int(sys.argv[3])
        data = ['']*lenData
        data_left = list(range(lenData))
        data_recived = []
    if len(sys.argv) == 5:
        type_of_peer = str(sys.argv[1])
        torrent_hash = str(sys.argv[2])
        lenData = int(sys.argv[3])
        data_left = []
        data_recived = list(range(lenData))
        with open(str(sys.argv[4]), 'r') as f:
            data = list(f.read())
            #f.closed
        if len(data) != lenData:
            print "Error in length. Length should be ", lenData, " and message has a length of ", len(data)
            shutdown()
            exit()
    peer.init()

    serve_forever()
