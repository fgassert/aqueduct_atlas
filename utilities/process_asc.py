'''
Created on Aug 28, 2013

@author: francis.gassert
'''

import arcpy as ap
import numpy as np
import matplotlib.mlab as mlab
import os
import cProfile,pstats
from zipfile import ZipFile

CWD = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/"
os.chdir(CWD)
WORKSPACE = "crops_m3.gdb"
TMPASC = "tmp.asc"
ASCZIPDIR = "asc/"
UNZIPDIR = "tmp/"

def main():
    print "initializing"
    ap.env.overwriteOutput = True
    ap.env.workspace = WORKSPACE
    
    
    dirlist = os.listdir(ASCZIPDIR)
    print dirlist
    
    for z in dirlist:
        if z[-8:]==".asc.zip":
            zf = ZipFile("%s%s" % (ASCZIPDIR,z))
            z0=zf.namelist()[0]
            print "extracting %s" % z0
            zf.extract(z0,UNZIPDIR)
            
    dirlist = os.listdir(UNZIPDIR)
    print dirlist
    
    for z in dirlist:
        if z[-4:]==".asc":
            targetfile = "%s%s/%s" % (CWD, WORKSPACE, z.split('.')[0])
            srcfile = "%s%s%s" % (CWD,UNZIPDIR,z)
            print "converting %s - %s" % (srcfile, targetfile)
            if not ap.Exists(targetfile):
                ap.ASCIIToRaster_conversion(srcfile, targetfile, "FLOAT")
                ap.DefineProjection_management(targetfile, ap.SpatialReference("WGS 1984"))
            else:
                print "%s exists" % targetfile
            
    print "complete"


if __name__ == '__main__':
    cProfile.run("main()",'profilelog')
    p=pstats.Stats('profilelog')
    p.strip_dirs().sort_stats('cum').print_stats()
    