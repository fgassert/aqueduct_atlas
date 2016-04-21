'''
Geodatabase builder for web export

Takes master table and shapefile as input and generates a gdb, mxd, and msd for web export.
Uses WGS84 Web Mercator (Aux) projection, Hollow symbology, and ArcGIS Online/Bing/Google scale range

Created on Dec 21, 2011

@author: Francis.Gassert

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/.
'''

import arcpy as ap
import csv
import os
import publishsd

###############################################################################
# 1. Working folder
BASEPATH = "C:/Users/francis.gassert/Desktop/export"
#BASEPATH = "C:/arcgisstaging"

#########
#timestamp = "20120904"
timestamp = "20121221"

#########
# 2,3,4. List of 3-tuples containing (<csv data table>, <shapefile>, <feacture class name>)
#
# As of 2/14/12:
# 0 : MDB
# 1 : CRB
# 2 : YRB
# 3 : ORB
#
DATASETS = []
DATASETS.append(("YRB_%s.csv" % timestamp,r"M:\Working\Aqueduct\Yellow River Basin (YRB)\Basin Boundaries\Yellow_GU_HU_2km.shp","YellowRiverBasinStudy%s" % timestamp))
DATASETS.append(("ORB_%s.csv" % timestamp,r"M:\Working\Aqueduct\Orange River Basin (ORB)\Basin Boundaries\hzones_admin_01_121311.shp","OrangeRiverBasinStudy%s" % timestamp))
DATASETS.append(("YZB_%s.csv" % timestamp,r"M:\Working\Aqueduct\Yangtze River Basin (YZR)\Basin Boundaries\Yangtze_GU_5km_tolerance.shp","YangtzeRiverBasinStudy%s" % timestamp))
DATASETS.append(("MKB_%s.csv" % timestamp,r"M:\Working\Aqueduct\Mekong River Basin (MKR)\Basin Boundaries\MekongGU_20121206.shp","MekongRiverBasinStudy%s" % timestamp))
DATASETS.append(("CRB_%s.csv" % timestamp,r"M:\Working\Aqueduct\Colorado River Basin (CRB)\Basin Boundaries\CRB_GU_20120221.shp","ColoradoRiverBasinStudy%s" % timestamp))
#DATASETS.append(("global_demo_%s.csv" % timestamp,r"C:/Users/francis.gassert/Documents/ArcGIS/global_workspace.gdb/global_GU_20120904","global_test_%s" % timestamp))
DATASETS.reverse()
# Last in gets top ID 

OUTNAME = "ColoradoRiverBasinStudy%s" % timestamp
# 5. output database name <*.gdb>
OUTDB = OUTNAME + ".gdb"
# 6. mxd and msd names
MXDNAME = OUTNAME + ".mxd"
SDDRAFT = OUTNAME + ".sddraft"
SDNAME = OUTNAME + ".sd"

# Join field names for shapefile and table. Both should be "GU"
JOIN_FIELD_SHAPEFILE = "GU"
JOIN_FIELD_JOINTABLE = "GU"

# Set to False to update an existing feature class without regenerating fields
# default = True
REGENERATE_FEATURES = True

# list of all fields that should be included
#ALLFIELDS = ["GU","REGION","COUNTRY","BASIN_ID","BWS_s","WSV_s","RF_s","SV_s","HFO_s","DRO_s","IEP_s","IWPro_s","NIA_s","WPG_s","STOR_s","WRI_s","BOD_s","COD_s","DO_s","TSS_s","TDS_s","NH3N_s","PO4P_s","EC_s","TP_s","IND_PR_s","IWPrice_s","UW_s","GDP_s","EFM_s","II_s","MSC_s","MC_s","WCG_s","GW_s","ECO_S_s","ECO_V_s","BWS","WSV","RF","SV","HFO","DRO","IEP","IWPro","NIA","WPG","STOR","WRI","BOD","COD","DO","TSS","TDS","NH3N","PO4P","EC","TP","IND_PR","IWPrice","UW","GDP","EFM","II","MSC","MC","WCG","GW","ECO_S","ECO_V","Ba","Bt","WITHDRAWAL","CATCHMENT"]
ALLFIELDS = ["GU","REGION","COUNTRY","BASIN_ID","BWS_s","WSV_s","SV_s","HFO_s","DRO_s","STOR_s","WRI_s","BOD_s","COD_s","DO_s","TDS_s","NH3N_s","PO4P_s","EC_s","ECO_S_s","MC_s","WCG_s","ECO_V_s","BWS","WSV","SV","HFO","DRO","STOR","WRI","BOD","COD","DO","TDS","NH3N","PO4P","EC","ECO_S","MC","WCG","ECO_V","BA","BT","WITHDRAWAL","CATCHMENT"]


# map server connection file (.ags)
SERVICE_CON = '23_21_100_32.ags'
REGISTERED_FOLDER = "C:/arcgisstaging/"
FORCE_MANUAL_UPLOAD = True
# map server folder location
SERVER_FOLDER = 'Aqueduct'
# Publish service (default = false)
PREPARE_SD = False 
PUBLISH = False
START = False

###############################################################################
# Templates for .mxd (with correct scales), hollow symbolized layer, and projection
DEFAULTMXDNAME = "blank_export.mxd"
HOLLOWLYRNAME = "hollow.lyr"
PRJNAME = "WGS 1984.prj"
###############################################################################


