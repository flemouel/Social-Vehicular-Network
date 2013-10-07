#!/usr/bin/env python

import libxml2
from libxml2 import xmlAttr
doc=libxml2.parseFile("data/Depart.trips.xml")
doc2=libxml2.parseFile("data/Arrivee.trips.xml")

ctxt=doc.xpathNewContext()
ctxt2=doc2.xpathNewContext()

From= map(xmlAttr.getContent,ctxt.xpathEval("//@from"))
To= map(xmlAttr.getContent,ctxt2.xpathEval("//@to"))
F=len(From)

from xml.dom.minidom import * 
def modify_node(node):
    i=0
    for n in node.childNodes:
        if n.nodeType == Node.ELEMENT_NODE:
	    if "from" in n.attributes.keys():
                n.setAttribute("from", From[i])
		n.setAttribute("to",To[i])
		i=i+1
        modify_node(n) 
 
try:
    xmldoc = parse('data/map.trips.xml')
    node_racine=xmldoc.documentElement
    modify_node(node_racine)
    filexsl = open('data/map.trips.xml',"w")
    filexsl.write(xmldoc.toxml())
    filexsl.close()
except Exception, e:
    raise e
