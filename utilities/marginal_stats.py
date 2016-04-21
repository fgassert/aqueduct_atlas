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
OUTCSV = "country_marginal_stats.csv"

def main():
    print "initializing"
    ap.env.overwriteOutput = True
    ap.env.workspace = WORKSPACE
    
    ras = ["marginal_ag_land_ha",
            "favored_ag_land_ha",
            "ag_wateronly_constrained_ha",
            "ag_landonly_constrained_ha",
            "ag_both_constrained_ha"]
    lbls = ["mar_ha","fav_ha","water_ha","land_ha","both_ha"]
    
    ap.CheckOutExtension("SPATIAL")
    
    POLYS = "mena_plus"
    POLYFIELD = "name"
    
    recs = []
    for i in range(len(ras)):
        ap.sa.ZonalStatisticsAsTable(POLYS,POLYFIELD,ras[i],lbls[i],"DATA","SUM")
        recs.append(ap.da.TableToNumPyArray(lbls[i],[POLYFIELD,"SUM"]))
    
    outrecs = [recs[i]["SUM"] for i in range(len(recs))]
    outrecs.extend([recs[i][POLYFIELD] for i in range(len(recs))])
    mlab.rec2csv(np.rec.fromarrays(outrecs, names=lbls),OUTCSV)
    
    
    print "complete"


if __name__ == '__main__':
    main()