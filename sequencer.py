# Peer pyTorrent
# Jesus Gracia & Miquel Sabate
# GEI URV 2016/2017
# Version 2.0
# Last-update 10.05.17

from pyactor.context import set_context, create_host, shutdown, serve_forever, interval
from random import randint
import random
import sys

class Sequencer(object):
    _tell = ['init']
    _ask = ['get_counter']
    _ref = []

    counter=0

    def init(self):
        self.counter=0

    def get_counter(self):
        count=self.counter
        self.counter += 1
        print count
        return count

if __name__ == "__main__":
    set_context()
    host = create_host('http://127.0.0.1:' + str(1500))
    print 'sequencer:1500'
    sequencer = host.spawn('sequencer', Sequencer)

    sequencer.init()
    serve_forever()
