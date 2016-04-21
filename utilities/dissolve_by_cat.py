
import arcpy as ap
import os


CWD = "C:/Users/francis.gassert/Documents/ArcGIS/"
os.chdir(CWD)
WORKSPACE = "Default.gdb"
IN_FEATURES = "BasinDownloads20130127/aqueduct_global_dl_20130123.gdb/global_master_20130123"

def main():
    
    ap.env.workspace = WORKSPACE
    ap.env.overwriteOutput = True
    
    cat_fields = [
        "BWS_cat",
        "WSV_cat",
        "SV_cat",
        "HFO_cat",
        "DRO_cat",
        "STOR_cat",
        "GW_cat",
        "WRI_cat",
        "ECO_S_cat",
        "MC_cat",
        "WCG_cat",
        "ECO_V_cat"
    ]
    
    for c in cat_fields:
        ap.Dissolve_management(IN_FEATURES,os.path.join(CWD,"dissolve_%s.shp" % c), c)

def get_default():
    
    ap.env.workspace = WORKSPACE
    ap.env.overwriteOutput = True
    
    ap.CopyFeatures_management(IN_FEATURES,'tmp')
    ap.AddField_management('tmp','default_cat')
    ap.CalculateField_management('tmp','default_cat','min(4,int(!DEFAULT!))',"PYTHON")
    ap.Dissolve_management('tmp',os.path.join(CWD,"dissolve_default.shp"), 'default_cat')
    

if __name__ == '__main__':
    get_default()
    #main()