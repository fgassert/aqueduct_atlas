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
  
    
    rasters = [
        "gmia_v5_aei_ha",
        "cropland_ha",
        "coffee_yh",
        "cocoa_yh",
        "sugarcane_yh",
        "orange_yh",
        "maize_yh",
        "maizefor_yh",
        "wheat_yh",
        "soybean_yh",
        "cotton_yh",
        "oats_yh",
        "rice_yh",
        "oilpalm_yh",
        "rapeseed_yh",
        "rubber_yh",
        "G_Cereals_yh",
        "G_Fiber_yh",
        "G_Forage_yh",
        "G_Fruit_yh",
        "G_Oilcrops_yh",
        "G_Pulses_yh",
        "G_RootsTubers_yh",
        "G_SugarCrops_yh",
        "G_Treenuts_yh"]
    
    #rasters = ap.ListRasters()
    
    sr = ap.SpatialReference(3857) 
    for r in rasters:
        o = "%s%s.tif" % (OUTDIR,os.path.basename(r))
        tmp = "tmp"
        print "projecting %s : %s" % (r, o)
        ap.ProjectRaster_management(r,o,sr,in_coor_system=4326)
        
    print "complete"



if __name__ == '__main__':
    main()