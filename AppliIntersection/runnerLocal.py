#!/usr/bin/env python

#simulation avec reroutage des vehicules sur un pourcentage d'intersection


import os,subprocess,sys,shutil,sumolib
from sumolib import checkBinary
import traci,libxml2,random
from libxml2 import xmlAttr
from fonctionLocal import rateOfJunctionChosen,listInter,save,listEdgeInc,listEdgeOut,juncVisitedVehID,slowEdge,currentTravelEdgeOut,updateEdgeWeight


PORT = 8813

	
sumoBinary = checkBinary('sumo-gui')
sumoConfig = "data/mapLocal.sumocfg"

if not traci.isEmbedded():
	
	#run simulation
        sumoProcess = subprocess.Popen(" %s -c  %s" % (sumoBinary,sumoConfig),shell=True, stdout=sys.stdout)
        traci.init(PORT)

#taux d'intersection touchees par le reroutage

rate=sys.argv[1]


#Choix des intersections ou le reroutage s'effectura

JunctionChosen=rateOfJunctionChosen(rate)
XJunc=JunctionChosen[0]
YJunc=JunctionChosen[1]
EdgeInc=JunctionChosen[2]
JuncId=JunctionChosen[3]


#Liste des coordonnees des intersecions

ListInter=listInter(XJunc,YJunc)

#On enregistre la Liste d'intersections choisies dans un fichier

save("data/ListeInterLocal",JuncId)

#Liste des liens entrants de chaque intersection

ListEdgeInc=listEdgeInc(EdgeInc)

#Liste des liens sortants de chaque intersection

ListEdgeOut=listEdgeOut(JuncId)

#initialisation des liens visites

JuncVisitedVehID=juncVisitedVehID(ListInter)

#pas de temps

step=0

#Liste des vehicules

ListvehID=[]

while step == 0 or traci.simulation.getMinExpectedNumber() > 0:
    	traci.simulationStep()
	index=0
        #a chaque pas de temps pour chaque intersection :
	for CoordInter in ListInter:
        	index=ListInter.index(CoordInter)
		CoordInterX=float(CoordInter[0])
		CoordInterY=float(CoordInter[1])

		#Liste des temps de passage de chaque lien sortant de l'intersection
		CurrentTravelEdgeOut=currentTravelEdgeOut(index,ListEdgeOut,step)

		#Liste des liens sortant les plus longs en temps de passage
		SlowEdge=slowEdge(CurrentTravelEdgeOut,index,ListEdgeOut)

		for vehID in traci.vehicle.getIDList():
			coordVehx=traci.vehicle.getPosition(vehID)[0]
			coordVehy=traci.vehicle.getPosition(vehID)[1]
			#on considere les vehicules sur les liens entrants presents a l'intersection
			if (coordVehx>=CoordInterX-40) and (coordVehx<=CoordInterX+40) and (coordVehy>=CoordInterY-40) and (coordVehy<=CoordInterY+40) and (traci.vehicle.getRoadID(vehID) in ListEdgeInc[index]) and not(vehID in JuncVisitedVehID[index]):

				#enregistrement du passage du vehicule pour eviter les boucles infinies
				JuncVisitedVehID[index].append(vehID)

				#changement du poids des liens sortant les plus longs
				#Les vehicules vont prendre le (les) lien(s) le (les) plus rapide(s)
				for edge in SlowEdge:
					traci.edge.adaptTraveltime(edge,920000)

				#recalcule du plus court chemin avec cette nouvelle direction prise pour chaque vehicule
				traci.vehicle.rerouteTraveltime(vehID)

		#initialisation des poids des liens modifies a l'intersection
		updateEdgeWeight(ListEdgeOut,index)

	step=step+1
traci.close()
sys.stdout.flush()
