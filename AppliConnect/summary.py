import libxml2
from libxml2 import xmlAttr
doc=libxml2.parseFile("data/maptripinfo.out.xml")
ctxt=doc.xpathNewContext()
duration= map(xmlAttr.getContent,ctxt.xpathEval("//@duration"))
waitSteps= map(xmlAttr.getContent,ctxt.xpathEval("//@waitSteps"))
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
TotalwaitSteps=0
while j<len(waitSteps):
	waitSteps[j]=float(waitSteps[j])
	TotalwaitSteps=TotalwaitSteps+waitSteps[j]
	j=j+1

MeanwaitSteps=TotalwaitSteps/len(waitSteps)
MeanwaitSteps=str(MeanwaitSteps)
TotalVeh=str(len(duration))
print "Le temps moyen d'attente par vehicule est : " + MeanwaitSteps +" s"
print " "
print "Le nombre de vehicule est : " + TotalVeh


exit()



