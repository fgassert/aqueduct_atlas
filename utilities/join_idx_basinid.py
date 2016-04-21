import arcpy as ap
import numpy as np
import pandas as pd
import sys, os


CWD = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/projections/"
os.chdir(CWD)


WORKSPACE = "scratch.gdb"
SHP = "inputs.gdb/Basins_15006"

CSVDIR = "join_csvs"
BASINID = "BasinID"



def main():
    ap.env.overwriteOutput = True
    ap.env.workspace = WORKSPACE
    
    csvs = [c for c in os.listdir(CSVDIR) if os.path.splitext(c)[1]==".csv"]
    
    for f in csvs:
        df = pd.read_csv(os.path.join(CSVDIR,f))
        df.index += 1
        df.columns = ['y%s'%y if y[0].isdigit() else y for y in df.columns ]
        df=df.drop('Unnamed: 0',1)
        out = os.path.basename(f)[:-4]
        ap.CopyFeatures_management(SHP,out)
        ap.da.ExtendTable(out,BASINID,df.to_records(),'index')

if __name__ == '__main__':
    main()