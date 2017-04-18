# Doing all the necessary imports
import sys
import os
import re
import numpy as np
import matplotlib.pyplot as plt

from astroquery.irsa import Irsa
from astropy.coordinates import SkyCoord
from astropy.table import Table, vstack
import astropy.units as u

my_table = Table.read("Retrieved_WD.csv", format='ascii.csv')
for colname in my_table.colnames:
  if (re.match('^c|\w*id|\w*percentiles|rms|\w*best|\w*consec|\w*good|\w*above|\w*below', colname)):
    my_table.remove_column(colname)

my_table.remove_column('ra')
my_table.remove_column('dec')

backup_table = Table(my_table,copy=True)

for i in backup_table.colnames:
  backup_table.remove_column(i)
  for j in backup_table.colnames:
    if i == j:
      continue
    print(i+" "+j+"\n")
    plt.figure()
    plt.plot(my_table[i],my_table[j],'ro')
    plt.title("Mean Statistics: "+i+" vs. "+j)
    plt.xlabel(i)
    plt.ylabel(j)
    plt.savefig("pics/"+i+"_"+j+".png")
