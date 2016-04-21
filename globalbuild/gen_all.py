'''
Created on Aug 20, 2012

@author: Francis Gassert

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/.
'''

import arcpy as ap
import gen_gu, gen_BWS, gen_WSV, gen_SV, gen_HFO, gen_DRO, gen_STOR, gen_GW, gen_WRI, gen_ECO_S, gen_MC, gen_ECO_V, gen_WCG
from constants import *
import gen_merge, aggregate_scores
import matplotlib.mlab as mlab
import generator
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

REGENERATE_ALL = False

GENERATORLIST = [gen_BWS, gen_WSV, gen_SV, gen_HFO, gen_DRO, gen_STOR, gen_GW, gen_WRI, gen_ECO_S, gen_MC, gen_ECO_V, gen_WCG]

G_args=(GLOBAL_OUT, GUPOLY, GENERATORLIST)
G_kwargs={'make_csv':"bin/global_%s.csv" % TIMESTAMP, 
        'make_map':"%s.mxd" % os.path.splitext(OUTPUT_GDB)[0], 
        'map_fields':MAP_FIELDS,
        'map_layer_labels':MAP_LABELS,
        'map_values':MAP_CLASSES,
        'extra_features':MXD_EXTRA_FEATURES,
        }



class gAll(generator.APGenerator):
    
    generator_name = "all"
    plot_field_names = []
    map_layer_labels = []
    threshold_values = (0,1,2,3,4,5,6,7)
    map_labels = ["low","low to medium","medium to high","high","extremely high"]
    
    def __init__(self):
        super(gAll,self).__init__()
        
    def _make(self, output_file, gu_poly, generator_list, overwrite=False, extra_features=None, **kwargs):
        print "generating feature class"
        if not(ap.Exists(OUTPUT_GDB)):
            ap.CreateFileGDB_management(".",OUTPUT_GDB)
        if extra_features is not None:
            print "copying extra features"
            for f in extra_features:
                ap.Project_management(f,os.path.join(OUTPUT_GDB,os.path.basename(f)),PRJNAME)
                
        
    def _postprocess(self, output_file, gu_poly, generator_list, overwrite=False, supplementary_figures=False, **kwargs):
        generatoroutputs = []
    
        for g in generator_list:
            if supplementary_figures:
                gkw = g.G_kwargs
            else:
                gkw = {}
            generatoroutputs.append(g.gen(*g.G_args, overwrite = overwrite, **gkw))
        
        gu_arr = gen_gu.gen(*gen_gu.G_args, overwrite=overwrite, **gen_gu.G_kwargs)
        print gu_arr
        
        print "merging arrays"
        out_arr = gen_merge.join_recs_on_keys(gu_arr, generatoroutputs, (BASIN_ID_FIELD, ADMIN_ID_FIELD, GW_ID_FIELD))
        sr = ap.SpatialReference(PRJNAME)
        ap.Project_management(gu_poly,output_file,sr)
        print out_arr[BASIN_NAME_FIELD]
        
        missing_fields = np.setdiff1d(ALL_FIELDS,out_arr.dtype.names)
        if len(missing_fields)>0:
            print "WARNING: missing fields %s" % missing_fields
            obs = len(out_arr[GU_FIELD])
            out_arr = mlab.rec_append_fields(out_arr, missing_fields, [np.repeat(np.nan, obs) for _ in missing_fields])
                
        extra_fields = np.setdiff1d(out_arr.dtype.names,ALL_FIELDS)
        print "dropping extra fields %s" % extra_fields
        out_arr = mlab.rec_drop_fields(out_arr,extra_fields)
        
        print "generating pre-weighted_columns"
        if WEIGHTING_SCHEMES is not None:
            new_cols = []
            names = []
            for n, weights in WEIGHTING_SCHEMES.iteritems():
                keys = weights.keys()
                values = weights.values()
                indicator_array = np.vstack([out_arr[f] for f in keys]).T
                indicator_array[indicator_array==NULL_VALUE] = np.nan
                scores = np.squeeze(np.asarray(aggregate_scores.aggregate_scores(indicator_array,values)))
                scores[np.isnan(scores)]=NULL_VALUE
                new_cols.append(scores)
                names.append(n)
            out_arr = mlab.rec_append_fields(out_arr, names, new_cols)
        
        for field in MAP_FIELDS:
            out_arr[field][out_arr[field]==""] = "No data"
        
        
        mlab.rec2csv(out_arr,"bin/test.csv")
        print "dropping fields"
        drop = [f.baseName for f in ap.ListFields(output_file) if not(f.required) and not(f.baseName == GU_FIELD)]
        if len(drop)>0:
            ap.DeleteField_management(output_file,drop)
        
        print "joining"
        ap.da.ExtendTable(output_file,GU_FIELD,out_arr,GU_FIELD)
        
        print "indexing"
        try:
            ap.AddSpatialIndex_management(output_file)
            ap.AddIndex_management(output_file,GU_FIELD,GU_FIELD,"UNIQUE")
        except Exception, e:
            print e
            

    def _get_array(self, output_file):
        print "generating table"
        fields = "*"
        array = super(gAll,self)._get_array(output_file, fields)
        return array
    
    def make_map(self, make_map, output_layer, map_fields=None, map_layer_labels=None, map_values=None, map_class_labels=None, extra_features=None, **kwargs):
        if map_fields is None:
            map_fields = self.plot_field_names
        print "Generating map"
        if map_values is None:
            map_values = self.threshold_values
        mxd = ap.mapping.MapDocument(MXD_TEMPLATE_EMPTY)
        df = ap.mapping.ListDataFrames(mxd)[0]
        if map_layer_labels is None:
            map_layer_labels = map_fields

        if len(map_fields)!=len(map_layer_labels):
            print "ERROR: Labels != fields"
        if mxd.relativePaths == False:
            print "ERROR: RelativePaths == False"
        
        
        for i in range(len(map_fields)):
            lyr = ap.mapping.Layer(LAYER_TEMPLATE)
            lyr.name = map_layer_labels[i]
            lyr.replaceDataSource(OUTPUT_GDB, "FILEGDB_WORKSPACE", os.path.split(output_layer)[-1], True)
            lyr.symbology.valueField = map_fields[i]
            lyr.symbology.classValues = map_values[map_fields[i]]
            if map_class_labels is not None:
                lyr.symbology.classLabels = map_class_labels
            ap.mapping.AddLayer(df, lyr)
        
        if extra_features is not None:
            for f in extra_features:
                lyr = ap.mapping.Layer(LAYER_TEMPLATE_HOLLOW)
                lyr.replaceDataSource(OUTPUT_GDB, "FILEGDB_WORKSPACE", os.path.basename(f), False)
                lyr.name = os.path.basename(f)
                ap.mapping.AddLayer(df, lyr)
                
        
        print "Exporting map"
        mxd.saveACopy(make_map)
        
        del mxd
        return 1

def gen(*args, **kwargs):
    return gAll().gen(*args, **kwargs)

if __name__ == '__main__':
    print TIMESTAMP
    #gen(*G_args, workspace = WORKSPACE, overwrite = REGENERATE_ALL, **G_kwargs)
    gen(*G_args, workspace = WORKSPACE, overwrite = False, **G_kwargs)