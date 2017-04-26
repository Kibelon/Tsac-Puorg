# Tracker pyTorrent
# Jesus Gracia & Miquel Sabate
# GEI URV 2016/2017
# Version 2.1
# Last-update 15.03.17

from pyactor.context import set_context, create_host, serve_forever, sleep, interval
import random

class Tracker(object):
    _tell = ['announce', 'update', 'init']
    _ask = ['get_peers']
    _ref = ['announce', 'get_peers']

    peers = {}

    def init(self):
        sleep(5) # sleep implemented in order to avoid an update when execTime=0
        self.interval1 = interval(self.host, 5, self.proxy, "update")

    def get_peers(self, torrent_hash, peer):
        peerResult = []
        if len(self.peers[torrent_hash].keys()) > 4:
            num = self.peers[torrent_hash].keys()
            num.remove(peer)
            peerResult = random.sample(num, 3)
        else:
            peerResult = self.peers[torrent_hash].keys()
            peerResult.remove(peer)
        return peerResult

    def announce(self, torrent_hash, peer):
        if not(self.peers.has_key(torrent_hash)):
            self.peers[torrent_hash] = {}
        self.peers[torrent_hash][peer] = 1

    def update(self):
        for swamp in self.peers.keys():
            for peer in self.peers[swamp].keys():
                if self.peers[swamp][peer] == 0:
                    del self.peers[swamp][peer]
                else:
                    self.peers[swamp][peer] = 0


if __name__ == "__main__":
    set_context()
    host = create_host('http://127.0.0.1:1277/')

    track = host.spawn('tracker', Tracker)

    track.init()
    serve_forever()
