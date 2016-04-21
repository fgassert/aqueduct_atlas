'''
Created on Sept 7, 2012

@author: Francis Gassert

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/.
'''

import arcpy as ap
import generator
import numpy as np
from constants import *

G_args = (WSV_OUT, BASINPOLY, BTCSV)
G_kwargs = {'make_csv':"bin/%s.csv" % WSV_OUT,
            'make_plot':"bin/%s.pdf" % WSV_OUT,
            'make_map':"bin/%s.jpg" % WSV_OUT,
            }

class gWSV(generator.APGenerator):
    """docstring for gWSV"""
    generator_name = "inter-annual variability"
    plot_field_name = "WSV"
    threshold_values = (0,.25,.50,.75,1,999999999999)
    map_layer_label = "Stdev. of discharge / mean discharge"
    c1 = .25
    base = .25
    category_names = MAP_CLASSES["WSV_cat"]
    
    def __init__(self):
        super(gWSV, self).__init__()
    
    def _make(self, output_file, basin_poly, bt_csv, **kwargs):
        print "loading data"
        bt = np.genfromtxt(bt_csv,np.double,skip_header=1,delimiter=',')
        mean_bt = np.mean(bt[:,1:],1)
        std_bt = np.std(bt[:,1:],1,ddof=1)
        wsv = std_bt/mean_bt
        
        wsv_s = self.score(wsv,logscale=False)
        wsv_cat = self.categorize(wsv_s)
        
        joinarray = np.rec.fromarrays((bt[:,0],mean_bt,std_bt,wsv,wsv_s,wsv_cat),names=(BASIN_ID_FIELD,"MEANBT","STDBT",self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name))
        
        print "joining data"
        ap.CopyFeatures_management(basin_poly,output_file)
        ap.da.ExtendTable(output_file,BASIN_ID_FIELD,joinarray,BASIN_ID_FIELD)
        
    def _get_array(self, output_file):
        print "generating table"
        fields = [BASIN_ID_FIELD,"MEANBT","STDBT",self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name]
        array = super(gWSV,self)._get_array(output_file, fields)
        return array
        
       
def gen(*args, **kwargs):
    return gWSV().gen(*args, **kwargs) 

if __name__ == '__main__':
    gen(*G_args, workspace=WORKSPACE, overwrite=True, **G_kwargs)
    #gen(*G_args, workspace=WORKSPACE, overwrite=False, map_values = (0,.5,1,1.5,2,99999), **G_kwargs)