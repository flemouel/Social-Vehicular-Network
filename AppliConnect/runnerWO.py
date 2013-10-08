#!/usr/bin/env python

import os,subprocess,sys,shutil
from sumolib import checkBinary

	
sumoBinary = checkBinary('sumo-gui')
sumoConfig = "data/mapWO.sumocfg"

#run simulation
sumoProcess = subprocess.Popen(" %s -c %s" % (sumoBinary,sumoConfig),shell=True, stdout=sys.stdout)
sys.stdout.flush()







