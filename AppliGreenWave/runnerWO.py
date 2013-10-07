#!/usr/bin/env python


import os,subprocess,sys,shutil
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', "tools")) # tutorial in tests
sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(os.path.dirname(__file__), "..", "..", "..")), "tools")) # tutorial in docs
from sumolib import checkBinary

	
sumoBinary = checkBinary('sumo-gui')
sumoConfig = "data/mapWO.sumocfg"

#run simulation
sumoProcess = subprocess.Popen(" %s -c %s" % (sumoBinary,sumoConfig),shell=True, stdout=sys.stdout)
sys.stdout.flush()







