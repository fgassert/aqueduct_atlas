"""

"""

import arcpy as ap
import numpy as np
import matplotlib.mlab as mlab
import os

CWD = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/"
os.chdir(CWD)
WORKSPACE = "crops_m3.gdb"
OUTDIR = "geotiff/"

def main():
    print "initializing"
    ap.env.overwriteOutput = True
    ap.env.workspace = os.path.join(CWD,WORKSPACE)
    ap.CheckOutExtension("spatial")
    '''
    crops = ["coffee",
        "cocoa",
        "sugarcane",
        "orange",
        "maize",
        "maizefor",
        "wheat",
        "soybean",
        "cotton",
        "oats",
        "rice",
        "oilpalm",
        "rapeseed",
        "rubber",
        "G_Cereals",
        "G_Fiber",
        "G_Forage",
        "G_Fruit",
        "G_Oilcrops",
        "G_Pulses",
        "G_RootsTubers",
        "G_SugarCrops",
        "G_Treenuts"]
    '''
    
    crops = [
        "castor",
        "carob",
        "lemonlime"
    ]
    
    
    #rasters = ap.ListRasters()
    
    for c in crops:
        if not ap.Exists("%s_yh"%c):
            print "Generating %s_yh" %c
            t = ap.sa.Raster("%s_yield"%c) * ap.sa.Raster("%s_harea"%c) * ap.sa.Raster("cellarea_ha")
            t.save("%s_yh"%c)
        else:
            print "%s_yh Exists"%c 
        
    print "complete"



if __name__ == '__main__':
    main()