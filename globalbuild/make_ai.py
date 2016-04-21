
import arcpy as ap
from constants import *

AI_RES = 600

def main(prefix, polygons, mxd_template, map_fields, map_layer_labels, map_values, ai_res):
    ap.env.workspace = WORKSPACE
    ap.env.overwriteOutput = True
    
    mxd = ap.mapping.MapDocument(mxd_template)
    
    df = ap.mapping.ListDataFrames(mxd)[0]
    if map_layer_labels is None:
        map_layer_labels = map_fields

    if len(map_fields)!=len(map_layer_labels):
        print "ERROR: Labels != fields"
    if mxd.relativePaths == False:
        print "ERROR: RelativePaths == False"
    
    
    
    grpLyr = ap.mapping.ListLayers(mxd,"indicators")[0]
    for i in range(len(map_fields)):
        
        print "dissolving %s" % map_fields[i]
        dissolved = "dis_%s_%s" % (map_layer_labels[i], TIMESTAMP)
        
        if not ap.Exists(dissolved):
            ap.Dissolve_management(polygons,dissolved,map_fields[i])
        else:
            print "%s exists, skipping" % dissolved
    
        lyr = ap.mapping.Layer(LAYER_TEMPLATE)
        lyr.name = map_layer_labels[i]
    
        lyr.replaceDataSource(WORKSPACE, "FILEGDB_WORKSPACE", dissolved, True)
        lyr.symbology.valueField = map_fields[i]
        lyr.symbology.classValues = map_values[map_fields[i]]
        
        if grpLyr.isGroupLayer:
            ap.mapping.AddLayerToGroup(df,grpLyr,lyr)
        else:
            ap.mapping.AddLayer(df, lyr)
        
        outfile = "bin/%s%s_%s.ai"%(prefix, map_layer_labels[i],TIMESTAMP)
        print "exporting %s" % outfile
        
        ap.mapping.ExportToAI(mxd, outfile,resolution=AI_RES)
        ap.mapping.RemoveLayer(df, ap.mapping.ListLayers(mxd,lyr.name)[0])




if __name__ == '__main__':
    
    #main('dark_', GLOBAL_OUT, MXD_TEMPLATE_AI, MAP_FIELDS, MAP_LABELS, MAP_CLASSES, AI_RES)
    main('light_', GLOBAL_OUT, "aqueduct_global_for_ai2_20140214.mxd", MAP_FIELDS, MAP_LABELS, MAP_CLASSES, AI_RES)