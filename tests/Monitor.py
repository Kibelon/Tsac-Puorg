# Monitor pyTorrent
# Jesus Gracia & Miquel Sabate
# GEI URV 2016/2017
# Version 2.1
# Last-check 15.03.17

from pyactor.context import set_context, create_host, serve_forever, sleep, interval
import random

class Monitor(object):
    _tell = ['messages_in', 'check', 'init']
    _ask = []
    _ref = []

    messages = {}

    def init(self):
        sleep(10) # sleep implemented in order to avoid an check when execTime=0
        self.interval1 = interval(self.host, 10, self.proxy, "check")
        self.messages = {}
    
    def check(self):
        errors_found = False
        for peer1 in self.messages.keys():
            for peer2 in self.messages.keys():
                if peer1 != peer2:
                    for i in range(min(len(self.messages[peer1]),len(self.messages[peer2]))):
                        if self.messages[peer1][i] != self.messages[peer2][i]:
                            print 'Error!!! els peers' + str(peer1) + ' i ' + str(peer2) + ' no coincideixen en el missatge ' + str(i)
                            errors_found = True
        if errors_found == False:
            print "No errors found"
        
    def messages_in(self,msg, id):
        if not(self.messages.has_key(id)):
            self.messages[id] = []
        self.messages[id].append(msg)


if __name__ == "__main__":
    set_context()
    host = create_host('http://127.0.0.1:1278/')

    monit = host.spawn('monitor', Monitor)

    monit.init()
    serve_forever()
