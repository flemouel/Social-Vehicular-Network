import libxml2
from libxml2 import xmlAttr
doc=libxml2.parseFile("data/maptripinfo.out.xml")
ctxt=doc.xpathNewContext()
duration= map(xmlAttr.getContent,ctxt.xpathEval("//tripinfo[@vType='public_emergency']/@duration"))
routeLength= map(xmlAttr.getContent,ctxt.xpathEval("//tripinfo[@vType='public_emergency']/@routeLength"))

duration=float(duration[0])
duration=duration/60
duration=str(duration)
print "Le parcours moyen en temps du vehicule d'urgence est " + duration +" min"

routeLength=float(routeLength[0])
routeLength=routeLength/1000
routeLength=str(routeLength)
print "Le parcours moyen en distance du vehicule d'urgence : est " + routeLength +" km"

exit()



