
import arcpy as ap
import os


CWD = "C:/Users/francis.gassert/Documents/ArcGIS/"
os.chdir(CWD)
WORKSPACE = "Default.gdb"

def main():
    
    ap.env.workspace = WORKSPACE
    ap.env.overwriteOutput = True
    
    shps = [
        "dissolve_BWS_cat.shp",
        "dissolve_default.shp"
    ]
    
    '''
        "dissolve_WSV_cat.shp",
        "dissolve_SV_cat.shp",
        "dissolve_HFO_cat.shp",
        "dissolve_DRO_cat.shp",
        "dissolve_STOR_cat.shp",
        "dissolve_GW_cat.shp",
        "dissolve_WRI_cat.shp",
        "dissolve_ECO_S_cat.shp",
        "dissolve_MC_cat.shp",
        "dissolve_WCG_cat.shp",
        "dissolve_ECO_V_cat.shp",
    '''
    
    for s in shps:
        s1 = "elim_%s"%s
        ap.EliminatePolygonPart_management(os.path.join(CWD,s),os.path.join(CWD,s1),"AREA", 100000000,'',"ANY")
        #s2 = "simp_%s"%s1
        #ap.SimplifyPolygon_cartography(os.path.join(CWD,s1),os.path.join(CWD,s2),"POINT_REMOVE",3000,1000,"RESOLVE_ERRORS","NO_KEEP")
        s2 = s1
        s3 = "prj_%s"%s2
        ap.Project_management(os.path.join(CWD,s2), os.path.join(CWD,s3), ap.SpatialReference("WGS 1984"))
    

if __name__ == '__main__':
    main()