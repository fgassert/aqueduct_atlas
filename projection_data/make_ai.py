
import arcpy as ap

AI_RES = 600

def render_fields(prefix, polygons, mxd_template, layer_template, map_fields, map_layer_labels, map_values, ai_res=AI_RES):
    
    mxd = ap.mapping.MapDocument(mxd_template)
    
    df = ap.mapping.ListDataFrames(mxd)[0]
    if map_layer_labels is None:
        map_layer_labels = map_fields

    if len(map_fields)!=len(map_layer_labels):
        print "ERROR: Labels != fields"
    if mxd.relativePaths == False:
        print "ERROR: RelativePaths == False"
    
    
    if type(map_fields) == str:
        map_fields = [map_fields]

    grpLyr = ap.mapping.ListLayers(mxd,"indicators")[0]
    for i in range(len(map_fields)):
        
        print "dissolving %s" % map_fields[i]
        dissolved = "dis_%s_%s" % (map_layer_labels[i])
        
        if not ap.Exists(dissolved):
            ap.Dissolve_management(polygons,dissolved,map_fields[i])
        else:
            print "%s exists, skipping" % dissolved
    
        lyr = ap.mapping.Layer(layer_template)
        lyr.name = map_layer_labels[i]
    
        lyr.replaceDataSource(WORKSPACE, "FILEGDB_WORKSPACE", dissolved, True)
        lyr.symbology.valueField = map_fields[i]
        lyr.symbology.classValues = map_values[map_fields[i]]
        
        if grpLyr.isGroupLayer:
            ap.mapping.AddLayerToGroup(df,grpLyr,lyr)
        else:
            ap.mapping.AddLayer(df, lyr)
        
        outfile = "bin/%s%s_%s.ai"%(prefix, map_layer_labels[i])
        print "exporting %s" % outfile
        
        ap.mapping.ExportToAI(mxd, outfile,resolution=ai_res)
        ap.mapping.RemoveLayer(df, ap.mapping.ListLayers(mxd,lyr.name)[0])


