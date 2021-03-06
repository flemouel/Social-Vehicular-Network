#!/usr/bin/env python
import os,subprocess,sys,shutil,sumolib
from sumolib import checkBinary
import traci,libxml2,random
from libxml2 import xmlAttr


#Creation des listes de donnees utiles

def createList(FichierMapXml):
	doc=libxml2.parseFile(FichierMapXml)
	ctxt=doc.xpathNewContext()

	#coordonnees des intersections autre que les feux
	XJuncAll=map(xmlAttr.getContent,ctxt.xpathEval("//junction[@type='priority']/@x"))
	YJuncAll=map(xmlAttr.getContent,ctxt.xpathEval("//junction[@type='priority']/@y"))

	#nom des liens entrant sur chaque intersection
	EdgeIncAll=map(xmlAttr.getContent,ctxt.xpathEval("//junction[@type='priority']/@incLanes"))

	#nom de chaque intersection
	JuncIdAll=map(xmlAttr.getContent,ctxt.xpathEval("//junction[@type='priority']/@id"))

	#nom des liens 
	EdgeIdAll=map(xmlAttr.getContent,ctxt.xpathEval("//edge[@priority]/@id"))

	#nom des departs de chaque lien (from-to)
	EdgeFromAll=map(xmlAttr.getContent,ctxt.xpathEval("//edge[@priority]/@from"))

	return XJuncAll,YJuncAll,EdgeIncAll,JuncIdAll,EdgeIdAll,EdgeFromAll

#Choix des intersections ou le reroutage s'effectura

def rateOfJunctionChosen(rate):
	CreateList=createList("data/map.net.xml")
	XJuncAll=CreateList[0]
	YJuncAll=CreateList[1]
	EdgeIncAll=CreateList[2]
	JuncIdAll=CreateList[3]
	XJunc=[]
	YJunc=[]
	EdgeInc=[]
	JuncId=[]
	N=0
	rate=float(rate)
	while N<len(XJuncAll):
		rand=random.uniform(0,1)
		if rand<rate:
			XJunc.append(XJuncAll[N])
			YJunc.append(YJuncAll[N])		
			EdgeInc.append(EdgeIncAll[N])
			JuncId.append(JuncIdAll[N])
			N=N+1
		else:
			N=N+1
	return XJunc,YJunc,EdgeInc,JuncId

#Liste des coordonnees de chaque intersection

def listInter(X,Y):
	i=0
	ListInter=[]
	while i<len(X):
		ListInter.append([X[i],Y[i]])
		i=i+1
	return ListInter

#Sauvegarde des identifiants des intersections ou s'effectue le reroutage

def save(Fichier,JuncId):
	f = open(Fichier, "w")

	for element in JuncId:
		f.write(element+' ')
		f.write('\n')
	f.close()


#Liste des liens entrants de chaque intersection

def listEdgeInc(EdgeInc):
	j=0
	ListEdgeInc=[]
	while j<len(EdgeInc):
		ListEdgeInc.append(EdgeInc[j].split(" "))
		k=0
		while k<len(ListEdgeInc[j]):
			ListEdgeInc[j][k]=ListEdgeInc[j][k].rstrip('0')
			ListEdgeInc[j][k]=ListEdgeInc[j][k].rstrip('_')
			k=k+1
		j=j+1
	return ListEdgeInc

#Liste des liens sortants de chaque intersection

def listEdgeOut(JuncId):
	CreateList=createList("data/map.net.xml")
	EdgeFrom=CreateList[5]
	EdgeId=CreateList[4]
	ListEdgeOut=[]
	l=0
	while l<len(JuncId):
		m=0
		Liste=[]
		while  m<len(EdgeFrom):
			if (JuncId[l]==EdgeFrom[m]):
				Liste.append(EdgeId[m])
				m=m+1
			else:
				m=m+1
		ListEdgeOut.append(Liste)
		l=l+1
	return ListEdgeOut

#initialisation de la liste des vehicules visitant chaque intersection

def juncVisitedVehID(ListInter):
	JuncVisitedVehID=len(ListInter)*range(1)
	i=0
	while i<len(JuncVisitedVehID):
		JuncVisitedVehID[i]=[]
		i=i+1
	return JuncVisitedVehID


#Liste des temps de passage de chaque lien sortant de l'intersection

def currentTravelEdgeOut(index,ListEdgeOut,step):
	CurrentTravelEdgeOut=[]
	for edge in ListEdgeOut[index]:
		traci.edge.adaptTraveltime(edge,traci.edge.getTraveltime(edge))
		CurrentTravelEdgeOut.append(traci.edge.getAdaptedTraveltime(edge,step))
	return CurrentTravelEdgeOut


#Liste des liens sortant les plus longs en temps de passage

def slowEdge(CurrentTravelEdgeOut,index,ListEdgeOut):
	l=0
	SlowEdge=[]
	#Lien sortant le plus rapide
	Min=min(CurrentTravelEdgeOut)
	#Lien sortant le plus long
	Max=max(CurrentTravelEdgeOut)		
	while l<len(ListEdgeOut[index]):
		if (CurrentTravelEdgeOut[l]>Min):
			SlowEdge.append(ListEdgeOut[index][l])
		l=l+1
	return SlowEdge


#initialisation des poids des liens modifies a l'intersection

def updateEdgeWeight(ListEdgeOut,index):
	for edge in ListEdgeOut[index]:
		lane=edge+'_0'
		L=traci.lane.getLength(lane)
		S=traci.lane.getMaxSpeed(lane)
		#poids initial : longueur/Vitesse max
		T=L/S
		traci.edge.adaptTraveltime(edge,T)
		



