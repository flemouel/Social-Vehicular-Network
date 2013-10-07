#!/usr/bin/env python

#simulation avec reroutage des vehicules a chaque pas de temps

import os,subprocess,sys,shutil
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', "tools")) # tutorial in tests
sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(os.path.dirname(__file__), "..", "..", "..")), "tools")) # tutorial in docs
from sumolib import checkBinary
import traci

PORT = 8813

	
sumoBinary = checkBinary('sumo-gui')
sumoConfig = "data/map.sumocfg"

if not traci.isEmbedded():
	
	#run simulation
        sumoProcess = subprocess.Popen(" %s -c %s" % (sumoBinary,sumoConfig),shell=True, stdout=sys.stdout)
        traci.init(PORT)

#pas de temps
step=0

#Liste des vehicules
ListevehID=[]

#Liste des routes empruntees par les vehicules
ListeCurrentRoad=[]

#repere pour savoir si le vehicule a ete reroute
Done=[]

#debut de la simulation
while step == 0 or traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

    #changement du poids de chaque lien de la carte en fonction de la longueur du lien et de la vitesse moyenne des vehicules presents dessus
    for edge in traci.edge.getIDList():
	traci.edge.adaptTraveltime(edge,traci.edge.getTraveltime(edge))

    #reroutage global des vehicules en fonction des nouveaux poids des liens de la carte, reroutage a chaque fois que le vehicule change de lien 
    for vehID in traci.vehicle.getIDList():
	if not(vehID in ListevehID):
		ListevehID.append(vehID)
		ListeCurrentRoad.append([])
		Done.append([])
	CurrentRoad=traci.vehicle.getRoadID(vehID)
	if CurrentRoad in traci.vehicle.getRoute(vehID):
		ListeCurrentRoad[ListevehID.index(vehID)].append(CurrentRoad)
		l=len(ListeCurrentRoad[ListevehID.index(vehID)])
		
		#le vehicule change de lien
		if l>3 and ListeCurrentRoad[ListevehID.index(vehID)][l-1]!=ListeCurrentRoad[ListevehID.index(vehID)][l-3] and Done[ListevehID.index(vehID)]!='ok':
        		traci.vehicle.rerouteTraveltime(vehID)
			Done[ListevehID.index(vehID)]='ok'

		#le vehicule ne change pas de lien
		if l>2 and ListeCurrentRoad[ListevehID.index(vehID)][l-1]==ListeCurrentRoad[ListevehID.index(vehID)][l-2]:
			Done[ListevehID.index(vehID)]='ini'
    
    step=step+1
traci.close()
sys.stdout.flush()







