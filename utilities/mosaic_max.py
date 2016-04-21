'''
Created on Aug 28, 2013

@author: francis.gassert
'''

import arcpy as ap
import numpy as np
import matplotlib.mlab as mlab
import os

CWD = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/corn/"
os.chdir(CWD)
WORKSPACE = "corn.gdb"
TIFDIR = "out/"
AGGRDIR = "aggr/"
factor = 10

out = 'corn'

def main():
    print "initializing"
    ap.env.overwriteOutput = True
    ap.env.workspace = WORKSPACE
    
            
    dirlist = os.listdir(TIFDIR)
    
    tifs = [z for z in dirlist if z[-4:]==".tif"]
    print tifs
    mtifs = [os.path.join(TIFDIR,t) for t in tifs]
    
    if 0:
        ap.CheckOutExtension("SPATIAL")
        for t in tifs:
            aggr = ap.sa.Aggregate(os.path.join(TIFDIR,t),factor)
            aggr.save(os.path.join(AGGRDIR,t))
        mtifs = [os.path.join(AGGRDIR,t) for t in tifs]
    
    
    ap.MosaicToNewRaster_management(mtifs,os.path.join(CWD,WORKSPACE),out,number_of_bands=1,mosaic_method="MAXIMUM")
    
    print "complete"


if __name__ == '__main__':
    main()