def opencsv(csvfilename):
    outtable = []
    csvfile = open(csvfilename, "rb")
    #dialect = csv.Sniffer().sniff(csvfile.read(1024))
    #csvfile.seek(0)
    reader = csv.reader(csvfile, delimiter=',',quotechar = '"')
    for row in reader:
        outtable.append(row)
    csvfile.close()
    return outtable

def main():
    print "initializing arcpy"
    ap.env.overwriteOutput = True
    ap.env.workspace = BASEPATH
    
    print "initializing map"
    blanktemplate = ap.mapping.MapDocument(os.path.join(BASEPATH, DEFAULTMXDNAME))
    blanktemplate.saveACopy(MXDNAME)
    del blanktemplate
    
    mxd = ap.mapping.MapDocument(os.path.join(BASEPATH,MXDNAME))
    if mxd.relativePaths == False:
        print "ERROR: RelativePaths == False"
        raise Exception()
    
    df = ap.mapping.ListDataFrames(mxd)[0]
    df.SpatialReference = ap.SpatialReference(PRJNAME)
    
    if not ap.Exists(os.path.join(BASEPATH, OUTDB)):
        print "generating new geodatabase"
        ap.CreateFileGDB_management(BASEPATH, OUTDB)
    else:
        print "geodatabase already exists"
    
    print "initializing features"
    ap.env.workspace = os.path.join(BASEPATH, OUTDB)
    
    #make each feature
    for incsv, shapefile, featurename in DATASETS:
        makefeature(df, incsv, shapefile, featurename)

    mxd.save()
    del mxd
    if PREPARE_SD:
        publishsd.publishsd(BASEPATH, MXDNAME, OUTDB, OUTNAME, SERVICE_CON, SERVER_FOLDER, FORCE_MANUAL_UPLOAD, REGISTERED_FOLDER, PUBLISH, START)
    
    print "complete"
    

def makefeature(df, in_csv, baseshapefile, featurename):
    print "loading csv %s" % in_csv
    try:
        datatable = opencsv(os.path.join(BASEPATH,in_csv))
    except:
        datatable = opencsv(os.path.join(in_csv))
    
    varnames = datatable[0]
    
    ##########
    #check varnames
    missingfields = ALLFIELDS[:]
    for field in ALLFIELDS:
        for var in varnames:
            if var == field:
                missingfields.remove(field)
                break
    if len(missingfields) > 0:
        print "WARNING: the following variables were not found:", missingfields
    
    
    ##########
    genfeature = REGENERATE_FEATURES
    if not (genfeature):
        if not ap.Exists(featurename):
            print "WARNING: Feature class does not exist: %s" % featurename
            genfeature = True
        else:
            for i in range(len(varnames)):
                if varnames[i] == JOIN_FIELD_JOINTABLE:
                    join_id = i
    if (genfeature):
    ##########
        #ap.CopyFeatures_management(baseshapefile, featurename)
        ap.Project_management(baseshapefile, featurename, PRJNAME)
            
        print "purging fields"
        drop = [f.baseName for f in ap.ListFields(featurename) if not(f.required) and not(f.baseName==JOIN_FIELD_SHAPEFILE)]
        ap.DeleteField_management(featurename,drop)
            
        #FIX: 10.1
        print "adding fields..."
        for i in range(len(varnames)):
            print varnames[i]
            if varnames[i] == JOIN_FIELD_JOINTABLE:
                join_id = i
            elif varnames[i] in ["REGION","COUNTRY","BASIN_ID","CATCHMENT"]:
                ap.AddField_management(featurename, varnames[i], "text")    
            elif varnames[i] != "":
                ap.AddField_management(featurename, varnames[i], "double")
        for i in range(len(missingfields)):
            pass
            #ap.AddField_management(featurename, missingfields[i], "double")
    ##########
    
    #FIX 10.1
    print "joining"
    datadict = {}
    for row in datatable[1:]:
        if row[0]!='':
            if datadict.has_key(row[join_id]):
                print "ERROR: duplicate join IDs"
                raise Exception()
            else:
                for i in range(len(row)):
                    if row[i] == "":
                        row[i] = None
                datadict[int(row[join_id])] = dict([(varnames[i],row[i]) for i in range(len(varnames)) if varnames[i] !=""])
    
    print "populating fields"
    updater = ap.UpdateCursor(featurename)
    for row in updater:
        i = int(row.getValue(JOIN_FIELD_SHAPEFILE))
        for key, value in datadict[i].iteritems():
            if value is None or value == "":
                row.setNull(key)
            else:
                if key not in ["REGION","COUNTRY","BASIN_ID"]:
                    value = float(value)
                row.setValue(key,value)
        updater.updateRow(row)
    del row
    del updater
    
    print "symbolizing layer"
    shapelayer = ap.mapping.Layer(HOLLOWLYRNAME)
    shapelayer.replaceDataSource(os.path.join(BASEPATH, OUTDB), "FILEGDB_WORKSPACE", featurename, True)
    shapelayer.name = featurename
    ap.mapping.AddLayer(df, shapelayer, "TOP")
    df.extent = shapelayer.getExtent()
    
if __name__ == '__main__':
    main()