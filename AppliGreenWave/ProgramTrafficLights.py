#!/usr/bin/env python
import traci

#Initialisation des longueurs des listes

def initialisation(CoordJunctionList):
	return len(CoordJunctionList)*range(1)



#Enregistrement des parametres du vehicule d'urgence lorsqu'il apparait sur le reseau

def presenceVehEmergency(check):
	for vehID in traci.vehicle.getIDList():
		if traci.vehicle.getTypeID(vehID)=='public_emergency':
			coordxVehEmergency=traci.vehicle.getPosition(vehID)[0]
			coordyVehEmergency=traci.vehicle.getPosition(vehID)[1]
			vehIdEmergency=vehID
			RoutevehEmergency=traci.vehicle.getRoute(vehIdEmergency)
			LastRoadVehEmergency=RoutevehEmergency[len(RoutevehEmergency)-2]
			Last2RoadVehEmergency=RoutevehEmergency[len(RoutevehEmergency)-1]
			check='ok'
	if check=='ok':
		return check,coordxVehEmergency,coordyVehEmergency,vehIdEmergency,RoutevehEmergency,LastRoadVehEmergency,Last2RoadVehEmergency
	else:
		return check,-1,-1,'',[],'',''




#Enregistrement des vehicules presents autour de l'intersection ou passe le vehicule d'urgence dans un rayon de 40metres par rapport à l'intersection : ListeVehIDJunc

def vehInJunction(index,ListeVehIDJunc,X,Y,EdgeInJunction,IdJunction):
	ListeVehIDJunc[index]=[]
	for vehID in traci.vehicle.getIDList():
		coordxVeh=traci.vehicle.getPosition(vehID)[0]
		coordyVeh=traci.vehicle.getPosition(vehID)[1]
		if (coordxVeh>=X-40) and (coordxVeh<=X+40) and (coordyVeh>=Y-40) and (coordyVeh<=Y+40) and (traci.vehicle.getRoadID(vehID) in EdgeInJunction[index]) and (traci.vehicle.getTypeID(vehID)!="public_emergency"):
			ListeVehIDJunc[index].append(vehID)
	return ListeVehIDJunc




#Enregistrement de la position des feux concernes par le passage du vehicule d'urgence

def listegreenposition(liste,vehIdEmergency,IdTrafficLights):
	l=0
	while l<len(traci.trafficlights.getControlledLanes(IdTrafficLights)):
		if traci.trafficlights.getControlledLanes(IdTrafficLights)[l]==traci.vehicle.getLaneID(vehIdEmergency):
			liste.append(l)
		l=l+1
	return liste




#Changement de l'etat du feu pour laisser le vehicule d'urgence passer

def changeTrafficLightState(vehIdEmergency,IdJunction,index,Done,Initialize,ProgramTrafficlights):
	IdTrafficLights=IdJunction[index]
	GreenPosition=listegreenposition([],vehIdEmergency,IdTrafficLights)

	#on memorise l'etat du feu pour le remettre a jour apres passage du vehicule d'urgence
	ProgramTrafficlights[index]=traci.trafficlights.getProgram(IdTrafficLights)
		
	state=traci.trafficlights.getRedYellowGreenState(IdTrafficLights)
	l=len(traci.trafficlights.getRedYellowGreenState(IdTrafficLights))
	s=list(state)
	i=0
	while i<len(s):
		#on passe au vert sur la voie ou se trouve le vehicule d'urgence
		if i in GreenPosition:
			s[i]='G'
			i=i+1
		#on passe les autres au rouge
		else:
			s[i]='r'
			i=i+1
	state="".join(s)
	traci.trafficlights.setRedYellowGreenState(IdTrafficLights,state)
	Initialize[index]='1'
	Done[index]='1'
	return Done, Initialize, IdTrafficLights, ProgramTrafficlights





#Changement du comportement des vehicules proches du vehicule d'urgence
	#Pour les vehicules proches sur la meme ligne au feu : acceleration

def vehNearVehEmergency1(ListeVehIDJunc,index,vehIdEmergency):
	for vehID in ListeVehIDJunc[index]:
		if traci.vehicle.getLaneID(vehID)==traci.vehicle.getLaneID(vehIdEmergency): 
			MaxSpeed=traci.lane.getMaxSpeed(traci.vehicle.getLaneID(vehIdEmergency))
			traci.vehicle.setAccel(vehID, MaxSpeed)
			




#Changement du comportement des vehicules proches du vehicule d'urgence
	#les vehicules proches du vehicule d'urgence a une intersection ralentissent

def vehNearVehEmergency2(ListeVehIDJunc,index,vehIdEmergency):
	for vehIDInter in ListeVehIDJunc[index]:
		if  traci.vehicle.getTypeID(vehIDInter)!="public_emergency" and traci.vehicle.getRoadID(vehIDInter)!=traci.vehicle.getRoadID(vehIdEmergency):
			speed=0
			duration=1
			traci.vehicle.slowDown(vehIDInter, speed, duration)
		MaxSpeed=traci.lane.getMaxSpeed(traci.vehicle.getLaneID(vehIdEmergency))
		traci.vehicle.setSpeed(vehIdEmergency, MaxSpeed)




#On remet a jour les feux apres le passage du vehicule d'urgence

def updateTrafficlights(vehIdEmergency,EdgeInJunction,EdgeOutJunction,IdJunction,index,IdTrafficLights,ProgramTrafficlights,Initialize):
	#lorsque le vehicule a quitte l'intersection
	if (traci.vehicle.getRoadID(vehIdEmergency) in EdgeOutJunction[index]) or (IdJunction[index] in traci.vehicle.getRoadID(vehIdEmergency)):
		traci.trafficlights.setProgram(IdTrafficLights,ProgramTrafficlights[index])
		Initialize[index]='0'
	#cas ou le vehicule demarre a une intersection
	elif (traci.vehicle.getRoute(vehIdEmergency)[0] in EdgeInJunction[index]):
		print "Depart"

	#cas d'erreur lorque l'intersection est complexe
	elif not(traci.vehicle.getRoadID(vehIdEmergency) in EdgeInJunction[index]):  
		for edge in EdgeOutJunction[index]:
			if "#" in traci.vehicle.getRoadID(vehIdEmergency) :
				pos=traci.vehicle.getRoadID(vehIdEmergency).split('#')
				Fin=int(pos[1])
				Fin=Fin-1
				Fin=str(Fin)
				pos=pos[0]+'#'+Fin
				if pos in edge:
					traci.trafficlights.setProgram(IdTrafficLights,ProgramTrafficlights[index])
					Initialize[index]='0'
	return ProgramTrafficlights,Initialize













	
