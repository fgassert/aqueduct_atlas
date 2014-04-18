
import arcpy as ap
import pandas as pd
import numpy as np
import sys, os

CWD = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/projections/"
os.chdir(CWD)
timestamp = 0

WORKSPACE = "aqueduct_projections_%s.gdb" % timestamp
INMXD = "empty.mxd"
OUTMXD = "aqueduct_projections.mxd"
LYR = "projections_symbology.lyr"
MASKLYR = "mask_symbology.lyr"
SHP = "shps/projection_data_20140416.shp"
OUTSHP = "aqueduct_projections"

II = ['ws','sv','ut','bt']
YY = ['20','30','40']
SS = ['24','28','38']
R = ['t','c','u']
    
def make_shp():
    """"""
    ap.env.workspace = WORKSPACE
    ap.env.overwriteOutput = True
        
    print "generating shp"
    s = ap.SpatialReference("WGS 1984 Web Mercator (Auxiliary Sphere)")
    ap.Project_management(SHP,OUTSHP,s)
    
    print "joining table"
    ap.da.ExtendTable(OUTSHP,"BasinID",rec,"BasinID")
    
    try:
        ap.AddSpatialIndex_management(OUTSHP)
    except Exception, e:
        print e
        
def make_mxd():
    mxd = ap.mapping.MapDocument(INMXD)
    df = ap.mapping.ListDataFrames(mxd)[0]
    labels = pd.read_csv()

    if mxd.relativePaths == False:
        print "ERROR: RelativePaths == False"
    
    for i in range(len(II)):
        for s in range(len(SS)):
            for y in range(len(YY)):
                for r in range(len(R)):
                    outlbll = "%s%s%s%sl" % (II[i],YY[y],SS[s],R[r])
                    lyr = ap.mapping.Layer(LYR[i][r])
                    lyr.name = outlabel
                    lyr.replaceDataSource(WORKSPACE, "FILEGDB_WORKSPACE", os.path.split(OUTSHP)[-1], True)
                    lyr.symbology.valueField = outlabel
                    lyr.symbology.classValues = labels["%s%s" % (II[i],R[r])]
                    lyr.visible = False
                    ap.mapping.AddLayer(df, lyr)
        
    print "Exporting map"
    mxd.saveACopy(OUTMXD)
    
    del mxd
    
def main():
    arr,datalbls = prep_data()
    print "saving csv"
    arr.to_csv(DUMPCSV)
    make_shp(arr)
    make_mxd(datalbls)
    
    print 'complete'
    
if __name__ == '__main__':
    main()
