"""

"""

import arcpy as ap
import numpy as np
import matplotlib.mlab as mlab
import os

CWD = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/"
os.chdir(CWD)
WORKSPACE = "country_aggr.gdb"
OUTCSV = "out.csv"

"""
INCSV = "aggr_country_20131022.csv"
JOIN_FIELD_CSV = 'OBJECTID'
JOIN_FIELD_SHP = "OBJECTID"
INFEATURES = "country_cleaned_20130819"
OUTFEATURES = "country_20131022"
OUTCSV = "country_out_20131022.csv"
"""
"""
INCSV = "aggr_basins_pop_20131022.csv"
JOIN_FIELD_CSV = 'OBJECTID_1'
JOIN_FIELD_SHP = "OBJECTID_1"
INFEATURES = "basins_fekete_pop100_names"
OUTFEATURES = "basins_pop_20131022"
OUTCSV = "basins_pop_out_20131022.csv"
"""
"""
INCSV = "aggr_basins_area_20131022.csv"
JOIN_FIELD_CSV = 'OBJECTID'
JOIN_FIELD_SHP = "OBJECTID"
INFEATURES = "basins_fekete_area100_names"
OUTFEATURES = "basins_area_20131022"
OUTCSV = "basins_area_out_20131022.csv"
"""

INCSV = "aggr_basins_area_20131022.csv"
JOIN_FIELD_CSV = 'OBJECTID'
JOIN_FIELD_SHP = "OBJECTID"
INFEATURES = "basins_fekete_area100_names"
OUTFEATURES = "basins_area_20131022"
OUTCSV = "basins_area_out_20131022.csv"
def main():
    print "initializing"
    ap.env.overwriteOutput = True
    ap.env.workspace = WORKSPACE
  
    print "copying"
    ap.CopyFeatures_management(INFEATURES,OUTFEATURES)
    
    print "joining"
    arr = mlab.csv2rec(INCSV)
    
    ap.da.ExtendTable(OUTFEATURES,JOIN_FIELD_SHP,arr,JOIN_FIELD_CSV)
    
    print "saving"
    arr = ap.da.TableToNumPyArray(OUTFEATURES,"*")
    mlab.rec2csv(arr,OUTCSV)
    
    print "complete"



if __name__ == '__main__':
    main()