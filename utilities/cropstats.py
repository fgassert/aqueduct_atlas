"""

"""

import arcpy as ap
import arcpy.sa as sa
import arcpy.da as da
import numpy as np
import matplotlib.mlab as mlab
import os

CWD = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/"
os.chdir(CWD)
WORKSPACE = "crops_m3.gdb"
POLY = "C:/Users/francis.gassert/Documents/ArcGIS/BasinDownloads20130127/aqueduct_global_dl_20130123.gdb/global_master_20130123"
OUTCSV = "cropstats.csv"
OVR = False

def main():
    print "initializing"
    ap.env.overwriteOutput = True
    ap.env.workspace = os.path.join(CWD,WORKSPACE)
    ap.CheckOutExtension("spatial")
    
    """
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
    """
    rasters = [
        "castor_yh",
        "carob_yh",
        "lemonlime_yh"
    ]
    
    
    keys = {"name":True}
    od = []
    for r in rasters:
        t = "%stab"%r
        if not ap.Exists(t) or OVR:
            sa.ZonalStatisticsAsTable(POLY,"BWS_cat",r,t,"DATA","SUM")
        a = da.TableToNumPyArray(t,["BWS_CAT","SUM"])
        
        d = {"name":r}
        for i in range(a["BWS_CAT"].shape[0]):
            d[a["BWS_CAT"][i]]=a["SUM"][i]
            keys[a["BWS_CAT"][i]]=True
        od.append(d)
    
    kl = keys.keys()
    oa = []
    for k in kl:
        l = np.array([d[k] if d.has_key(k) else 0 for d in od])
        oa.append(l)
    
    a = np.rec.fromarrays(oa,names=kl)
    print a
    mlab.rec2csv(a,OUTCSV)
    
    print "complete"



if __name__ == '__main__':
    main()