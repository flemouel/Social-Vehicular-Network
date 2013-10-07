#!/bin/bash
#genere $1 departs et arrivees aleatoirement
./generateTrip.sh $1

#on prend le vehicule correspondant au milieu de la simulation
y=$(($1/2))
time="${y}.00"
dep="depart=\"$time\""

#genere le chemin le plus court en temps hors ligne pour chaque depart et arrivee
duarouter --repair --ignore-errors -t data/map.trips.xml -n data/map.net.xml -o data/map.rou.xml

#definie la couleur du vehicule d'urgence que l'on integre au fichier des chemins : map.rou.xml
sed -i "25a <vType id=\"public_emergency\" color=\"0,1,0\"/>" data/map.rou.xml

#definie un des vehicules comme etant le vehicule d'urgence
sed -i '/'$dep'/s//& type=\"public_emergency\" /' data/map.rou.xml

#copie du fichier pour comparer avec une circulation sans synchro des feux
cp data/map.rou.xml data/mapWO.rou.xml

#verification de la presence du vehicule d'urgence
./presenceVehEmergencyIndata.py

#fait tourner la simulation avec synchro des feux
#./runner.py

#les resultats du vehicule d'urgence obtenus en executant le fichier : ./result.sh

#pour comparer avec la simulation sans synchro : ./runnerWO.py puis pour avoir les resultats : ./resultWO.sh



