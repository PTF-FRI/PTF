# Doing all the necessary imports
from glob import glob
import numpy as np
import sys
import os
import csv
import glue

from astroquery.irsa import Irsa
from astropy.coordinates import SkyCoord
from astropy.table import Table, vstack
import astropy.units as u

# Converting what we ask to find into arrays
def CSV_to_coords(filename):
    all_coords = []
    myCSVReader = csv.DictReader(open(filename), fieldnames=['name','ra','dec'], delimiter=",", quotechar='"')
    for row in myCSVReader:
        #print(row, row['ra'])
        #print(SkyCoord(float(row['ra']),float(row['dec']),frame='icrs', unit='deg'))
        all_coords.append(SkyCoord(float(row['ra']),float(row['dec']),frame='icrs', unit='deg'))
    return all_coords

# Downloading Data
filename = input('What is the Input File name? (give in CSV): ')
all_coords = CSV_to_coords(filename)

all_data = []

for WDstar in all_coords:
    try:
        table = Irsa.query_region(coordinates=WDstar,catalog='ptf_objects',spatial="Cone",radius=5*u.arcsec)
    except:
        table = []
        print("No data found at "+WDstar.toString())
    table = table.filled(-99)
    all_data.append(table)

#Removes all the stars for which no data was found
list_data = list(filter(None,all_data))

#Combines all the stars' data into one big huge table
master_table = vstack(list_data)

#saving it to a file so that everytime it runs it doesn't have to download a bunch of data again
writeOpt = input("Wouldyou like to save this table?[y/n]")
if (writeOpt == "y"):
    master_table.write("Retrieved_"+filename,format='ascii.csv')
    print ("Saved")

#Note: To read the data in from the file (like in another program), use the command below:
# my_table = Table.read(filename, format='ascii.csv')
