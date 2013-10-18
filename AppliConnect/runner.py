#!/usr/bin/env python

import os,subprocess,sys,shutil
from sumolib import checkBinary
import traci,fonction
from fonction import initialisation,intersect,noChangeSaveTimeAndSpeed,changeSaveTimeAndSpeed,reroutage



PORT = 8813

	
sumoBinary = checkBinary('sumo-gui')
sumoConfig = "data/map.sumocfg"

if not traci.isEmbedded():
	
	#run simulation
        sumoProcess = subprocess.Popen(" %s -c  %s" % (sumoBinary,sumoConfig),shell=True, stdout=sys.stdout)
        traci.init(PORT)

#initialisation du pas de temps
step=0

#List des vehicules
ListVeh=[]

#temps de parcours de chaque lien parcouru par chaque vehicule
ListTravelTime=[]

#lien visite au pas de temps precedent par le vehicule
Visited=[]

#List des liens parcouru par chaque vehicule
ListVisited=[]

#temps pour calculer le temps de parcours de chaque lien
time=[]

#vitesse du vehicule pour calculer le tems de parcours de chaque lien
speed=[]

#List des vehicules qui interagissent
ListVehInteract=[]

#simulation
while step == 0 or traci.simulation.getMinExpectedNumber() > 0:
    	traci.simulationStep()
	for vehID in traci.vehicle.getIDList():
		if not(vehID in ListVeh):
			#initialisation des parametres
			Initialisation=initialisation(ListVeh,ListTravelTime,ListVisited,Visited,time,speed,vehID)
			Listveh=Initialisation[0]
			ListTravelTime=Initialisation[1]		
			ListVisited=Initialisation[2]	
			Visited=Initialisation[3]
			time=Initialisation[4]
			speed=Initialisation[5]

		#le vehicule ne change pas de lien
		NoChangeSaveTimeAndSpeed=noChangeSaveTimeAndSpeed(Visited,ListVeh,time,speed,vehID)
		Visited=NoChangeSaveTimeAndSpeed[0]
		time=NoChangeSaveTimeAndSpeed[1]
		speed=NoChangeSaveTimeAndSpeed[2]

		#le vehicule change de lien
		ChangeSaveTimeAndSpeed=changeSaveTimeAndSpeed(Visited,ListVeh,time,speed,ListVisited,vehID,ListTravelTime)
		Visited=ChangeSaveTimeAndSpeed[0]
		time=ChangeSaveTimeAndSpeed[1]
		speed=ChangeSaveTimeAndSpeed[2]
		ListVisited=ChangeSaveTimeAndSpeed[3]
		ListTravelTime=ChangeSaveTimeAndSpeed[4]


	for vehID2 in traci.vehicle.getIDList():
		for vehID1 in traci.vehicle.getIDList():
			Road1=traci.vehicle.getRoadID(vehID1)
			Road2=traci.vehicle.getRoadID(vehID2)
			OppositeRoad1='-'+Road1
			OppositeRoad2='-'+Road2
			if not((vehID2,vehID1) in ListVehInteract):
				x1=traci.vehicle.getPosition(vehID1)[0]
				y1=traci.vehicle.getPosition(vehID1)[1]
				x2=traci.vehicle.getPosition(vehID2)[0]
				y2=traci.vehicle.getPosition(vehID2)[1]

				#deux vehicules se croisent en sens inverse
				if abs(x1-x2)>0 and abs(x1-x2)<20 and (Road1==OppositeRoad2 or Road2==OppositeRoad1):

					#enregistrement des vehicules qui interagissent pour eviter les doublons au pas de temps suivant
					ListVehInteract.append((vehID2,vehID1))

					#chemin de chaque vehicule
					Route2=traci.vehicle.getRoute(vehID2)
					Route1=traci.vehicle.getRoute(vehID1)

					#indice de l'endroit ou ils se croisent
					Index2=Route2.index(traci.vehicle.getRoadID(vehID2))
					Index1=Route1.index(traci.vehicle.getRoadID(vehID1))

					#liens visites par le vehicule 2
					VisitedEdge2=ListVisited[ListVeh.index(vehID2)][0:len(ListVisited[ListVeh.index(vehID2)])-1]

					#le vehicule 1 possede de nouvelles informations pour se rerouter	
					reroutage(VisitedEdge2,ListTravelTime,vehID1,vehID2,ListVeh)
		
	step=step+1
traci.close()
sys.stdout.flush()
