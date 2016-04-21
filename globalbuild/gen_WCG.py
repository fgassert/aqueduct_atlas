'''
Created on Sept 21, 2012

@author: Francis Gassert

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/.
'''

import arcpy as ap
import generator
import numpy as np
import matplotlib.mlab as mlab
from constants import *

G_args=(WCG_OUT, ADMINPOLY, ACCESSCSV)
G_kwargs={'make_csv':"bin/%s.csv" % WCG_OUT, 
        'make_plot':"bin/%s.pdf" % WCG_OUT, 
        'make_map':"bin/%s.jpg" % WCG_OUT, 
        }

WCG_COUNTRY_ID = "iso_n3"

class gWCG(generator.APGenerator):
    """docstring for gWCG"""
    generator_name = "Water Access"
    plot_field_name = "WCG"
    threshold_values = (0,.02,0.05,0.1,.2,1)
    map_layer_label = "population without access to water"
    c1 = 0.025
    base = 2
    category_names = MAP_CLASSES["WCG_cat"]

    
    def __init__(self):
        super(gWCG, self).__init__()
    
    def _make(self, output_file, admin_poly, access_csv, **kwargs):
        print "loading data"
        wc_arr = mlab.csv2rec(access_csv,delimiter=',')
        id_field = wc_arr[WCG_COUNTRY_ID]
        wc_all = wc_arr['national_pop_x1000'].astype(np.double)
        wc_access = wc_arr['water_national_total_improved_x1000'].astype(np.double)
        wcg = 1-wc_access/wc_all
        wcg[wc_access<1]=np.nan
        
        wcg_s = self.score(wcg)
        wcg_cat = self.categorize(wcg_s)
        
        joinarray = np.rec.fromarrays((id_field,wc_access,wc_all,wcg,wcg_s,wcg_cat),names=(ADMIN_ID_FIELD,"WCG_water","WCG_all",self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name))
                
        print "joining data"
        ap.CopyFeatures_management(admin_poly,output_file)
        ap.da.ExtendTable(output_file,ADMIN_ID_FIELD,joinarray,ADMIN_ID_FIELD)
        
    def _get_array(self, output_file):
        print "generating table"
        fields = [ADMIN_ID_FIELD,"WCG_water","WCG_all",self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name]
        array = super(gWCG,self)._get_array(output_file, fields)
        return array
        
       
def gen(*args, **kwargs):
    return gWCG().gen(*args, **kwargs) 

if __name__ == '__main__':
    gen(*G_args, workspace=WORKSPACE, overwrite=True, **G_kwargs)