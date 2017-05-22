#! /bin/bash

gnome-terminal -e "python ../tracker.py"
#gnome-terminal -e "python sequencer.py"
gnome-terminal -e "python Monitor.py"
sleep 2
gnome-terminal -e "python ../peer.py sec grup1 t"
gnome-terminal -e "python ../peer.py sec grup1 t"
gnome-terminal -e "python ../peer.py sec grup1 t"
gnome-terminal -e "python ../peer.py sec grup1 t"
