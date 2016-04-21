

import arcpy as ap
import numpy as np
import matplotlib.mlab as mlab
from arcpy.sa import Raster, Con
import os
import spatial_weighted_stats as sw

CWD = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/corn/"
os.chdir(CWD)
INPUTS = "corn.gdb"
SCRATCHGDB = "scratch.gdb"
OUTCOORDS = "USA Contiguous Albers Equal Area Conic"
OUTRES = 750

RASTERFIELDS = [
    "f_irrtons",
    "f_nirrtons",
    "f_tons",
    "f_grainirrtons",
    "f_grainnirrtons",
    "f_silirrtons",
    "f_silnirrtons",
]
DISTRASTERS = {
    "f_irrtons":os.path.join(INPUTS,"irrcorn"),
    "f_nirrtons":os.path.join(INPUTS,"nonirrcorn"),
    "f_tons":os.path.join(INPUTS,"corn_aggr_750"),
    "f_grainirrtons":os.path.join(INPUTS,"irrcorn"),
    "f_grainnirrtons":os.path.join(INPUTS,"nonirrcorn"),
    "f_silirrtons":os.path.join(INPUTS,"irrcorn"),
    "f_silnirrtons":os.path.join(INPUTS,"nonirrcorn"),
}

INPUTPOLYS = os.path.join(INPUTS,"corn_20140317")
TMPPOLYS = "tmp_shps"

#OUTPOLYS = [INPUTPOLYS,os.path.join("corn_states"),None]
OUTPOLYS = [os.path.join(INPUTS,"corn_states")]
#OUTPOLYS = os.path.join(INPUTS,"corn_country")
AQUEDUCTPOLYS = "../global_maps/aqueduct_global_dl_20130123.gdb/global_master_20130123"

def make_weightrasters():
    ap.Project_management(INPUTPOLYS,TMPPOLYS,ap.SpatialReference(OUTCOORDS))
    ap.AddField_management(TMPPOLYS,"__area","DOUBLE")
    ap.AddField_management(TMPPOLYS,"__normalized","DOUBLE")
    ap.CalculateField_management(TMPPOLYS,"__area","!shape.area@kilometers!","PYTHON")
    ret = []
    for f in RASTERFIELDS:
        ap.CalculateField_management(TMPPOLYS,"__normalized","!%s!/!__area!"%f,"PYTHON")
        ap.PolygonToRaster_conversion(TMPPOLYS,"__normalized",f,cellsize=OUTRES)
        distributed = Raster(f) * Raster(DISTRASTERS[f])
        out = "d%s"%f
        distributed.save(out)
        ret.append(out)
    
    return ret

def main():
    ap.env.workspace = SCRATCHGDB
    ap.env.overwriteOutput = True
    ap.env.outputCoordinateSystem = ap.SpatialReference(OUTCOORDS)
    ap.CheckOutExtension("SPATIAL")
    
    wrs = make_weightrasters()
    
    stats = {"nan":1,"hist":[0,1,2,3,4,100]}
    
    sw.spatial_weighted_stats(AQUEDUCTPOLYS,"BWS_s",wrs,"corn",OUTPOLYS,stats,sr=ap.SpatialReference(OUTCOORDS))
    

if __name__ == '__main__':
    main()