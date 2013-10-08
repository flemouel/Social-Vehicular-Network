#!/usr/bin/env python
import os,subprocess,sys,shutil
from sumolib import checkBinary
import traci, random
import string,operator
import libxml2
from libxml2 import xmlAttr
from subprocess import PIPE, Popen
from fonction import intersect,communityNodeList,communitiesList,socialLink,listInfos,newRoute,listVehID,listPoIID

#mis en place :
ListNodeCommunities=communityNodeList("communities.txt")
ListCommunities=communitiesList(ListNodeCommunities)
ListEdge=socialLink("forestfire.txt")


#mise en place : simulation
PORT = 8813

	
sumoBinary = checkBinary('sumo-gui')
sumoConfig = "data/map.sumocfg"

if not traci.isEmbedded():
	
#simulation
        sumoProcess = subprocess.Popen(" %s -c  %s" % (sumoBinary,sumoConfig),shell=True, stdout=sys.stdout)
        traci.init(PORT)

#initialisation du pas de temps
step=0

#Liste des identifiants des vehicules impliques dans le scenario (certains ont une route non-valides et ne sont pas representes) : ListeVehID
 
ListVehID=listVehID("data/map.rou.xml")

#Liste des identifiants des points d'interet : ListePoIID
ListPoIID= listPoIID("data/poi.add.xml")

#Liste des vehicules possedant une info sur un point d'interet ("rate" pourcentage) : ListeInfoVehID
#Liste des infos que possedent ces vehicules : ListeInfo
rate=sys.argv[1]
ListInfos=listInfos(rate,ListPoIID,ListVehID)
ListInfoVehID=ListInfos[0]
ListInfo=ListInfos[1]

#Liste des vehicules qui communiquent
ListVehInteract=[]

#Debut de la simulation
while step == 0 or traci.simulation.getMinExpectedNumber() > 0:
    	traci.simulationStep()
	#Chaque communaute est prise en compte
	for community in ListCommunities:
		#consideration des vehicules present dans la communaute et sur la route
		List=intersect(traci.vehicle.getIDList(), community)
		for vehID2 in List:
			for vehID1 in List:

				#enregistrement de la position des vehicules
				x1=traci.vehicle.getPosition(vehID1)[0]
				y1=traci.vehicle.getPosition(vehID1)[1]
				x2=traci.vehicle.getPosition(vehID2)[0]
				y2=traci.vehicle.getPosition(vehID2)[1]

				#route ou se trouve le vehicule
				RoadVehID2=traci.vehicle.getRoadID(vehID2)

				#trajet complet du vehicule
				Route2=traci.vehicle.getRoute(vehID2)

				#cas ou deux vehicules d'une meme communaute sont proches 
				if (vehID1 in community) and (vehID2 in community) and  not((vehID2,vehID1) in ListVehInteract) and abs(x1-x2)>0 and abs(x1-x2)<20 and abs(y1-y2)<20 and RoadVehID2 in Route2:

					#enregistrement des vehicules qui interagissent pour eviter les doublons au pas de temps suivant
					ListVehInteract.append((vehID2,vehID1))

					#si un des deux vehicules possede une info 
					if vehID1 in ListInfoVehID:
						#position x y du point d'interet possedant l'info
						PoiID=ListInfo[ListInfoVehID.index(vehID1)]

						#position de la route ou se trouve le point d'interet
						PosPoiID=traci.poi.getPosition(PoiID)
						RoadPoiID=traci.simulation.convertRoad(PosPoiID[0],PosPoiID[1])

						#mis en place de la nouvelle arrivee et de la position actuelle du vehicule
						subprocess.call(['./SameArr.py',RoadVehID2,RoadPoiID[0]])
						#calcul du plus court chemin jusqu'au PoI
						subprocess.call('./generateTrips.sh', shell=True)
						#on recupere la donnee du chemin
						ListEdgeVehID=newRoute("data/newmap.rou.xml")

						#le vehicule interesse par l'info change de route et prend le point d'interet comme nouvelle destination
						if len(ListEdgeVehID)!=0:
							traci.vehicle.setRoute(vehID2, ListEdgeVehID)					
			
	step=step+1
traci.close()
sys.stdout.flush()
