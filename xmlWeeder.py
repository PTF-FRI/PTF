#Very rudimentary! I will work on it over the weekend

import xml.etree.ElementTree as ET
import numpy as np
import sys
import glob

datafiles = glob("data/*.xml")
for file in datafiles:
	numObs.append = ET.parse(file).getroot()[0][0][41][0]
#Above in that big list is where the number of observations is stored as an XML element

avgObs = np.mean(numObs)
cutoff = avgObs - (1.5*np.std(numObs))
print("There are " + len(numObs) + "data files here. The mean number of observations is " + avgObs +" .")
print("Every file with less than " + cutoff + " observations will be removed.")
#for file in datafiles:
#	if (numObs < cutoff):
#		os.remove(file)

