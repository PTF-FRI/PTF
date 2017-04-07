#Very rudimentary! I will work on it over the weekend

import xml.etree.ElementTree as ET
import sys

for (filename,i) in enumerate(dir(data)):
	numObs = ET.parse(filename).getroot()[0][0][41][0]
#Above in that big list is where the number of observations is stored as an XML element
	if (numObs > 4):
		#keep
	else
		#destroy
