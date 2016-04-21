'''
Created on Nov 16, 2012

@author: francis.gassert
'''

import arcpy as ap
import numpy as np
import matplotlib.mlab as mlab
import os
from constants import *

CLASSES = "global_inputs.gdb/grdc_basins_wfn"
OUTTAB = "in_memory/tab_basin_areas"
TMPBASINS = "in_memory/tmp"
MIN_OVERLAP = 80
BIGBASIN_FIELD = 'bigbasin'


def make_bigbasins():
    basins = mlab.csv2rec(BASINCSV)
    dwnbasin = basins["dwnbasinid"].astype(np.long)
    basinid = basins["basinid"].astype(np.long)
    dwnbasin[dwnbasin==0]=basinid[dwnbasin==0]
    
    numbasins = np.max(basinid)
    dbid = np.zeros(numbasins+1, dtype=np.long)
    dbid[basinid] = dwnbasin
    
    olddbid = dbid.copy()
    dbid = dbid[dbid]
    while np.sum(olddbid!=dbid):
        olddbid = dbid.copy()
        dbid = dbid[dbid]
    
    outrec = np.rec.fromarrays([np.arange(0,numbasins+1),dbid], names=("BasinID",BIGBASIN_FIELD))
    mlab.rec2csv(outrec,"big_basins.csv")
    
    ap.CopyFeatures_management(RAWBASINS, TMPBASINS)
    ap.da.ExtendTable(TMPBASINS, BASIN_ID_FIELD, outrec, BASIN_ID_FIELD)

def main():
    print "initializing"
    ap.env.overwriteOutput = True
    ap.env.workspace = WORKSPACE
    
    make_bigbasins()
    
    print "intersecting"
    ap.TabulateIntersection_analysis(TMPBASINS,BIGBASIN_FIELD,CLASSES,OUTTAB,"DRAINAGE",None,0)
    
    print "copying"
    ap.CopyFeatures_management(TMPBASINS,BASINPOLY)
    
    print "joining"
    arr = ap.da.TableToNumPyArray(OUTTAB,"*")
    fi = arr["PERCENTAGE"]>MIN_OVERLAP
    join_array = np.rec.fromarrays((arr[BIGBASIN_FIELD][fi],arr["DRAINAGE"][fi]),names=(BIGBASIN_FIELD,BASIN_NAME_FIELD))
    
    ap.da.ExtendTable(BASINPOLY,BIGBASIN_FIELD,join_array,BIGBASIN_FIELD)
    print "dropping fields"
    ap.DeleteField_management(BASINPOLY, [BIGBASIN_FIELD,"dwnBasinId"])
    
    print "complete"


if __name__ == '__main__':
    main()
