#!/bin/bash
#construit les chemins le plus court hors ligne en fonction des données de la carte et des arrivees et departs des fichiers trips.xml.
duarouter --repair --ignore-errors -t data/newmap.trips.xml -n data/map.net.xml -o data/newmap.rou.xml
