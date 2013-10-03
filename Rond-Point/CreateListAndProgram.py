
import traci 



def CreateProgramTrafficLights(Program,BusRedOutRedInGreen,BusRedOutRedInYellow,BusRedOutGreenInRed,BusRedOutYellowInRed):
	i=1
	while i<=79:
		if i<=30:
			Program.append(BusRedOutRedInGreen)
		if 30<i<=40:
			Program.append(BusRedOutRedInYellow)
		if 40<i<=70:
			Program.append(BusRedOutGreenInRed)
		if 70<i<=79:
			Program.append(BusRedOutYellowInRed)
		i=i+1
	return Program

def CreateProgramBusTrafficLights(Program,BusGreen,BusYellow,BusRedOutRedInGreen,BusRedOutRedInYellow,BusRedOutGreenInRed,BusRedOutYellowInRed):
	i=1
	while i<=15:
		if i==1:
			Program.append(BusRedOutYellowInRed)
		if i==2:
			Program.append(BusRedOutRedInYellow)
		if 3<=i<=10:
			Program.append(BusGreen)
		if 11<=i<=13:
			Program.append(BusYellow)
		if i==14:
			Program.append(BusRedOutGreenInRed)
		if i==15:
			Program.append(BusRedOutRedInGreen)
		i=i+1
	return Program
			
	



def ChangeBusTrafficLights(loop1,loop2,feu,step,check,Prog,programPointer,i,ProgInitial):
    no1 = traci.inductionloop.getLastStepVehicleNumber(loop1)
    no2 = traci.inductionloop.getLastStepVehicleNumber(loop2)
    no=no1+no2
    if no==0 and check=='ok':
	if i==len(ProgInitial)-1:
		traci.trafficlights.setRedYellowGreenState(feu,ProgInitial[i])
		i=0
	else:
		traci.trafficlights.setRedYellowGreenState(feu,ProgInitial[i])
		i=i+1
    if no > 0 and check=='':
	programPointer=programPointer+1
	i=programPointer
	if i==len(Prog)-2:
                check='ok'
		i=0
	else:
		traci.trafficlights.setRedYellowGreenState(feu,Prog[i])
    if no==0 and check=='':
	i=i+1
	if i==len(Prog)-2:
		check='ok'
		programPointer=len(Prog)-2
		i=0
	else:
        	traci.trafficlights.setRedYellowGreenState(feu,Prog[i])	
		
    if no > 0 and check=='ok':
	check=''
	statutactuel=traci.trafficlights.getRedYellowGreenState(feu)
	programPointeur=Prog.index(statutactuel)
	a=len(Prog)-2
	c=len(Prog)-1
	b=programPointeur
	if c-b==0:
		traci.trafficlights.setRedYellowGreenState(feu,Prog[1])
	if a-b==0:
		traci.trafficlights.setRedYellowGreenState(feu,Prog[0])
	programPointer=1
    return check,programPointer,i

