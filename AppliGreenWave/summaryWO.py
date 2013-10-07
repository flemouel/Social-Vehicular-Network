import libxml2
from libxml2 import xmlAttr
doc=libxml2.parseFile("data/maptripinfoWO.out.xml")
ctxt=doc.xpathNewContext()
duration= map(xmlAttr.getContent,ctxt.xpathEval("//@duration"))
routeLength= map(xmlAttr.getContent,ctxt.xpathEval("//@routeLength"))
i=0
TotalDuration=0
while i<len(duration):
	duration[i]=float(duration[i])
	TotalDuration=TotalDuration+duration[i]
	i=i+1
MeanDuration=(TotalDuration/len(duration))/60
MeanDuration=str(MeanDuration)
print "Le parcours moyen en temps est " + MeanDuration +" min"
j=0
TotalRouteLength=0
while j<len(routeLength):
	routeLength[j]=float(routeLength[j])
	TotalRouteLength=TotalRouteLength+routeLength[j]
	j=j+1
MeanRouteLength=(TotalRouteLength/len(routeLength))/1000
MeanRouteLength=str(MeanRouteLength)
print "Le parcours moyen en distance : est " + MeanRouteLength +" km"
k=0
MeanSpeed=list()
TotalMeanSpeed=0
while k<len(duration):
	MeanSpeed.append(routeLength[k]/duration[k])
	TotalMeanSpeed=TotalMeanSpeed+MeanSpeed[k]
	k=k+1
TotalMeanSpeed=((TotalMeanSpeed/len(duration))*3600)/1000
TotalMeanSpeed=str(TotalMeanSpeed)
print "La vitesse moyenne totale est de " + TotalMeanSpeed + " km/h"
print "Il y a " + str(len(duration)) +" vehicules"

exit()



