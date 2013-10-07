#!/usr/bin/env python
import libxml2, random
from libxml2 import xmlAttr

def number(FichierRouXml):
	doc=libxml2.parseFile(FichierRouXml)
	ctxt=doc.xpathNewContext()
	ListVeh=map(xmlAttr.getContent,ctxt.xpathEval("//vehicle/@depart"))
	return len(ListVeh)


def createListe(FichierMapXml):
	doc=libxml2.parseFile(FichierMapXml)
	ctxt=doc.xpathNewContext()
	#on recupere les coordonnees de chaque intersection
	CoordXJunction=map(xmlAttr.getContent,ctxt.xpathEval("//junction[@shape]/@x"))
	CoordYJunction=map(xmlAttr.getContent,ctxt.xpathEval("//junction[@shape]/@y"))
	TypeJunction=map(xmlAttr.getContent,ctxt.xpathEval("//junction[@shape]/@type"))
	IdJunction=map(xmlAttr.getContent,ctxt.xpathEval("//junction[@shape]/@id"))
	IdEdge=map(xmlAttr.getContent,ctxt.xpathEval("//edge[@priority]/@id"))
	EdgeInJunction=map(xmlAttr.getContent,ctxt.xpathEval("//junction[@shape]/@incLanes"))
	EdgeFromJunction=map(xmlAttr.getContent,ctxt.xpathEval("//edge[@priority]/@from"))
	return CoordXJunction, CoordYJunction, TypeJunction, IdJunction, IdEdge, EdgeInJunction, EdgeFromJunction

def coordinateJunction(X,Y):
	i=0
	List=[]
	while i<len(X):
       	 	List.append([X[i],Y[i]])
		i=i+1
	return List

def edgeInJunction(List):
	j=0
	NewList=[]
	while j<len(List):
		NewList.append(List[j].split(" "))
		k=0
		while k<len(NewList[j]):
			NewList[j][k]=NewList[j][k].rstrip('0')
			NewList[j][k]=NewList[j][k].rstrip('_')
			k=k+1
		j=j+1
	return NewList

def edgeOutJunction(List1,List2,List3):
	NewList=[]
	l=0
	while l<len(List1):
		m=0
		L=[]
		while  m<len(List2):
			if (List1[l]==List2[m]):
				L.append(List3[m])
				m=m+1
			else:
				m=m+1
		NewList.append(L)
		l=l+1
	return NewList

