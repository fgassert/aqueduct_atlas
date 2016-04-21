"""

"""

import numpy as np
import arcpy as ap
import matplotlib.mlab as mlab
import rtree
import fiona
import shapely
import csv

POINTS = None
POLYS = None
OUT1CSV = None
OUT2CSV = None
TMP_OUT = "in_memory/tmp"

def spatial_join(points_shp, poly_shp, outcsv):
    points = fiona.open(points_shp, 'r')
    polys = fiona.open(poly_shp,'r')
    
    shp_polys = []
    poly_ids = []
    for p in poly:
        poly_ids.append(p['attributes'][POLYIDFIELD])
        shp_polys.append(shapely.shape(p['geometry']))

    shp_points = []
    point_ids = []
    for p in points:
        point_ids.append(p['attributes'][PTIDFIELD])
        shp_pts.append(shapely.point(p['geometry']))
    
    r = [["pt_ids","poly_ids"]]
    for i in range(len(shp_polys)):
        p = shp_polys[i]
        r.append([poly_ids[i],shp_polys[filter(p.crosses,shp_pts)]])
    
    f = open(outcsv,'r')
    c = csv.writer(f)
    c.writerows(r)
    
    f.close()

def py_spatial_join(points_shp, poly_shp, outcsv):
    ap.identity(points_shp, poly_shp, TMP_OUT)
    out = ap.da.FeatureToNumPyArray(TMP_OUT,"*")
    mlab.rec2csv(out,outcsv)

if __name__ == "__main__":
    spatial_join(POINTS,POLYS,OUT1CSV)
    py_spatial_join(POINTS,POLYS,OUT2CSV)
