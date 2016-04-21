'''
Created on Nov 15, 2012

@author: francis.gassert
'''

import matplotlib.mlab as mlab
import numpy as np
import os
import arcpy as ap
from constants import *

TMP_BASINS = "in_memory/tmp"

def main():
    
    basins = mlab.csv2rec(BASINCSV)
    dwnbasin = basins["dwnbasinid"].astype(np.long)
    basinid = basins["basinid"].astype(np.long)
    dwnbasin[dwnbasin==0]=basinid[dwnbasin==0]
    
    numbasins = np.max(basinid)
    dbid = np.zeros(numbasins+1, dtype=np.long)
    dbid[basinid] = dwnbasin
    
    olddbid = dbid.copy()
    dbid1 = dbid.copy()
    dbid = dbid[dbid]
    while np.sum(olddbid!=dbid):
        olddbid = dbid.copy()
        dbid = dbid[dbid]
    
    outrec = np.rec.fromarrays([np.arange(0,numbasins+1),dbid,dbid1], names=("BasinID","bigbasin","dbid"))
    mlab.rec2csv(outrec,"big_basins.csv")
    
    ap.CopyFeatures_management(RAWBASINS, BIGBASINS)
    ap.da.ExtendTable(BIGBASINS, BASIN_ID_FIELD, outrec, BASIN_ID_FIELD)
    

if __name__ == '__main__':
    main()