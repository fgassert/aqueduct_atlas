"""
"""

import arcpy as ap
import matplotlib.mlab as mlab
import os

from constants import *

TMP_OUT = os.path.join(WORKSPACE,"project_basins_tmp")
TMP_OUT2 = "in_memory/tmp2"

def main():
    print "initializing"
    
    ap.env.overwriteOutput = True
    
    #"World_Cylindrical_Equal_Area"
    sr = ap.SpatialReference(54034) 
    ap.Project_management(BASINPOLY, TMP_OUT, sr)
    ap.CalculateAreas_stats(TMP_OUT,TMP_OUT2)
    out = ap.da.FeatureClassToNumPyArray(TMP_OUT2,[BASIN_ID_FIELD,"F_AREA"])
    mlab.rec2csv(out,AREACSV)
    
    print "complete"



if __name__ == '__main__':
    main()