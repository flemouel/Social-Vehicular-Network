#!/usr/bin/env python
import libxml2, random
from libxml2 import xmlAttr

#Permet de savoir si la route du vehicule d'urgence a bien ete prise en compte 

doc=libxml2.parseFile("data/map.rou.xml")
ctxt=doc.xpathNewContext()
TypeVeh=map(xmlAttr.getContent,ctxt.xpathEval("//vehicle/@type"))
if len(TypeVeh)==0:
	print "Pas de vehicule d'urgence, veuillez relancer la simulation :./runner.sh n"
else:
	IdVehEmergency=map(xmlAttr.getContent,ctxt.xpathEval("//vehicle[@type]/@id"))
	print "le vehicule d'urgence est le numero : "+ str(IdVehEmergency[0])
