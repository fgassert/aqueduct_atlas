'''
Created on Aug 20, 2012

@author: Francis Gassert

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/.
'''

import arcpy as ap
import generator
from constants import *
import numpy as np

G_args = (HFO_OUT, BASINPOLY, FLOODPOLY)
G_kwargs = {'make_csv':"bin/%s.csv" % HFO_OUT,
            'make_plot':"bin/%s.pdf" % HFO_OUT,
            'make_map':"bin/%s.jpg" % HFO_OUT,
            }

class gHFO(generator.APGenerator):
    """docstring for HFO"""
    generator_name = "flood occurrence"
    plot_field_name = "HFO"
    threshold_values = (0,1,3,9,27,999999999999)
    map_layer_label = "Flood count"
    c1 = 1
    base = 3
    category_names = MAP_CLASSES["HFO_cat"]
    
    def __init__(self):
        super(gHFO, self).__init__()
        
    def _make(self, output_file, basin_poly, flood_poly, **kwargs):
        print "joining floods"
        fm = ap.FieldMappings()
        fm.addTable(basin_poly)
        ap.SpatialJoin_analysis(basin_poly, flood_poly, "tmp", "JOIN_ONE_TO_ONE", "KEEP_ALL", fm, "intersect")
        arr = ap.da.TableToNumPyArray("tmp",(BASIN_ID_FIELD,"join_count"))
        oid = arr[BASIN_ID_FIELD]
        hfo = arr["join_count"]
        
        hfo_s = self.score(hfo)
        hfo_s[hfo==0] = 0
        hfo_cat = self.categorize(hfo_s)
        
        joinarray = np.rec.fromarrays((oid,hfo,hfo_s,hfo_cat),names=(BASIN_ID_FIELD,self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name))
        
        ap.CopyFeatures_management(basin_poly,output_file)
        ap.da.ExtendTable(output_file,BASIN_ID_FIELD,joinarray,BASIN_ID_FIELD)
    
    def _get_array(self, output_file):
        fields = (BASIN_ID_FIELD, self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name)
        array = super(gHFO,self)._get_array(output_file, fields)
        return array

def gen(*args, **kwargs):
    return gHFO().gen(*args, **kwargs)

if __name__ == '__main__':
    gen(*G_args, workspace=WORKSPACE, overwrite=True, **G_kwargs)