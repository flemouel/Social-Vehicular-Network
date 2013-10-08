#!/usr/bin/env python

import libxml2,sys
from libxml2 import xmlAttr

NewDest=sys.argv[2]
CurrentDep=sys.argv[1]

#modification du fichier xml des arrivees et des departs

from xml.dom.minidom import * 
def modify_node(node):
    i=0
    for n in node.childNodes:
        if n.nodeType == Node.ELEMENT_NODE:
	    if "depart" in n.attributes.keys():
		n.setAttribute("to",NewDest)
		n.setAttribute("from",CurrentDep)
		i=i+1
        modify_node(n) 
 
try:
    xmldoc = parse('data/newmap.trips.xml')
    node_racine=xmldoc.documentElement
    modify_node(node_racine)
    filexsl = open('data/newmap.trips.xml',"w")
    filexsl.write(xmldoc.toxml())
    filexsl.close()
except Exception, e:
    raise e
