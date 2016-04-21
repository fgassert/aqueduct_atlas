import arcpy as ap
import matplotlib.mlab as mlab
import os

CWD = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/"
os.chdir(CWD)
#RUNOFF = "GLDAS2_20130901.gdb/runoff_1950"
USE = "use/U_2010.gdb/Ut"
CONS = "use/U_2010.gdb/Ct"
#POLYGONS = "WULCA/BWF.shp"
POLYGONS = "global_maps/Basins_15006-20130820.shp"
WORKSPACE = "scratch.gdb"
#ZONEFIELD = "FID_Monthl"
ZONEFIELD = "BasinID"
#SUFFIX = "tab_amb"
SUFFIX = "tab_gu2"
#RR = "runoffresample2"
#RES = 0.0083333333

def main():
    
    ap.env.workspace = WORKSPACE
    ap.env.overwriteOutput = True
    
    ap.CheckOutExtension("Spatial")
    
    #ap.Resample_management(RUNOFF,RR,RES)
    
    ras = [USE, CONS]
    #ras = [RR]
    for x in ras:
        o = os.path.basename(x)+SUFFIX
        ap.sa.ZonalStatisticsAsTable(POLYGONS, ZONEFIELD, x, o, "DATA", "SUM")
        t = ap.da.TableToNumPyArray(o,"*")
        mlab.rec2csv(t,o+".csv")

    print ("complete")
    
if __name__ == '__main__':
    main()