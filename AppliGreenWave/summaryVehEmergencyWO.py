import libxml2
from libxml2 import xmlAttr
doc=libxml2.parseFile("data/maptripinfoWO.out.xml")
ctxt=doc.xpathNewContext()
duration= map(xmlAttr.getContent,ctxt.xpathEval("//tripinfo[@vType='public_emergency']/@duration"))
routeLength= map(xmlAttr.getContent,ctxt.xpathEval("//tripinfo[@vType='public_emergency']/@routeLength"))

duration=float(duration[0])
Duration=duration/60
Duration=str(Duration)
print "Le parcours moyen en temps du vehicule d'urgence est " + Duration +" min"

routeLength=float(routeLength[0])
RouteLength=routeLength/1000
RouteLength=str(RouteLength)
print "Le parcours moyen en distance du vehicule d'urgence : est " +RouteLength +" km"


MeanSpeed=((routeLength/duration)*3600)/1000
MeanSpeed=str(MeanSpeed)
print "La vitesse moyenne du vehicule d'urgence est de " + MeanSpeed + " km/h"

exit()



