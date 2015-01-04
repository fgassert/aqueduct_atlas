
import arcpy as ap
import pandas as pd
import numpy as np
import sys, os
import make_ai

CWD = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/projections/"
os.chdir(CWD)
AI_RES = 600

WORKSPACE = "scratch.gdb" % timestamp
INMXD = "empty.mxd"

LABELS = "labels_20140416.csv"

pfx = ''
INSHP = "aqueduct_projections_20150103.gdb/aqueduct_projections.shp"
MXD = "aqueduct_global_for_ai2_20140214.mxd"

def main():

    # first render RCP85/SSP2 for BT, UT, WS, SV
    ap.env.workspace = WORKSPACE
    ap.env.overwriteOutput = True    
    
    fields = ['ws4028cl',
              'ut4028cl',
              'bt4028cl',
              'sv4028cl',
              'ut4028ul',
              'sv4028ul']
    templates = ["blue_red_7_1.lyr",
                 "blue_red_7_1.lyr",
                 "red_blue_7_1.lyr",
                 "blue_red_7_1.lyr",
                 "gray_mask.lyr",
                 "gray_mask.lyr"]
    label_headers = ['wsc',
                     'utc',
                     'btc',
                     'svc',
                     'utu',
                     'svu']
    labels = pd.read_csv(LABELS)
    
    for i in range(len(fields)]:
        l = labels[label_headers[i]].dropna()
        make_ai.render_fields(pfx, INSHP, MXD, templates[i], fields[i], fields[i], l)
    
    print 'complete'
    
if __name__ == '__main__':
    main()
