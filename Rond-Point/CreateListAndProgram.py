
import traci 



def CreateProgramTrafficLights(Program,BusRedOutRedInGreen,BusRedOutRedInYellow,BusRedOutGreenInRed,BusRedOutYellowInRed,BusRedOutRedInRed):
	i=1
	while i<=52:
		if i<=15:
			Program.append(BusRedOutRedInGreen)
		if 15<i<=18:
			Program.append(BusRedOutRedInYellow)
		if 18<i<=21:		
			Program.append(BusRedOutRedInRed)
		if 21<i<=46:
			Program.append(BusRedOutGreenInRed)
		if 46<i<=49:
			Program.append(BusRedOutYellowInRed)
		if 49<i<=52:
			Program.append(BusRedOutRedInRed)
		i=i+1
	return Program

def CreateProgramBusTrafficLights(Program,BusGreen,BusYellow,BusRedOutRedInGreen,BusRedOutRedInYellow,BusRedOutGreenInRed,BusRedOutYellowInRed,BusRedOutRedInRed):
	i=1
	while i<=24:
		if i==1:
			Program.append(BusRedOutYellowInRed)
		if i==2:
			Program.append(BusRedOutRedInYellow)
		if 3<=i<=19:
			Program.append(BusGreen)
		if 19<=i<=21:
			Program.append(BusYellow)
		if i==22:
			Program.append(BusRedOutGreenInRed)
		if i==23:
			Program.append(BusRedOutRedInGreen)
		if i==24:
			Program.append(BusRedOutRedInRed)
		i=i+1
	return Program
			
	



def ChangeBusTrafficLights(loop1,loop2,feu,step,check,Prog,programPointer,i,ProgInitial,counter,b):
    no1 = traci.inductionloop.getLastStepVehicleNumber(loop1)
    no2 = traci.inductionloop.getLastStepVehicleNumber(loop2)
    no=no1+no2
    a=len(Prog)-3
    c=len(Prog)-2
    if no==0 and check=='ok':
	if i==len(ProgInitial)-1:
		traci.trafficlights.setRedYellowGreenState(feu,ProgInitial[i])
		i=0
	else:
		traci.trafficlights.setRedYellowGreenState(feu,ProgInitial[i])
		i=i+1
    if no > 0 and check=='':
	if counter!=0:
		if c-b==0:
			traci.trafficlights.setRedYellowGreenState(feu,Prog[1])
			counter=counter-1
		elif a-b==0:
			traci.trafficlights.setRedYellowGreenState(feu,Prog[0])
			counter=counter-1
	else :
		programPointer=programPointer+1
		i=programPointer
		if i==len(Prog)-3:
                	check='ok'
			i=0
		else:
			traci.trafficlights.setRedYellowGreenState(feu,Prog[i])
    if no==0 and check=='':
	i=i+1
	if i==len(Prog)-3:
		check='ok'
		programPointer=len(Prog)-3
		i=0
	else:
        	traci.trafficlights.setRedYellowGreenState(feu,Prog[i])	
		
    if no > 0 and check=='ok':
	check=''
	statutactuel=traci.trafficlights.getRedYellowGreenState(feu)
	programPointeur=Prog.index(statutactuel)
	b=programPointeur
	if c-b==0:
		traci.trafficlights.setRedYellowGreenState(feu,Prog[1])
		counter=2
	elif a-b==0:
		traci.trafficlights.setRedYellowGreenState(feu,Prog[0])
		counter=2
	else:
		counter=0
	programPointer=1
    return check,programPointer,i,counter,b

