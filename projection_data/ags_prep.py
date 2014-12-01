
import arcpy as ap
import pandas as pd
import numpy as np
import sys, os

CWD = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/projections/"
os.chdir(CWD)
timestamp = 20141201

WORKSPACE = "aqueduct_projections_%s.gdb" % timestamp
INMXD = "empty.mxd"
OUTMXD = "aqueduct_projections.mxd"
LYRS = [
        ["aqueduct_7.lyr","blue_red_7_1.lyr","gray_mask.lyr"],
        ["aqueduct_6.lyr","blue_red_7_1.lyr","gray_mask.lyr"],
        ["aqueduct_blue_8_1.lyr","red_blue_7_1.lyr","gray_mask.lyr"],
        ["aqueduct_6.lyr","blue_red_7_1.lyr","gray_mask.lyr"],
       ]

SHP = "projection_data_20141201.shp"
LAKES = "inputs.gdb/ne_10m_majorlakes_20121116"
TMP = "in_memory/tmp"
OUTSHP = "aqueduct_projections"

II = ['ws','ut','bt','sv']
YY = ['20','30','40']
SS = ['24','28','38']
R = ['t','c','u']
LABELS = "labels_20140416.csv"
    
def make_shp():
    """"""
    if not ap.Exists(WORKSPACE):
        ap.CreateFileGDB_management(".",WORKSPACE)
    ap.env.workspace = WORKSPACE
    ap.env.overwriteOutput = True
        
    print "generating shp"
    s = ap.SpatialReference("WGS 1984 Web Mercator (Auxiliary Sphere)")
    ap.Erase_analysis(SHP, LAKES, TMP)
    ap.Project_management(TMP,OUTSHP,s)
    
    try:
        ap.AddSpatialIndex_management(OUTSHP)
    except Exception, e:
        print e
        
def make_mxd():
    mxd = ap.mapping.MapDocument(INMXD)
    df = ap.mapping.ListDataFrames(mxd)[0]
    labels = pd.read_csv(LABELS)

    if mxd.relativePaths == False:
        print "ERROR: RelativePaths == False"
    
    for i in range(len(II)):
        for y in range(len(YY)):
            for s in range(len(SS)):
                for r in range(len(R)):
                    outlbll = "%s%s%s%sl" % (II[i],YY[y],SS[s],R[r])
                    lyr = ap.mapping.Layer(LYRS[i][r])
                    lyr.name = outlbll
                    lyr.replaceDataSource(WORKSPACE, "FILEGDB_WORKSPACE", os.path.split(OUTSHP)[-1], True)
                    lyr.symbology.valueField = outlbll
                    lyr.symbology.classValues = labels["%s%s" % (II[i],R[r])].dropna()
                    lyr.visible = False
                    ap.mapping.AddLayer(df, lyr)
        
    print "Exporting map"
    mxd.saveACopy(OUTMXD)
    
    del mxd
    
def main():
    make_shp()
    make_mxd()
    
    print 'complete'
    
if __name__ == '__main__':
    main()
