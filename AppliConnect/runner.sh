#!/bin/bash

#genere $1 departs et arrivees aleatoirement 
./generateTrip.sh $1

#genere le chemin le plus court en temps hors ligne pour chaque depart et arrivee
duarouter --repair --ignore-errors -t data/map.trips.xml -n data/map.net.xml -o data/map.rou.xml


