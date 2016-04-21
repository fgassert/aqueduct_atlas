'''
Created on Sept 6, 2012

@author: Francis Gassert

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/.
'''

import arcpy as ap
import generator
import numpy as np
from constants import *
import time

G_args=(GW_OUT, BASINPOLY, GWPOLY)
G_kwargs={'make_csv':"bin/%s.csv" % GW_OUT, 
        'make_plot':"bin/%s.pdf" % GW_OUT, 
        'make_map':"bin/%s.jpg" % GW_OUT, 
        }

TMP = "in_memory/GW_tmp"

class gGW(generator.APGenerator):
    """docstring for gGW"""
    generator_name = "Groundwater Stress"
    plot_field_name = "GW"
    threshold_values = (0,1,5,10,20,999999999999)
    map_layer_label = "Groundwater Stress"
    c1 = 2.5
    base = 2
    category_names = MAP_CLASSES["GW_cat"]

    
    def __init__(self):
        super(gGW, self).__init__()
    
    def _make(self, output_file, basin_poly, gw_poly, **kwargs):
        #print "integerizing"
        #ap.CheckOutExtension("Spatial")
        #integerized = ap.sa.Int(ap.sa.Raster(gw_raster)*1000)
        #print "polygonizing"
        #ap.RasterToPolygon_conversion(integerized, gw_poly)
        #ap.CheckInExtension("Spatial")
        
        ap.CopyFeatures_management(gw_poly, output_file)
        #ap.AddField_management(output_file, self.plot_field_name, "DOUBLE")
        #ap.CalculateField_management(output_file, self.plot_field_name, "!grid_code!/1000.", "PYTHON")
        
        arr = ap.da.TableToNumPyArray(output_file,(GW_ID_FIELD,"grid_code"))
        oid = arr[GW_ID_FIELD]
        gw = arr["grid_code"].astype(np.double)/1000.0
        
        gw_mod = gw.copy()
        gw_mod[gw_mod<5] = np.minimum(gw_mod+1.5,5)
        gw_s = self.score(gw_mod)
        gw_cat = self.categorize(gw_s)
        
        joinarray = np.rec.fromarrays((oid,gw,gw_s,gw_cat),names=(GW_ID_FIELD,self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name))
        
        ap.da.ExtendTable(output_file,GW_ID_FIELD,joinarray,GW_ID_FIELD)
        
    def _get_array(self, output_file):
        print "generating table"
        fields = [GW_ID_FIELD,self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name]
        array = super(gGW,self)._get_array(output_file, fields)
        return array
       
def gen(*args, **kwargs):
    return gGW().gen(*args, **kwargs) 

if __name__ == '__main__':
    gen(*G_args, workspace=WORKSPACE, overwrite=True, **G_kwargs)