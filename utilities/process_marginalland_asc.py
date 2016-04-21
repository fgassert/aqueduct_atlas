'''
Created on Aug 28, 2013

@author: francis.gassert
'''

import arcpy as ap
import numpy as np
import matplotlib.mlab as mlab
import os

CWD = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/marginal_lands"
os.chdir(CWD)
WORKSPACE = "marginal_land_inputs.gdb"
ASCDIR = "asc/"

def main():
    print "initializing"
    ap.env.overwriteOutput = True
    ap.env.workspace = WORKSPACE
    
            
    dirlist = os.listdir(ASCDIR)
    print dirlist
    
    for z in dirlist:
        if z[-4:]==".asc":
            targetfile = os.path.join(CWD, WORKSPACE, z.split('.')[0])
            srcfile = os.path.join(CWD,ASCDIR,z)
            print "converting %s - %s" % (srcfile, targetfile)
            if not ap.Exists(targetfile):
                ap.ASCIIToRaster_conversion(srcfile, targetfile, "FLOAT")
                ap.DefineProjection_management(targetfile, ap.SpatialReference("WGS 1984"))
            else:
                print "%s exists" % targetfile
            
    print "complete"


if __name__ == '__main__':
    main()