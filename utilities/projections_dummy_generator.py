
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
SHP = "inputs.gdb/Basins_15006"
OUTSHP = "aqueduct_projections"

BACSV = "Ba-20140303.csv"
BTCSV = "projections-bt-20140121.csv"
DUMPCSV = "prepped.csv"

II = ['ws','sv','ut','bt']
csvII = ['WWR_ch_','Ba_ch_','Ut_ch_','Bt_ch_']
YY = ['20','30','40']
csvYY = ['2020_','2030_','2040_']
SS = ['24','28','38']
csvSS = ['RCP45_SSP2','RCP85_SSP2','RCP85_SSP3']
R = ['w','a','d']

thresholds = (2**(np.arange(10)/4.0-1.125))[:,np.newaxis]
thresholds[9] = 100 #hack inf filter

category_lbls = np.array(
                    ['No data',
                    '2x or greater decrease',
                    '1.7x decrease',
                    '1.4x decrease',
                    '1.2x decrease',
                    'near normal',
                    '1.2x increase',
                    '1.4x increase',
                    '1.7x increase',
                    '2x or greater increase',
                    'No data'
                 ])

LYR_VALUES = ['2x or greater decrease',
                    '1.7x decrease',
                    '1.4x decrease',
                    '1.2x decrease',
                    'near normal',
                    '1.2x increase',
                    '1.4x increase',
                    '1.7x increase',
                    '2x or greater increase',
                    'No data'
                 ]

def score(vec):
    """"""
    #print vec.as_matrix(), thresholds
    return category_lbls[np.sum(vec.as_matrix() > thresholds,0)]
    
def mask():
    return (np.arange(15006)//5002)*.5

def prep_data():
    """"""
    BAdf = pd.read_csv(BACSV)
    BTdf = pd.read_csv(BTCSV)
    BAdf = BAdf.set_index('BasinID')
    BTdf = BTdf.set_index('BasinID')
    for y in csvYY:
        for s in ('RCP45','RCP85'):
            BTdf["%s%s%s" % (csvII[3],y,s)] = BTdf["Bt_%s%s" % (y,s)] / BTdf["Bt_2005_%s" % (s)]
    
    df = BAdf.join(BTdf)
    
    outdf = pd.DataFrame()
    outdf['_id'] = df.index
    outdf = outdf.set_index('_id')
    outdf["BasinID"] = df.index
    #print outdf
    datalbls = []
    for i in range(4):
        for y in range(3):
            for s in range(3):
                for r in range (3):
                    inlbl = "%s%s%s" % (csvII[i],csvYY[y],csvSS[s])
                    if i == 3:
                        inlbl = inlbl[:-5]
                    outlblr = "%s%s%s%sr" % (II[i],YY[y],SS[s],R[r])
                    outlbll = "%s%s%s%sl" % (II[i],YY[y],SS[s],R[r])
                    datalbls.append(outlbll)
                    outdf[outlblr] = df[inlbl]
                    outdf[outlbll] = score(outdf[outlblr])
        
    for s in range(3):
        outdf["u%s" % SS[s]] = mask()
    
    return outdf, datalbls
    
def make_shp(arr):
    """"""
    ap.env.workspace = WORKSPACE
    ap.env.overwriteOutput = True
    
    rec_dtypes = []
    # coerce objects to strings
    for n,d in zip(arr.columns,arr.dtypes):
        if not (np.issubdtype(d,'f') or np.issubdtype(d,'i')):
            d = np.dtype('S32')
        rec_dtypes.append((n,d))
    rec = np.rec.fromarrays([arr[x] for x in arr.columns],dtype=rec_dtypes)
    
    print "generating shp"
    s = ap.SpatialReference("WGS 1984 Web Mercator (Auxiliary Sphere)")
    ap.Project_management(SHP,OUTSHP,s)
    
    print "joining table"
    ap.da.ExtendTable(OUTSHP,"BasinID",rec,"BasinID")
    
    try:
        ap.AddSpatialIndex_management(OUTSHP)
        ap.AddIndex_management(OUTSHP,["u%s"%s for s in SS],"masks","NON_UNIQUE")
    except Exception, e:
        print e
        
def make_mxd(datalbls):
    mxd = ap.mapping.MapDocument(INMXD)
    df = ap.mapping.ListDataFrames(mxd)[0]

    if mxd.relativePaths == False:
        print "ERROR: RelativePaths == False"
    
    
    for i in range(len(datalbls)):
        lyr = ap.mapping.Layer(LYR)
        lyr.name = datalbls[i]
        lyr.replaceDataSource(WORKSPACE, "FILEGDB_WORKSPACE", os.path.split(OUTSHP)[-1], True)
        lyr.symbology.valueField = datalbls[i]
        lyr.symbology.classValues = LYR_VALUES
        lyr.visible = False
        ap.mapping.AddLayer(df, lyr)
    
    for i in range(len(SS)):
        name = "u%s" % SS[i]
        lyr = ap.mapping.Layer(MASKLYR)
        lyr.name = name
        lyr.replaceDataSource(WORKSPACE, "FILEGDB_WORKSPACE", os.path.split(OUTSHP)[-1], True)
        lyr.symbology.valueField = name
        lyr.symbology.classValues = [0,0.5]
        lyr.visible = False
        ap.mapping.AddLayer(df, lyr, "BOTTOM")
    
        
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