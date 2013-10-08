#!/bin/bash
#graphe social forestfire (Measurement-calibrated graph models for social network experiments/ Sala Alessandra)
~/Documents/Snap-1.11/examples/forestfire/./forestfire -o:forestfire.txt -n:$1 -f:0.01

#recherche des communautes dans le graphe social
cp ~/Documents/Snap-1.11/examples/forestfire/forestfire.txt ~/Documents/Snap-1.11/examples/community/forestfire.txt
~/Documents/Snap-1.11/examples/community/./community -i:forestfire.txt -a:2 -o:communities.txt

#genere $1 departs et arrivees aleatoirement 
~/Documents/Sumo/sumo-0.16.0/tools/trip/randomTrips.py -n data/map.net.xml -o data/map.trips.xml -e $1

#genere le chemin le plus court en temps hors ligne pour chaque depart et arrivee
duarouter --repair --ignore-errors -t data/map.trips.xml -n data/map.net.xml -o data/map.rou.xml



