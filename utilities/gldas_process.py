import arcpy as ap
import os

WORKSPACE = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/gldas/GLDAS_NOAH10_M.020-20121211-filled"
OUTFILE = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/GLDAS2_20130901.gdb/runoff"
AREAGRID = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/GLDAS2_20130901.gdb/a1deg_m"
SYR = 1948
EYR = 2011

def main():
    ap.env.workspace = WORKSPACE
    ap.env.overwriteOutput = True
    
    ap.CheckOutExtension("Spatial")
    yr = []
    areagrid = ap.sa.Raster(AREAGRID)
    for y in range(SYR,EYR):
        mr = [os.path.join(WORKSPACE,"runoff_%04d%02d_m-filled.img" % (y,m+1)) for m in range(12)]
        mr_tab = [[r,"VALUE",1] for r in mr]
        o = ap.sa.WeightedSum(mr_tab)
        v = o * areagrid
        v.save("%s_%s" % (OUTFILE, y))
        yr.append(v)
    yr_tab = [[r,"VALUE",1.0/(EYR-SYR)] for r in yr]
    o = ap.sa.WeightedSum(yr_tab)
    o.save(OUTFILE)

if __name__ == "__main__":
    main()

#arcpy.Resample_management("GISSync/GLDAS2_20130901.gdb/runoff","GISSync/GLDAS2_20130901.gdb/runoff_Resample1",0.00833333333,"NEAREST")