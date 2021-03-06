#!/usr/bin/env python



import os,subprocess,sys,shutil
from sumolib import checkBinary
import traci, libxml2, random
from libxml2 import xmlAttr
from CreateListe import number, createListe, coordinateJunction, edgeInJunction, edgeOutJunction
from ProgramTrafficLights import initialisation, presenceVehEmergency, vehInJunction, changeTrafficLightState, vehNearVehEmergency1, vehNearVehEmergency2, updateTrafficlights




PORT = 8813

	
sumoBinary = checkBinary('sumo-gui')
sumoConfig = "data/map.sumocfg"

if not traci.isEmbedded():
	
	#run simulation
        sumoProcess = subprocess.Popen(" %s -c  %s" % (sumoBinary,sumoConfig),shell=True, stdout=sys.stdout)
        traci.init(PORT)
 
#Creation des Listes de donnees utiles de la carte
CoordXJunction=createListe("data/map.net.xml")[0] 
CoordYJunction=createListe("data/map.net.xml")[1] 
TypeJunction=createListe("data/map.net.xml")[2] 
IdJunction=createListe("data/map.net.xml")[3]
IdEdge=createListe("data/map.net.xml")[4]
EdgeInJunction=createListe("data/map.net.xml")[5] 
EdgeFromJunction=createListe("data/map.net.xml")[6]


#Nombre de vehicule dans la simulation

print 'le nombre de vehicule est de : ' +  str(number("data/map.rou.xml"))


#construction de la liste des coordonnees des intersections

CoordJunctionList=coordinateJunction(CoordXJunction,CoordYJunction)

#construction de la liste des liens entrant sur chaque intersection

EdgeInJunction=edgeInJunction(EdgeInJunction)

#construction des routes sortant pour chaque intersection

EdgeOutJunction=edgeOutJunction(IdJunction,EdgeFromJunction,IdEdge)

#pas de temps

step=0

#premiere presence du vehicule d'urgence sur le reseau

check=''

#fin de la presence du vehicule d'urgence sur le reseau

finish=''

#initialisation des listes :

ProgramTrafficlights=initialisation(CoordJunctionList)
ListeVehIDJunc=initialisation(CoordJunctionList)

#permet de savoir si un feu a ete change apres passage d'un vehicule d'urgence
Initialize=initialisation(CoordJunctionList)

#permet de garder le feu modifie le temps du passage du vehicule d'urgence
Done=initialisation(CoordJunctionList)


#debut de la simulation

while step == 0 or traci.simulation.getMinExpectedNumber() > 0:
   	traci.simulationStep()
	k=0
	if finish=='ok':
		step=step+1

	if finish!='ok':
		#enregistrement des parametres du vehicule d'urgence
		ParameterVehEmergency=presenceVehEmergency(check)
		coordxVehEmergency=ParameterVehEmergency[1]
		coordyVehEmergency=ParameterVehEmergency[2]
		RoutevehEmergency=ParameterVehEmergency[4]
		LastRoadVehEmergency=ParameterVehEmergency[5]
		Last2RoadVehEmergency=ParameterVehEmergency[6]
		vehIdEmergency=ParameterVehEmergency[3]
		check=ParameterVehEmergency[0]
		
		#fin du parcours du vehicule d'urgence
		if check=='ok' and (traci.vehicle.getRoadID(vehIdEmergency)==LastRoadVehEmergency or traci.vehicle.getRoadID(vehIdEmergency)==Last2RoadVehEmergency):
			finish='ok'

		#pour chaque intersection
		for CoordJunction in CoordJunctionList:
        		index=CoordJunctionList.index(CoordJunction)
			coordXJunction=float(CoordJunction[0])
			coordYJunction=float(CoordJunction[1])
			
			#le vehicule d'urgence est proche de l'intersection (30 metres de rayon)
			if (coordxVehEmergency>=coordXJunction-30) and (coordxVehEmergency<=coordXJunction+30) and (coordyVehEmergency>=coordYJunction-30) and (coordyVehEmergency<=coordYJunction+30) and (traci.vehicle.getRoadID(vehIdEmergency) in EdgeInJunction[index]):
				ListeVehIDJunc=vehInJunction(index,ListeVehIDJunc,coordXJunction,coordYJunction,EdgeInJunction,IdJunction)
					
				#changement du feu
				if TypeJunction[index]=='traffic_light' and Done[index]!='1':
					ChangeTrafficLightState=changeTrafficLightState(vehIdEmergency,IdJunction,index,Done,Initialize,ProgramTrafficlights)
					Done=ChangeTrafficLightState[0]
					Initialize=ChangeTrafficLightState[1]
					IdTrafficLights=ChangeTrafficLightState[2]
					ProgramTrafficlights=ChangeTrafficLightState[3]
					#changement du comportement des vehicules
					vehNearVehEmergency1(ListeVehIDJunc,index,vehIdEmergency)
				else:	
					#ralentissement des vehicules pour les intersections sans feux
					vehNearVehEmergency2(ListeVehIDJunc,index,vehIdEmergency)
					
			#remise a jour des feux
			if TypeJunction[index]=='traffic_light'and Initialize[index]=='1':
				UpdateTrafficlights=updateTrafficlights(vehIdEmergency, EdgeInJunction,EdgeOutJunction,IdJunction,index,IdTrafficLights,ProgramTrafficlights,Initialize)
				ProgramTrafficlights=UpdateTrafficlights[0]
				Initialize=UpdateTrafficlights[1]
			
		step=step+1
traci.close()
sys.stdout.flush()
       




