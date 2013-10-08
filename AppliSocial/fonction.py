#!/usr/bin/env python
import libxml2,random
from libxml2 import xmlAttr
from random import randrange


#fonction pour trouver l'intersection de deux listes


def intersect(a, b):
	return list(set(a) & set(b))




#changement du fichier ou se trouve les communautes en liste de noeuds


def communityNodeList(File):
	g = open(File,"r")
	lignes=g.readlines()
	ListNodeCommunities=[]
	j=0
	for ligne in lignes:
		i=0
		l=0
		node=''
		community=''
		if ligne[0]!='#':
			ListNodeCommunities.append([])
			while i<len(ligne):
				if ligne[i]!='	' and ligne[i]!='\n':
					node=node+ligne[i]
					i=i+1
				else:
					ListNodeCommunities[j].append(node)
					node=''
					i=i+1
			j=j+1
	g.close()
	return ListNodeCommunities



#Liste des communautes formees dans le graphe social


def communitiesList(ListNodeCommunities):
	community=ListNodeCommunities[0][1]
	ListCommunities=[[]]
	i=0
	for Node in ListNodeCommunities:
		if Node[1]==community:
			ListCommunities[i].append(Node[0])
		else:
			i=i+1
			community=Node[1]
			ListCommunities.append([Node[0]])
	return ListCommunities



#liste des liens produits par le graphe social

def socialLink(graphFile):
	f = open(graphFile,"r")
	lignes=f.readlines()
	ListEdge=[]
	for ligne in lignes:
		i=0
		j=''
		k=''
		if ligne[0]!='#':
			while ligne[i]!='	':
				j=j+ligne[i]
				i=i+1
			while i<len(ligne):
				if ligne[i]!='\t' and ligne[i]!='\n':
					k=k+ligne[i]
					i=i+1
				else:
					i=i+1
		ListEdge.append([j,k])
	f.close()
	return ListEdge




#Liste de tous les vehicules presents dans la simulation

def listVehID(FichierMapXml):
	doc=libxml2.parseFile(FichierMapXml)
	ctxt=doc.xpathNewContext()
	ListVehID= map(xmlAttr.getContent,ctxt.xpathEval("//@id"))
	return ListVehID





#Liste des noms des Points d'interets dans la ville

def listPoIID(FichierPoIxml):
	doc2=libxml2.parseFile(FichierPoIxml)
	ctxt2=doc2.xpathNewContext()
	ListPoIID= map(xmlAttr.getContent,ctxt2.xpathEval("//@id"))
	return ListPoIID




#Liste des infos sur les points d'interets et liste des vehicules possedant ces infos

def listInfos(rate,ListPoIID,ListVehID):
	ListInfo=[]
	ListInfoVehID=[]
	for vehID in ListVehID:
		rand=random.uniform(0,1)
		rate=float(rate)
		if rand<rate:
			ListInfoVehID.append(vehID)
			ListInfo.append(ListPoIID[randrange(len(ListPoIID))])
	return ListInfoVehID, ListInfo





#mis en place de la nouvelle route pour les vehicules ayant recu l'info de leur communaute


def newRoute(FichierMapXml):
	ListEdgeVehID=[]
	doc=libxml2.parseFile(FichierMapXml)
	ctxt=doc.xpathNewContext()
	edges=map(xmlAttr.getContent,ctxt.xpathEval("//@edges"))
	if len(edges)==0:
		return ListEdgeVehID
	StringEdges=list(edges[0])
	edge=''
	j=0
	#enregistrement de la nouvelle route au bon format
	for char in StringEdges:
		if char!=' ':
			edge=edge+char
			j=j+1
		else:
			ListEdgeVehID.append(edge)
			edge=''
			j=j+1
		if j==len(StringEdges):
			ListEdgeVehID.append(edge)
	return ListEdgeVehID





