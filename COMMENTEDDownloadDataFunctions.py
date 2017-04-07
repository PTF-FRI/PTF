
# coding: utf-8

# In[ ]:

#NOTE that you can't download COMMENTEDDownloadDataFunctions and run it and expect it to work
#(you would have to change some stuff, e.g. in cell 2 don't use from PTFViewerimport download_ptf)
#but you can look at it and use the comments to make sense of Keaton's code
#-Josey

#this cell is copied from Keaton's PFTViewer at github.com/keatonb/PTFViewer
from __future__ import absolute_import
from __future__ import print_function
from glob import glob
import numpy as np
import sys
import os
from astroquery.irsa import Irsa
from astropy.coordinates import SkyCoord
from astropy.table import Table
import astropy.units as u

from bokeh.io import curdoc
from bokeh.layouts import row, column, widgetbox
from bokeh.models import ColumnDataSource, DataRange1d, Select, Button, DataTable, TableColumn, TextInput, Div, VBox, RadioButtonGroup
from bokeh.plotting import figure
#you may need to upgrade bokeh by typing into the terminal:
#pip install --user --upgrade bokeh



#defines a function that downloads the data, from Keaton's PTFViewer.py

#Download PTF data and add to list
def download_ptf(coords,name=None,directory=None):
    #None is a placeholder value that is used instead of modifying the default value
    #name and directory are optional argments
    #multidownload.py passes arguments to coords, name, and directory
    """Download PTF light curve data.
    Keyword arguments:
    coords -- astropy.coordinates.SkyCoord object
    name -- string for filename (default None, i.e. PTF oid)
    directory -- location to save data (default './')
    """
    #Download the PTF data
    if directory is None:
        directory = datadir
        #datadir appears earlier in the PTFViewer.py code, before this function is defined
        #Note that multidownload.py passes an argument to directory, 
        #so directory!=None if we call this from multidownload.py
        #If we copy-paste this function into our own code
        #we will want to define datadir before this function
        #or make sure we pass an argument into directory
    table = Irsa.query_region(coordinates=coords,catalog='ptf_lightcurves',radius=5*u.arcsec)
    #IRSA is the Infrared Science Archive
    #this performs (I think) a cone search, where radius is the cone search radius
    #NOTE the catalog arguent - we may want to change this to the PTF objects catalog!
    #u.arcsec specifies the unit
    #the query returns the results in an astropy.table.Table
    table = table.filled(-99)
    #table.filled replaces missing or invalid entries with fill values, in this case, -99
    #Don't only use the nearest!
    nearest = np.where(table['dist'] == np.min(table['dist']))
    #(I think) this line finds the nearest result to the user-given coordinates,
    #and stores the location of that result in the variable nearest
    if name is None:
        name = str(table["oid"][0])
        #oid is object id assigned by Palomar
        
    nearestcoords = SkyCoord(table["ra"][nearest][0],table["dec"][nearest][0],unit="deg")
    #gives ra, dec coordinates of the "nearest" object
    #recall "nearest" is storing the location in the table 
    #of the object that is the minimum distance away
    matchedinds = []
    for i in range(len(table)):
        #iterates through the entire table, 
        #finds separation between each object i and the "nearest" object
        #If object i and the "nearest" object are fewer than 3 arcsec away from each other,
        #adds the index of object i to a table of matched indexes
        #(considers object i and the "nearest" object to be the same)
        if nearestcoords.separation(SkyCoord(table["ra"][i],table["dec"][i],unit="deg")) < 3*u.arcsec:
            matchedinds.append(i)
                
    #saves the matched data points to an xml file
    fname = directory+name+'.xml'
    table[matchedinds].write(fname, format='votable', overwrite=True)
    #the documentation for table.write is found at
    #http://docs.astropy.org/en/stable/io/unified.html#built-in-readers-writers
    print(str(len(matchedinds))+" data points saved to "+fname)
    
    #add to target menu and display
    #^Keaton wrote this above comment
    #idk what these lines do
    targets[name] = fname
    target_select.options.append(name)
    target_select.value = target_select.options[-1]




# In[6]:

#this cell is copied from Keaton's multidownload.py code

#!/usr/bin/python
#what does this line do? -J
"""
Script to download Palomar Transient Factory light curves for a list of targets
for visualization with PTFViewer: https://github.com/keatonb/PTFViewer
input csv file should have format:
targetname,rad,decd
where rad and decd are the RA and Dec in decimal degrees.
WARNING: Downloads data for nearest PTF source to given coordinates, not 
necessarily for the target you want.
Learn more at https://github.com/keatonb/PTFViewer/
@author: keatonb
"""
#Note that this imports the download_ptf function from PFTViewer!
from __future__ import print_function
import sys
import os
import csv
from astropy.coordinates import SkyCoord
from PTFViewer import download_ptf
#Make sure PTFViewer.py is in the same folder as multidownload.py. Otherwise this will throw an error

nargs = len(sys.argv)
#sys.argv is a list that contains the command-line arguments

if nargs < 2:
    print('usage: python multidownload.py input_file.csv [/data/directory]')
    sys.exit()
#checks that the user put enough arguments into the command line
    
#In this section, the program sets the directory where the data should be saved, 
#and may create a new folder
datadir = os.getcwd()+'/data/'
#datadir is a string
#getcwd returns the current working directory
#+'/data/' appends the string /data/ to the cwd
if len(sys.argv) > 2:
    datadir = sys.argv[2]
    #sets the string datadir to the third argument entered into the command line
    #only if a third argument was entered (otherwise datadir still = [current directory]/data/)
    #(remember that Python starts counting at 0)
if datadir[-1] != '/':
    datadir += '/'
    #makes sure the string datadir ends with a / character
if not os.path.exists(datadir):
    datadir = os.getcwd()+'/data/'
    print(('Created data directory at '+datadir))
    if not os.path.exists(datadir):
        os.makedirs(datadir)
    #if the file path stored in the string datadir does not exist,
    #the string datadir is changed to [curent directory]/data/
        #then, if the folder /data/ does not exist in the current directory
        #the folder /data/ is created

#In this section, the program starts saving the data to the directory        
print(('Saving data to '+datadir))
        
csvname = sys.argv[1]
#sets the string csvname to the second argument entered into the command line
#csvname is the name of the file where the targets (name, ra, dec) are stored
with open(csvname) as csvfile:
#opens the file located at [csvname] and assigns it to the variable csvfile
#csvfile is object of type 'file' (not a string or array!)
#if the file cannot be opened, IOError is raised
    myCSVReader = csv.DictReader(csvfile, fieldnames=['name','ra','dec'],delimiter=",", quotechar='"')
    #myCSVReader is an instance of the class csv.DictReader
    #NOTE the delimiter argument
    #if your delimiter is ; or |, change the delimiter
    #csv.DictReader creates a dictionary
    #a dictionary is like a list, but instead of being indexed by numbers, it is indexed by keys
    #fieldnames contains the keys
    for row in myCSVReader:
        coords = SkyCoord(float(row['ra']),float(row['dec']),frame='icrs', unit='deg')
        #creates pairs of coordinates from the ra and dec columns of each row in the CSV
        #coords is an argument that is passed to the download_ptf function
        #icrs stands for Internatl Celestial Reference System
        try:
            download_ptf(coords,name=row['name'],directory=datadir)
            print("Data saved to "+datadir+row['name']+'.xml')
            #uses the download_ptf function to download data at those coords 
            #and save it to an xml file in datadir
            #where the name of the xml is the name of the star (first column) from the csv input
        except:
            #except handles any exceptions (errors) that were caught in the try block
            print("No data found at: "+coords.to_string())

