#!/bin/bash

#Initialisation de la simulation : 

#genere $1 departs et arrivees aleatoirement 
./generateTrip.sh $1


#genere des departs et arrivee localises dans la carte
if [ $2 = ] ||  ([ $2 != 'y' ]  &&  [ $2 != 'n' ]) ;
then
	echo 'Il manque un argument : n : pas de depart et arrivee localises, y : depart et arrivee localises';
elif [ $2 = 'n' ];
then
	echo 'Pas de depart et arrivee localises';
elif [ $2 = 'y' ] ;
then 
	~/Documents/Sumo/sumo-0.16.0/tools/trip/randomTrips.py -n data/Depart.net.xml -o data/Depart.trips.xml -e $1;
	~/Documents/Sumo/sumo-0.16.0/tools/trip/randomTrips.py -n data/Arrivee.net.xml -o data/Arrivee.trips.xml -e $1;
	./SameDepArr.py
fi



#genere le chemin le plus court en temps hors ligne pour chaque depart et arrivee
duarouter --repair --ignore-errors -t data/map.trips.xml -n data/map.net.xml -o data/map.rou.xml


