# Peer pyTorrent
# Jesus Gracia & Miquel Sabate
# GEI URV 2016/2017
# Version 2.3
# Last-update 17.05.17

from pyactor.context import set_context, create_host, shutdown, serve_forever, interval, sleep
from random import randint
import random
import sys
from pyactor.exceptions import TimeoutError

class Peer(object):
    _tell = ['get_peers', 'announce', 'init', 'multicast','check_buffer','receive','fight_for_power',
    'lider_chosen', 'lider_proposal', 'lider_aceptance', 'sendLamp', 'recLamp', 'check_bufferLamp', 'ack']
    _ask = ['get_counter']
    _ref = ['get_peers','lider_chosen', 'lider_proposal']

    group = ""
    tracker=""
    sequencer=""
    neighbors=""
    msg=""
    counter=0
    type_of_peer=""
    buffer =[]
    internal_count=0
    my_number=0 #used for the bully algorithm
    victory_count=0
    im_sequencer = False

    def init(self, num):
        if type_of_peer != "sequencer":
            self.counter = 0
            self.my_number = num
            self.internal_count = 0
            self.victory_count = 0
            self.im_sequencer = False
            self.tracker = host.lookup_url('http://127.0.0.1:1277/tracker', 'Tracker', 'tracker')
            self.sequencer = ""
            #self.sequencer = host.lookup_url('http://127.0.0.1:1500/peer1500', 'Peer', 'peer')
            self.announce()
            sleep(2) #wait for all peers to start
            self.get_peers()
            if type_of_peer == "sec":
                self.interval3 = interval(self.host, 2, self.proxy, "check_buffer")
                self.interval4 = interval(self.host, 4, self.proxy, "multicast")
            elif type_of_peer == "lamp":
                self.interval3 = interval(self.host, 2, self.proxy, "check_bufferLamp")
                self.interval4 = interval(self.host, 5+randint(5,10), self.proxy, "sendLamp")
        else:
            self.counter = 0

    def get_counter(self):
        count=self.counter
        self.counter += 1
        return count

    def lider_chosen(self, lider):
        if self.sequencer != "":
            self.neighbors.remove(self.sequencer)
        self.sequencer = lider
        self.proposed_lider = ""
        self.counter = 0
        self.internal_count = 0
        self.buffer =[]
        print "we have anew lider!"
        self.interval4 = interval(self.host, 4, self.proxy, "multicast") #restarting messages

    def lider_aceptance(self, result):
        print "lider opnion recived"
        if result == True:
            self.victory_count += 1
            if self.victory_count == len(self.neighbors):
                print "I'm the king!!!"
                for peer in self.neighbors:
                    peer.lider_chosen(self.proxy)
                self.lider_chosen(self.proxy)
                self.im_sequencer = True
        else:
            print "I've lost, retreet!"

    def lider_proposal(self, lider, value):
        print "lider opnion recived"
        if value <= self.my_number:
            lider.lider_aceptance(True)
        else:
            lider.lider_aceptance(False)

    def fight_for_power(self):
        im_strongest = True
        print "showing off my power: "
        for peer in self.neighbors:
            peer.lider_proposal(self.proxy ,self.my_number)


    def multicast(self):
        if self.sequencer != "":
            if self.im_sequencer == True:
                count = self.get_counter()
                for peer in self.neighbors:
                    peer.receive ([count, msg])
                self.receive ([count, msg])
            else:
                try:
                    count = self.sequencer.get_counter()
                except TimeoutError, e:
                    print "error! Starting lider election!!"
                    self.interval4.set()#stops interval so is not called while deciding new lider
                    self.fight_for_power()
                for peer in self.neighbors:
                    peer.receive ([count, msg])
                self.receive ([count, msg])
        else:
            print "No sequencer! Starting lider election!!"
            self.interval4.set() #stops interval so is not called while deciding new lider
            self.fight_for_power()


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

    def check_bufferLamp(self):
        if len(self.buffer) > 0:
            if min(self.buffer)[1] == len(self.neighbors):
                self.process_msg(min(self.buffer)[0][1])
                self.buffer.remove(min(self.buffer))
            print min(self.buffer)

    def ack(self, msg_ack):
        print msg_ack
        for tup in self.buffer:
            if (tup[0][0] == msg_ack[0] and tup[0][2] == msg_ack[1]):
                tup[1] += 1
                print "ACK"
                break

    def sendLamp(self):
        for peer in self.neighbors:
            peer.recLamp([self.counter, msg, self.my_number])
        self.recLamp([self.counter, msg, self.my_number])
        #self.counter += 1

    def recLamp(self, data):
        if data[0] > self.counter:
            self.counter = data[0]
        elif data[0] == self.counter:
            self.counter += 1
        for peer in self.neighbors:
            peer.ack([data[0], data[2]])
        self.buffer.append([data, 0])

    def process_msg(self,msg):
        print msg

    def announce(self):
        self.tracker.announce(self.group, self.proxy)

    def get_peers(self):
        self.neighbors = self.tracker.get_peers(self.group, self.proxy)

if __name__ == "__main__":
    set_context()
    rand=0
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
    peer.init(rand)

    serve_forever()
